# -*- coding: utf-8 -*-
"""
Passo 2 - Construcao das series de tempo ate a falha (TTF).

Como o dataset e de snapshots (nao run-to-failure), usamos um modelo de
degradacao para gerar os TTF:
  - degradacao cresce de forma exponencial: D(tau) = D0 * exp(rho*tau);
  - a taxa media rho_bar e calibrada nos dados (baseline -> severidade maxima);
  - cada unidade simulada recebe uma taxa aleatoria (variabilidade operacional);
  - a unidade falha quando D cruza o limiar L;
  - quem nao cruza ate o horizonte vira dado CENSURADO a direita.

Entrada: features.csv (passo 1). Saida: ttf.csv.
"""
import os
import numpy as np
import pandas as pd

import config
import graficos


def _ttf_de_um_modo(valores_por_nivel, rng):
    """Recebe um dict {nivel: array de RMS} e devolve (ttf, censura, info)."""
    niveis = sorted(valores_por_nivel.keys())
    baseline = np.array(valores_por_nivel[0])          # nivel 0 = saudavel
    mu0 = baseline.mean()
    sev_medias = [np.mean(valores_por_nivel[n]) for n in niveis if n > 0]

    S = len(sev_medias)
    tau_max = S * config.HORAS_POR_NIVEL               # horizonte de observacao
    D_max = sev_medias[-1]
    rho_bar = np.log(D_max / mu0) / tau_max            # taxa media calibrada
    L = mu0 + config.FRAC_LIMIAR * (D_max - mu0)       # limiar de falha

    ttf, censura = [], []
    for _ in range(config.N_UNIDADES):
        D0 = rng.choice(baseline)                      # baseline sorteado dos dados
        rho = rho_bar * np.exp(rng.normal(0, config.COV_TAXA))  # taxa da unidade
        if rho <= 0 or L <= D0:
            t = tau_max * 10                           # praticamente nao falha
        else:
            t = np.log(L / D0) / rho                   # instante em que D atinge L
        if t > tau_max:
            ttf.append(tau_max); censura.append(1)     # censura a direita
        else:
            ttf.append(t); censura.append(0)
    info = {"mu0": mu0, "D_max": D_max, "L": L, "rho_bar": rho_bar,
            "tau_max": tau_max}
    return np.array(ttf), np.array(censura), info


def construir(features=None):
    if features is None:
        features = pd.read_csv(os.path.join(config.SAIDA_TAB, "features.csv"))
    rng = np.random.default_rng(config.SEMENTE)

    linhas = []
    for modo in config.MODOS:
        sub = features[features["modo"] == modo["id"]]
        valores_por_nivel = {n: g["valor"].values
                             for n, g in sub.groupby("nivel")}
        ttf, cens, info = _ttf_de_um_modo(valores_por_nivel, rng)

        n_cens = int(cens.sum())
        falhas = ttf[cens == 0]
        print("  [ttf] %-30s falhas=%d censura=%d (%.0f%%)  L=%.4f"
              % (modo["nome"], len(falhas), n_cens,
                 100 * n_cens / len(ttf), info["L"]))

        graficos.fig_ttf_hist(modo, falhas, n_cens, info["L"], info["tau_max"])
        for t, c in zip(ttf, cens):
            linhas.append([modo["id"], t, int(c)])

    df = pd.DataFrame(linhas, columns=["modo", "ttf", "censura"])
    caminho = os.path.join(config.SAIDA_TAB, "ttf.csv")
    df.to_csv(caminho, index=False)
    print("  [ttf] salvo:", caminho)
    return df


if __name__ == "__main__":
    construir()
