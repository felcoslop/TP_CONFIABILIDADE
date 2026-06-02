# -*- coding: utf-8 -*-
"""
Funcoes de apoio compartilhadas: leitura dos sinais, calculo do indicador de
degradacao (RMS em banda) e o ranqueamento por median rank da disciplina.
"""
import os
import numpy as np
import pandas as pd
from scipy.signal import welch

import config


def caminho_longo(caminho):
    """Adiciona o prefixo \\?\ pra contornar o limite de 260 chars do Windows.
    Os caminhos do dataset passam de 290 caracteres, entao sem isso o open()
    do Python da FileNotFoundError."""
    caminho = os.path.abspath(caminho)
    if not caminho.startswith("\\\\?\\"):
        caminho = "\\\\?\\" + caminho
    return caminho


def caminho_csv(motor, vel, cond, canal):
    """Monta o caminho do CSV de vibracao de uma condicao/canal."""
    nome = "Vibration_Motor-%d_%d_time-%s-ch%d.csv" % (motor, vel, cond, canal)
    return os.path.join(config.DATASET, "Vibration", "Motor-%d" % motor,
                        str(vel), cond, nome)


def ler_repeticoes(motor, vel, cond, canal):
    """Le um CSV e devolve a matriz (amostras x repeticoes).
    Cada coluna do CSV (alem de 'time') e uma repeticao independente da medicao.
    No modo rapido le so um trecho do arquivo."""
    cam = caminho_longo(caminho_csv(motor, vel, cond, canal))
    nrows = config.NROWS_RAPIDO if config.MODO_RAPIDO else None
    df = pd.read_csv(cam, nrows=nrows)
    cols = [c for c in df.columns if c != "time"]
    return df[cols].values.astype(float)


def band_rms(sinal_1d, fmin, fmax):
    """RMS do sinal dentro de uma banda de frequencia (via densidade espectral
    de Welch). E o nosso indicador de degradacao."""
    x = sinal_1d - sinal_1d.mean()
    f, Pxx = welch(x, fs=config.FS, nperseg=4096)
    m = (f >= fmin) & (f < fmax)
    return np.sqrt(np.trapezoid(Pxx[m], f[m]))


def band_rms_repeticoes(motor, vel, cond, canal, banda):
    """Aplica o band_rms em cada repeticao (coluna) de uma condicao.
    Devolve um vetor com um valor de degradacao por repeticao."""
    mat = ler_repeticoes(motor, vel, cond, canal)
    fmin, fmax = banda
    return np.array([band_rms(mat[:, j], fmin, fmax) for j in range(mat.shape[1])])


def existe_condicao(motor, vel, cond, canal):
    """Confere se o arquivo de uma condicao existe (algumas severidades faltam)."""
    return os.path.exists(caminho_longo(caminho_csv(motor, vel, cond, canal)))


def median_rank(i, n):
    """Median rank de Benard (formula da disciplina): (i - 0,3)/(n + 0,4),
    com i = posicao (1..n) na amostra ordenada."""
    return (i - 0.3) / (n + 0.4)


def median_rank_censura(tempos, censuras):
    """Median rank ajustado pra dados com censura a direita (metodo de Johnson,
    como no script 4_Sobrevivencia.py da disciplina).
    Recebe tempos e o vetor de censura (0=falha, 1=censura) e devolve os pares
    (tempo_de_falha, median_rank) apenas das falhas, ordenados."""
    ordem = np.argsort(tempos)
    t = np.array(tempos)[ordem]
    c = np.array(censuras)[ordem]
    n = len(t)
    i_ant = 0.0           # i da falha anterior
    pares = []
    for k in range(n):
        if c[k] == 0:     # so calcula posicao pra falhas
            # numero de itens que ainda restam (incluindo o atual)
            n_rest = n - k
            incremento = (n + 1 - i_ant) / (1 + n_rest)
            i_k = i_ant + incremento
            pares.append((t[k], median_rank(i_k, n)))
            i_ant = i_k
    return pares


def garantir_pastas():
    """Cria as pastas de saida se nao existirem."""
    os.makedirs(config.SAIDA_FIG, exist_ok=True)
    os.makedirs(config.SAIDA_TAB, exist_ok=True)
