# -*- coding: utf-8 -*-
"""
Passo 4 - Intervalos de confianca por bootstrap.

Reamostra com reposicao as TTF (preservando o status de censura), reajusta a
Weibull a cada reamostra e tira os percentis 2,5% e 97,5% dos parametros.
Mesma ideia do script 6_2_IC_Bootstrap.py da disciplina, mas com censura.

Pra aguentar R=10^4 reamostragens, o ajuste no laco usa um MLE proprio da Weibull
(rapido), em vez da biblioteca pesada.
"""
import os
import numpy as np
import pandas as pd
from scipy.optimize import minimize

import config
import graficos


def _neg_loglik_weibull(p_log, t_fal, t_cens):
    """-log-verossimilhanca da Weibull com censura a direita.
    p_log = [ln(beta), ln(eta)] (log pra manter os parametros positivos)."""
    beta, eta = np.exp(p_log[0]), np.exp(p_log[1])
    # contribuicao das falhas: ln f(t)
    z = t_fal / eta
    ll = np.sum(np.log(beta / eta) + (beta - 1) * np.log(z) - z ** beta)
    # contribuicao das censuras: ln R(t)
    if len(t_cens):
        ll += np.sum(-(t_cens / eta) ** beta)
    return -ll


def _mle_weibull(t_fal, t_cens, init):
    """Estima (beta, eta) por maxima verossimilhanca com censura."""
    p0 = np.log(init)
    res = minimize(_neg_loglik_weibull, p0, args=(t_fal, t_cens),
                   method="Nelder-Mead")
    beta, eta = np.exp(res.x[0]), np.exp(res.x[1])
    return beta, eta


def rodar(resultados, ttf=None):
    if ttf is None:
        ttf = pd.read_csv(os.path.join(config.SAIDA_TAB, "ttf.csv"))
    rng = np.random.default_rng(config.SEMENTE + 1)

    ic_todos = {}
    linhas = []
    for modo in config.MODOS:
        if modo["id"] not in resultados:
            continue
        sub = ttf[ttf["modo"] == modo["id"]]
        t = sub["ttf"].values
        c = sub["censura"].values
        init = np.array([resultados[modo["id"]]["beta"],
                         resultados[modo["id"]]["eta"]])

        betas, etas = [], []
        n = len(t)
        for _ in range(config.R_BOOTSTRAP):
            idx = rng.integers(0, n, n)               # reamostra com reposicao
            tb, cb = t[idx], c[idx]
            t_fal, t_cens = tb[cb == 0], tb[cb == 1]
            if len(t_fal) < 5:                         # reamostra ruim, ignora
                continue
            try:
                b, e = _mle_weibull(t_fal, t_cens, init)
                if 0 < b < 50 and e > 0:
                    betas.append(b); etas.append(e)
            except Exception:
                continue

        betas, etas = np.array(betas), np.array(etas)
        ic_beta = (np.percentile(betas, 2.5), np.percentile(betas, 97.5))
        ic_eta = (np.percentile(etas, 2.5), np.percentile(etas, 97.5))
        ic_todos[modo["id"]] = {"beta": ic_beta, "eta": ic_eta,
                                "amostras_beta": betas, "amostras_eta": etas}

        graficos.fig_bootstrap(modo, [betas, etas],
                               [r"$\beta$ (forma)", r"$\eta$ (escala) [h]"],
                               [ic_beta, ic_eta])
        print("  [bootstrap] %-30s beta IC95=[%.2f, %.2f]  eta IC95=[%.0f, %.0f]"
              % (modo["nome"], ic_beta[0], ic_beta[1], ic_eta[0], ic_eta[1]))
        linhas.append([modo["id"], round(ic_beta[0], 3), round(ic_beta[1], 3),
                       round(ic_eta[0], 1), round(ic_eta[1], 1)])

    df = pd.DataFrame(linhas, columns=["modo", "beta_ic_inf", "beta_ic_sup",
                                       "eta_ic_inf", "eta_ic_sup"])
    df.to_csv(os.path.join(config.SAIDA_TAB, "bootstrap_ic.csv"), index=False)
    print("  [bootstrap] salvo: bootstrap_ic.csv")
    return ic_todos


if __name__ == "__main__":
    import ajustar_distribuicoes
    res = ajustar_distribuicoes.ajustar()
    rodar(res)
