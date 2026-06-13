# -*- coding: utf-8 -*-
"""
Passo 3 - Ajuste de distribuicoes de vida.

Sobre as TTF de cada modo, ajusta Exponencial, Weibull e Lognormal com suporte a
censura a direita (biblioteca reliability, que usa maxima verossimilhanca).
Compara as tres pelo criterio AICc e por Kolmogorov-Smirnov, e escolhe a melhor.
Tambem calcula os median ranks (metodo da disciplina) para os graficos.

Entrada: ttf.csv. Saida: parametros.csv + graficos (papel Weibull, ajuste das CDFs).
"""
import os
import numpy as np
import pandas as pd
from scipy import stats
from reliability.Fitters import (Fit_Weibull_2P, Fit_Exponential_1P,
                                 Fit_Lognormal_2P)
import warnings
warnings.filterwarnings("ignore")

import config
import utils
import graficos


def _ajustar_um(falhas, censuradas):
    """Ajusta as 3 distribuicoes e devolve um dict com os objetos e metricas."""
    rc = censuradas.tolist() if len(censuradas) else None
    fw = Fit_Weibull_2P(failures=falhas.tolist(), right_censored=rc,
                        show_probability_plot=False, print_results=False)
    fe = Fit_Exponential_1P(failures=falhas.tolist(), right_censored=rc,
                            show_probability_plot=False, print_results=False)
    fl = Fit_Lognormal_2P(failures=falhas.tolist(), right_censored=rc,
                          show_probability_plot=False, print_results=False)

    dists = {"Weibull": fw.distribution,
             "Exponencial": fe.distribution,
             "Lognormal": fl.distribution}
    aicc = {"Weibull": fw.AICc, "Exponencial": fe.AICc, "Lognormal": fl.AICc}

    # KS de cada distribuicao contra as falhas observadas
    ks = {nome: stats.kstest(falhas, d.CDF).statistic for nome, d in dists.items()}

    melhor = min(aicc, key=aicc.get)   # menor AICc vence
    return {"fits": {"Weibull": fw, "Exponencial": fe, "Lognormal": fl},
            "dists": dists, "aicc": aicc, "ks": ks, "melhor": melhor,
            "beta": fw.beta, "eta": fw.alpha}


def ajustar(ttf=None):
    if ttf is None:
        ttf = pd.read_csv(os.path.join(config.SAIDA_TAB, "ttf.csv"))

    resultados = {}
    linhas = []
    for modo in config.MODOS:
        sub = ttf[ttf["modo"] == modo["id"]]
        falhas = sub.loc[sub["censura"] == 0, "ttf"].values
        censuradas = sub.loc[sub["censura"] == 1, "ttf"].values
        if len(falhas) < 3:
            print("  [ajuste] %s: poucas falhas, pulando" % modo["id"])
            continue

        r = _ajustar_um(falhas, censuradas)
        r["falhas"], r["censuradas"] = falhas, censuradas
        # median ranks (com correcao de censura) pros graficos
        r["pares_mr"] = utils.median_rank_censura(sub["ttf"].values,
                                                  sub["censura"].values)
        resultados[modo["id"]] = r

        # graficos (passa n_falhas/n_total pro CDF explicar a truncagem empirica)
        tmax = float(np.max(falhas)) * 1.05
        n_total = len(falhas) + len(censuradas)
        graficos.fig_papel_weibull(modo, r["pares_mr"], r["beta"], r["eta"])
        graficos.fig_ajuste_cdf(modo, r["pares_mr"], r["dists"], tmax,
                                n_falhas=len(falhas), n_total=n_total)

        print("  [ajuste] %-30s melhor=%-11s (AICc W=%.0f E=%.0f L=%.0f)"
              % (modo["nome"], r["melhor"], r["aicc"]["Weibull"],
                 r["aicc"]["Exponencial"], r["aicc"]["Lognormal"]))

        linhas.append([modo["id"], modo["nome"], r["melhor"],
                       round(r["beta"], 3), round(r["eta"], 1),
                       round(r["fits"]["Exponencial"].Lambda, 8),
                       round(r["fits"]["Lognormal"].mu, 3),
                       round(r["fits"]["Lognormal"].sigma, 3),
                       round(r["aicc"]["Weibull"], 1),
                       round(r["aicc"]["Exponencial"], 1),
                       round(r["aicc"]["Lognormal"], 1)])

    cols = ["modo", "nome", "melhor_dist", "weibull_beta", "weibull_eta",
            "exp_lambda", "logn_mu", "logn_sigma",
            "aicc_weibull", "aicc_exp", "aicc_logn"]
    df = pd.DataFrame(linhas, columns=cols)
    caminho = os.path.join(config.SAIDA_TAB, "parametros.csv")
    df.to_csv(caminho, index=False)
    print("  [ajuste] salvo:", caminho)
    return resultados


if __name__ == "__main__":
    ajustar()
