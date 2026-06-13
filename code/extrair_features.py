# -*- coding: utf-8 -*-
"""
Passo 1 - Extracao de features.

Le os CSVs do dataset PRONOSTIA e calcula o indicador de degradacao (RMS)
para cada snapshot de cada rolamento.
"""
import os
import pandas as pd

import config
import utils
import graficos


def extrair():
    utils.garantir_pastas()
    linhas = []  # vai virar o features.csv

    print("  [features] Extraindo RMS dos 17 rolamentos...")
    
    # Vamos usar apenas a banda definida em config.MODOS[0]
    modo = config.MODOS[0]
    
    for r in config.ROLAMENTOS:
        nome = r["nome"]
        print(f"    -> Processando {nome} ({r['set']}) ...")
        
        rms_vals, n_arquivos_total = utils.rms_por_snapshot(r["set"], nome, modo["banda"])
        
        # Em modo rapido rms_vals tem menos pontos, mas n_arquivos_total eh o real
        passo_amostragem = 10 if config.MODO_RAPIDO else 1
        
        for idx, val in enumerate(rms_vals):
            snapshot_real = idx * passo_amostragem
            tempo_horas = (snapshot_real * config.SNAPSHOT_DURACAO) / 3600.0
            linhas.append([nome, r["condicao"], snapshot_real, tempo_horas, val])
        
    df = pd.DataFrame(linhas, columns=["rolamento", "condicao", "snapshot", "tempo_horas", "rms"])
    caminho = os.path.join(config.SAIDA_TAB, "features.csv")
    df.to_csv(caminho, index=False)
    
    # Gerar grafico de degradacao global
    graficos.fig_assinatura_pronostia(df)
    
    print("  [features] salvo:", caminho, "(%d linhas)" % len(df))
    return df


if __name__ == "__main__":
    extrair()
