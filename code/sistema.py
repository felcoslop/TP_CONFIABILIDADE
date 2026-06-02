# -*- coding: utf-8 -*-
"""
Passo 6 - Modelo do sistema e Monte Carlo.

O conjunto motor-bomba e um Diagrama de Blocos de Confiabilidade com dois
subsistemas em serie: o motor e a bomba (a falha de qualquer um para o conjunto).
A partir das distribuicoes ajustadas de um modo do motor e de um modo da bomba,
simulamos por Monte Carlo (inversao da CDF, t = F^-1(U)) tres configuracoes:

  - Serie    : um conjunto motor-bomba (arranjo real da bancada);
  - Paralelo : dois conjuntos ativos, basta um funcionar (redundancia hipotetica);
  - Standby  : um conjunto opera e o outro entra so quando o primeiro falha.

As formulas analiticas de disponibilidade verificam o resultado da simulacao.
Baseado no script 7_2_MC_sistema_dependencia.py da disciplina.
"""
import os
import numpy as np
import pandas as pd

import config
import graficos


def _amostra_ttf(dist, n, rng):
    """Sorteia n tempos ate a falha por inversao da CDF: t = F^-1(U)."""
    U = rng.random(n)
    return np.asarray(dist.quantile(U))


def rodar(resultados):
    rng = np.random.default_rng(config.SEMENTE + 2)
    N = config.N_MC_SISTEMA

    dist_motor = resultados[config.MODO_SISTEMA_MOTOR]["dists"][
        resultados[config.MODO_SISTEMA_MOTOR]["melhor"]]
    dist_bomba = resultados[config.MODO_SISTEMA_BOMBA]["dists"][
        resultados[config.MODO_SISTEMA_BOMBA]["melhor"]]

    # --- Monte Carlo dos tempos de falha ---
    # conjunto A (motor em serie com bomba): falha no primeiro que falhar
    mA, pA = _amostra_ttf(dist_motor, N, rng), _amostra_ttf(dist_bomba, N, rng)
    mB, pB = _amostra_ttf(dist_motor, N, rng), _amostra_ttf(dist_bomba, N, rng)
    conjA = np.minimum(mA, pA)
    conjB = np.minimum(mB, pB)

    ttf_serie = conjA                       # 1 conjunto
    ttf_paralelo = np.maximum(conjA, conjB)  # 2 ativos, basta 1
    ttf_standby = conjA + conjB              # reserva entra apos a 1a falha

    # --- R(t) do sistema por Monte Carlo ---
    tmax = float(np.percentile(ttf_standby, 95))
    tt = np.linspace(1, tmax, 400)
    curvas = {
        "Serie": np.mean(ttf_serie[None, :] > tt[:, None], axis=1),
        "Paralelo": np.mean(ttf_paralelo[None, :] > tt[:, None], axis=1),
        "Standby": np.mean(ttf_standby[None, :] > tt[:, None], axis=1),
    }
    graficos.fig_sistema_R(tt, curvas)

    # --- Disponibilidade: analitica e Monte Carlo ---
    mttf_motor = float(dist_motor.mean)
    mttf_bomba = float(dist_bomba.mean)
    A_motor = mttf_motor / (mttf_motor + config.MTTR_HORAS)
    A_bomba = mttf_bomba / (mttf_bomba + config.MTTR_HORAS)
    A_conj = A_motor * A_bomba                      # motor em serie com bomba

    mttf_conj = float(np.mean(conjA))
    lamb, mu = 1.0 / mttf_conj, 1.0 / config.MTTR_HORAS
    A_ana = {
        "Serie": A_conj,
        "Paralelo": 1 - (1 - A_conj) ** 2,
        "Standby": (mu ** 2 + mu * lamb) / (mu ** 2 + mu * lamb + lamb ** 2),
    }

    # MC da disponibilidade por renovacao alternada (sobe-cai) numa grade de tempo
    A_mc = _disponibilidade_mc(dist_motor, dist_bomba, mttf_conj, rng)

    nomes = ["Serie", "Paralelo", "Standby"]
    graficos.fig_disponibilidade(nomes, [A_ana[n] for n in nomes],
                                 [A_mc[n] for n in nomes])

    # --- salvar e imprimir ---
    R_missao = {n: float(np.mean(arr > config.TEMPO_MISSAO))
                for n, arr in [("Serie", ttf_serie), ("Paralelo", ttf_paralelo),
                               ("Standby", ttf_standby)]}
    linhas = []
    for n in nomes:
        print("  [sistema] %-9s  A_analitico=%.5f  A_MC=%.5f  R(%.0fh)=%.3f"
              % (n, A_ana[n], A_mc[n], config.TEMPO_MISSAO, R_missao[n]))
        linhas.append([n, round(A_ana[n], 5), round(A_mc[n], 5),
                       round(R_missao[n], 4)])
    df = pd.DataFrame(linhas, columns=["config", "A_analitico", "A_montecarlo",
                                       "R_missao"])
    df.to_csv(os.path.join(config.SAIDA_TAB, "sistema.csv"), index=False)
    print("  [sistema] MTTF conjunto (serie) = %.0f h" % mttf_conj)
    print("  [sistema] salvo: sistema.csv")
    return df


def _grade_estado(dist_m, dist_b, mttr, T, dt, rng):
    """Linha do tempo (sobe/cai) de um conjunto reparavel: fica em reparo por
    mttr horas a cada falha. Devolve vetor booleano de estado (True=operando)."""
    n = int(T / dt)
    estado = np.ones(n, dtype=bool)
    t = 0.0
    while t < T:
        up = min(float(dist_m.quantile(rng.random())),
                 float(dist_b.quantile(rng.random())))
        i_falha = int((t + up) / dt)
        i_volta = int(min(t + up + mttr, T) / dt)
        estado[i_falha:i_volta] = False    # periodo em reparo
        t += up + mttr
    return estado


def _disponibilidade_mc(dist_m, dist_b, mttf_conj, rng):
    """Disponibilidade de longo prazo por simulacao temporal.
    Serie = 1 conjunto; Paralelo = 2 conjuntos (sistema cai se os dois caem)."""
    T = 200 * mttf_conj
    dt = config.MTTR_HORAS / 4.0
    g1 = _grade_estado(dist_m, dist_b, config.MTTR_HORAS, T, dt, rng)
    g2 = _grade_estado(dist_m, dist_b, config.MTTR_HORAS, T, dt, rng)
    A_serie = g1.mean()
    A_paralelo = (g1 | g2).mean()
    # standby a frio (reserva nao envelhece ociosa) nao e o mesmo que paralelo;
    # sua simulacao correta exige modelar o reparador. Aqui verificamos standby
    # so pela formula analitica, entao deixamos o MC como NaN.
    return {"Serie": A_serie, "Paralelo": A_paralelo, "Standby": np.nan}


if __name__ == "__main__":
    import ajustar_distribuicoes
    res = ajustar_distribuicoes.ajustar()
    rodar(res)
