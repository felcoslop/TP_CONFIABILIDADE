# -*- coding: utf-8 -*-
"""
Orquestrador do trabalho de confiabilidade (EEE017).

Roda os 6 passos na ordem e gera todas as tabelas e figuras em resultados/.
O comportamento (base reduzida ou completa) e controlado por config.MODO_RAPIDO.

Uso:
    python main.py
"""
import time
import warnings
warnings.filterwarnings("ignore")

import config
import utils
import extrair_features
import construir_ttf
import ajustar_distribuicoes
import bootstrap_ic
import indices
import sistema


def main():
    t0 = time.time()
    utils.garantir_pastas()
    print("=" * 70)
    print("ANALISE DE CONFIABILIDADE - CONJUNTO MOTOR-BOMBA (EEE017)")
    print("Modo:", "RAPIDO (base reduzida)" if config.MODO_RAPIDO
          else "COMPLETO (base toda)")
    print("=" * 70)

    print("\n[1/6] Extraindo features dos sinais...")
    features = extrair_features.extrair()

    print("\n[2/6] Construindo as series de tempo ate a falha (TTF)...")
    ttf = construir_ttf.construir(features)

    print("\n[3/6] Ajustando distribuicoes (Exp, Weibull, Lognormal)...")
    resultados = ajustar_distribuicoes.ajustar(ttf)

    print("\n[4/6] Intervalos de confianca por bootstrap...")
    ic = bootstrap_ic.rodar(resultados, ttf)

    print("\n[5/6] Calculando indices de confiabilidade...")
    indices.calcular(resultados, ic)

    print("\n[6/6] Modelando o sistema e simulando por Monte Carlo...")
    sistema.rodar(resultados)

    print("\n" + "=" * 70)
    print("Concluido em %.1f s. Resultados em: %s" % (time.time() - t0,
                                                      config.SAIDA_FIG))
    print("=" * 70)


if __name__ == "__main__":
    main()
