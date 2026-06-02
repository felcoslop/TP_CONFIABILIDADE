# -*- coding: utf-8 -*-
"""
Passo 5 - Indices de confiabilidade.

Com a distribuicao escolhida (menor AICc), calcula para cada modo:
  - MTTF (tempo medio ate a falha) = media da distribuicao;
  - R(t) (confiabilidade) e h(t) (taxa de falha instantanea);
  - disponibilidade A = MTTF / (MTTF + MTTR).
Tambem desenha R(t) com a banda de confianca de 95% vinda do bootstrap (Weibull).

Entrada: resultados do passo 3 e os ICs do passo 4. Saida: indices.csv + graficos.
"""
import os
import numpy as np
import pandas as pd

import config
import graficos


def calcular(resultados, ic_boot):
    linhas = []
    for modo in config.MODOS:
        if modo["id"] not in resultados:
            continue
        r = resultados[modo["id"]]
        dist = r["dists"][r["melhor"]]          # distribuicao vencedora
        mttf = float(dist.mean)
        A = mttf / (mttf + config.MTTR_HORAS)   # disponibilidade

        # grade de tempo pros graficos
        tmax = max(2 * mttf, float(np.max(r["falhas"])))
        tt = np.linspace(1, tmax, 400)

        # R(t), h(t), f(t) da distribuicao vencedora
        graficos.fig_indices(modo, dist, tmax)

        # R(t) Weibull com banda de confianca do bootstrap
        betas = ic_boot[modo["id"]]["amostras_beta"]
        etas = ic_boot[modo["id"]]["amostras_eta"]
        R_central = np.exp(-(tt[:, None] / r["eta"]) ** r["beta"])[:, 0]
        # cada coluna = uma reamostra; percentis ao longo das reamostras
        R_boot = np.exp(-(tt[:, None] / etas[None, :]) ** betas[None, :])
        R_lo = np.percentile(R_boot, 2.5, axis=1)
        R_hi = np.percentile(R_boot, 97.5, axis=1)
        graficos.fig_R_banda(modo, tt, R_central, R_lo, R_hi)

        # interpretacao do beta (estagio na curva da banheira).
        # beta perto de 1 (0,9 a 1,2) ja conta como taxa ~ constante.
        if r["beta"] < 0.9:
            estagio = "mortalidade infantil"
        elif r["beta"] <= 1.2:
            estagio = "taxa aproximadamente constante"
        else:
            estagio = "desgaste (taxa crescente)"

        print("  [indices] %-30s MTTF=%.0f h  A=%.4f  beta=%.2f (%s)"
              % (modo["nome"], mttf, A, r["beta"], estagio))
        linhas.append([modo["id"], modo["nome"], r["melhor"], round(mttf, 1),
                       round(1.0 / mttf, 8), round(r["beta"], 3),
                       config.MTTR_HORAS, round(A, 5), estagio])

    cols = ["modo", "nome", "dist", "MTTF_h", "lambda_aprox", "beta",
            "MTTR_h", "disponibilidade", "estagio_banheira"]
    df = pd.DataFrame(linhas, columns=cols)
    df.to_csv(os.path.join(config.SAIDA_TAB, "indices.csv"), index=False)
    print("  [indices] salvo: indices.csv")

    # grafico resumo (MTTF e beta por modo)
    graficos.fig_resumo(df["modo"].tolist(), df["MTTF_h"].tolist(),
                        df["beta"].tolist())

    # figuras combinadas: R(t) e h(t) de todos os modos juntos, e curva da banheira
    dists_todos = {r["modo"]["nome"]: resultados[r["modo"]["id"]]["dists"][
                       resultados[r["modo"]["id"]]["melhor"]]
                   for r in [{"modo": m} for m in config.MODOS
                              if m["id"] in resultados]}
    # monta dict nome -> distribuicao na ordem dos modos
    dists_por_nome = {}
    for modo in config.MODOS:
        if modo["id"] in resultados:
            r = resultados[modo["id"]]
            dists_por_nome[modo["nome"]] = r["dists"][r["melhor"]]

    graficos.fig_rt_todos(list(dists_por_nome.keys()), dists_por_nome)
    graficos.fig_ht_todos(list(dists_por_nome.keys()), dists_por_nome)
    graficos.fig_banheira_esquema()
    return df


if __name__ == "__main__":
    import ajustar_distribuicoes
    import bootstrap_ic
    res = ajustar_distribuicoes.ajustar()
    ic = bootstrap_ic.rodar(res)
    calcular(res, ic)
