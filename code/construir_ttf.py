# -*- coding: utf-8 -*-
"""
Passo 2 - Construcao das series de tempo ate a falha (TTF).

No dataset PRONOSTIA, os dados sao run-to-failure (rodados ate a falha real).
Portanto, nao precisamos de simulacao Monte Carlo nem modelo de degradacao.
O TTF de cada rolamento eh simplesmente o tempo do seu ultimo snapshot.
Todos os dados sao falhas confirmadas (censura = 0).
"""
import os
import pandas as pd

import config
import graficos


def construir(features=None):
    if features is None:
        features = pd.read_csv(os.path.join(config.SAIDA_TAB, "features.csv"))

    print("  [ttf] Extraindo tempos de falha reais dos 17 rolamentos...")

    linhas = []
    ttf_vals = []
    
    # Agrupa por rolamento e pega o ultimo tempo_horas de cada um
    for rolamento, dados in features.groupby("rolamento"):
        ttf = dados["tempo_horas"].max()
        
        # censura=0 pois todos os rolamentos do PRONOSTIA foram rodados ate a falha
        censura = 0 
        
        linhas.append([config.MODOS[0]["id"], ttf, censura])
        ttf_vals.append(ttf)

    df = pd.DataFrame(linhas, columns=["modo", "ttf", "censura"])
    caminho = os.path.join(config.SAIDA_TAB, "ttf.csv")
    df.to_csv(caminho, index=False)
    
    modo = config.MODOS[0]
    horizonte = max(ttf_vals) * 1.1
    graficos.fig_ttf_hist(modo, ttf_vals, 0, 0, horizonte)
    
    print("  [ttf] %-30s falhas=%d censura=0" % (modo["nome"], len(ttf_vals)))
    print("  [ttf] salvo:", caminho)
    return df


if __name__ == "__main__":
    construir()
