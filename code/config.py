# -*- coding: utf-8 -*-
"""
Configuracao central do trabalho de confiabilidade.
Adaptado para o dataset PRONOSTIA (IEEE PHM 2012).
"""
import os

# =============================================================================
# Caminhos
# =============================================================================
RAIZ = os.path.dirname(os.path.abspath(__file__))

# O dataset atual: PRONOSTIA Full Test Set e Learning Set
DATASET = os.path.join(
    RAIZ, "..", "data", "dataset_full",
    "ieee-phm-2012-data-challenge-dataset-master"
)

# pastas de saida
SAIDA_FIG = os.path.join(RAIZ, "resultados", "figuras")
SAIDA_TAB = os.path.join(RAIZ, "resultados", "tabelas")

# =============================================================================
# Modo de execucao
# =============================================================================
MODO_RAPIDO = False
NROWS_RAPIDO = 2560  # no PRONOSTIA os arquivos tem 2560 linhas

FS = 25600.0  # taxa de amostragem dos sensores (Hz)
SNAPSHOT_DURACAO = 10.0  # s (duracao real entre arquivos)

# =============================================================================
# Constantes do modelo
# =============================================================================
# Como agora temos TTF real, grande parte da simulacao cai fora.
# numero de iteracoes do Monte Carlo do sistema (passo 6)
N_MC_SISTEMA = 10000 if MODO_RAPIDO else 100000

# numero de reamostragens do bootstrap (IC dos parametros)
R_BOOTSTRAP = 2000 if MODO_RAPIDO else 10000

# tempo de reparo medio (MTTR) por subsistema, em horas.
MTTR_HORAS = 24.0

SEMENTE = 42

# =============================================================================
# Dados dos rolamentos (17 rolamentos no total)
# =============================================================================
# Usaremos todos os 17 como uma unica populacao ("Rolamento sob carga acelerada")
ROLAMENTOS = [
    # Learning Set
    {"nome": "Bearing1_1", "condicao": 1, "set": "Learning_set"},
    {"nome": "Bearing1_2", "condicao": 1, "set": "Learning_set"},
    {"nome": "Bearing2_1", "condicao": 2, "set": "Learning_set"},
    {"nome": "Bearing2_2", "condicao": 2, "set": "Learning_set"},
    {"nome": "Bearing3_1", "condicao": 3, "set": "Learning_set"},
    {"nome": "Bearing3_2", "condicao": 3, "set": "Learning_set"},
    # Full Test Set
    {"nome": "Bearing1_3", "condicao": 1, "set": "Full_Test_Set"},
    {"nome": "Bearing1_4", "condicao": 1, "set": "Full_Test_Set"},
    {"nome": "Bearing1_5", "condicao": 1, "set": "Full_Test_Set"},
    {"nome": "Bearing1_6", "condicao": 1, "set": "Full_Test_Set"},
    {"nome": "Bearing1_7", "condicao": 1, "set": "Full_Test_Set"},
    {"nome": "Bearing2_3", "condicao": 2, "set": "Full_Test_Set"},
    {"nome": "Bearing2_4", "condicao": 2, "set": "Full_Test_Set"},
    {"nome": "Bearing2_5", "condicao": 2, "set": "Full_Test_Set"},
    {"nome": "Bearing2_6", "condicao": 2, "set": "Full_Test_Set"},
    {"nome": "Bearing2_7", "condicao": 2, "set": "Full_Test_Set"},
    {"nome": "Bearing3_3", "condicao": 3, "set": "Full_Test_Set"},
]

# Definimos 1 unico modo global para aproveitar a estrutura anterior
MODOS = [
    {
        "id": "pronostia_all", 
        "nome": "Rolamento (PRONOSTIA)",
        "banda": (10, 10000), # banda ampla
    }
]

# Modos usados no modelo de sistema do passo 6.
MODO_SISTEMA_MOTOR = "pronostia_all"
MODO_SISTEMA_BOMBA = "pronostia_all"

# tempo de missao (horas) para avaliar R do sistema no passo 6
TEMPO_MISSAO = 2.0  # os rolamentos falham em ~1 a 7 horas, entao missao de 2h eh ok.
