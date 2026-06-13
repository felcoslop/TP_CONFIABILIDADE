# -*- coding: utf-8 -*-
"""
Funcoes de apoio compartilhadas: leitura dos sinais, calculo do indicador de
degradacao (RMS em banda) e o ranqueamento por median rank da disciplina.
"""
import os
import glob
import numpy as np
import pandas as pd
from scipy.signal import welch

import config


def listar_acc_files(bearing_set, bearing_nome):
    """Retorna lista de caminhos dos arquivos acc_*.csv de um rolamento."""
    pasta = os.path.join(config.DATASET, bearing_set, bearing_nome)
    arquivos = sorted(glob.glob(os.path.join(pasta, "acc_*.csv")))
    return arquivos


def ler_snapshot(caminho):
    """Le um snapshot CSV (2560 amostras). Retorna aceleração horizontal."""
    try:
        # Tenta ler com virgula, ignora linhas defeituosas
        df = pd.read_csv(caminho, header=None, sep=',', on_bad_lines='skip')
        if df.shape[1] < 5:
            # Tenta com ponto e virgula
            df = pd.read_csv(caminho, header=None, sep=';', on_bad_lines='skip')
        
        # O arquivo deveria ter: h, min, s, us, acc_h, acc_v
        # Retornamos a aceleracao horizontal (coluna 4)
        if df.shape[1] > 4:
            return df.iloc[:, 4].values.astype(float)
        else:
            # Retorna zeros se o arquivo estiver corrompido ou sem a coluna
            return np.zeros(2560)
    except Exception:
        return np.zeros(2560)


def band_rms(sinal_1d, fmin, fmax):
    """RMS do sinal dentro de uma banda de frequencia (via densidade espectral
    de Welch). E o nosso indicador de degradacao."""
    x = sinal_1d - sinal_1d.mean()
    f, Pxx = welch(x, fs=config.FS, nperseg=512)
    m = (f >= fmin) & (f < fmax)
    return np.sqrt(np.trapezoid(Pxx[m], f[m]))


def rms_por_snapshot(bearing_set, bearing_nome, banda):
    """Calcula o RMS para todos os snapshots de um rolamento."""
    arquivos = listar_acc_files(bearing_set, bearing_nome)
    
    # Se MODO_RAPIDO, pulamos alguns arquivos para processar rapido
    if config.MODO_RAPIDO:
        arquivos = arquivos[::10]
        
    rms_vals = []
    fmin, fmax = banda
    for arq in arquivos:
        sinal = ler_snapshot(arq)
        rms = band_rms(sinal, fmin, fmax)
        rms_vals.append(rms)
    return np.array(rms_vals), len(listar_acc_files(bearing_set, bearing_nome))


def median_rank(i, n):
    """Median rank de Benard (formula da disciplina): (i - 0,3)/(n + 0,4)."""
    return (i - 0.3) / (n + 0.4)


def median_rank_censura(tempos, censuras):
    """Median rank ajustado pra dados com censura a direita."""
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
