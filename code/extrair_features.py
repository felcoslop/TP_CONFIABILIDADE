# -*- coding: utf-8 -*-
"""
Passo 1 - Extracao de features.

Le os CSVs grandes do dataset e calcula o indicador de degradacao (RMS na banda
de cada modo) para cada repeticao de cada condicao. Salva tudo numa tabela
compacta (features.csv) pra que os passos seguintes nao precisem reler os CSVs.

E o unico passo caro (le os arquivos de centenas de MB).
"""
import os
import pandas as pd

import config
import utils
import graficos


def extrair():
    utils.garantir_pastas()
    linhas = []  # vai virar o features.csv (formato longo)

    for modo in config.MODOS:
        print("  [features] %s ..." % modo["nome"])
        rotulos, listas = [], []

        # condicao saudavel (nivel 0): junta as 3 medicoes healthy
        valores_saud = []
        for h in modo["healthy"]:
            v = utils.band_rms_repeticoes(modo["motor"], modo["vel"], h,
                                          modo["canal"], modo["banda"])
            valores_saud.extend(v)
            for val in v:
                linhas.append([modo["id"], h, 0, val])
        rotulos.append("saudavel")
        listas.append(valores_saud)

        # severidades (nivel 1, 2, 3, ...)
        for nivel, sev in enumerate(modo["severidades"], start=1):
            if not utils.existe_condicao(modo["motor"], modo["vel"], sev, modo["canal"]):
                print("    (aviso) condicao ausente, pulando:", sev)
                continue
            v = utils.band_rms_repeticoes(modo["motor"], modo["vel"], sev,
                                          modo["canal"], modo["banda"])
            for val in v:
                linhas.append([modo["id"], sev, nivel, val])
            rotulos.append("sev %d" % nivel)
            listas.append(list(v))

        # grafico da assinatura de degradacao deste modo
        graficos.fig_assinatura(modo, rotulos, listas)

    df = pd.DataFrame(linhas, columns=["modo", "condicao", "nivel", "valor"])
    caminho = os.path.join(config.SAIDA_TAB, "features.csv")
    df.to_csv(caminho, index=False)
    print("  [features] salvo:", caminho, "(%d linhas)" % len(df))
    return df


if __name__ == "__main__":
    extrair()
