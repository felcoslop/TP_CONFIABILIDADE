# -*- coding: utf-8 -*-
"""
Configuracao central do trabalho de confiabilidade.
Aqui ficam os caminhos, a lista de modos de falha e as constantes do modelo.
Mexer so aqui pra mudar o comportamento de tudo.
"""
import os

# =============================================================================
# Caminhos
# =============================================================================
# pasta deste arquivo (code/)
RAIZ = os.path.dirname(os.path.abspath(__file__))

# --- Qual dataset usar? ---
# True  -> database_tiny (~4,4 GB, so os 28 arquivos do trabalho final)
#          Gere com: python construir_dataset_tiny.py
# False -> dataset original completo (~80 GB)
USAR_DATASET_TINY = True

# pasta com os CSVs de vibracao
if USAR_DATASET_TINY:
    # o tiny ja tem "Vibration/" como raiz direto
    _BASE_DATA = os.path.join(RAIZ, "..", "data", "database_tiny")
else:
    # o original tem dois niveis extras (Dataset/Dataset/)
    _BASE_DATA = os.path.join(
        RAIZ, "..", "data",
        "dataset_bruinsma2024", "Dataset", "Dataset")

DATASET = _BASE_DATA

# pastas de saida
SAIDA_FIG = os.path.join(RAIZ, "resultados", "figuras")
SAIDA_TAB = os.path.join(RAIZ, "resultados", "tabelas")

# =============================================================================
# Modo de execucao
# =============================================================================
# True  -> le so um trecho de cada CSV (rapido, pra validar o pipeline)
# False -> le o CSV inteiro (base toda, mais lento)
MODO_RAPIDO = False

# numero de linhas lidas por CSV no modo rapido (cada linha = 1/20000 s)
# 30000 linhas = 1,5 s de sinal, suficiente pra um RMS estavel
NROWS_RAPIDO = 30000

FS = 20000.0  # taxa de amostragem dos sensores (Hz), informada no README do dataset

# =============================================================================
# Constantes do modelo de degradacao -> TTF
# =============================================================================
# Cada nivel de severidade equivale a este tempo de operacao acumulada (horas).
# E uma hipotese de modelagem (o dataset nao tem eixo de tempo real); ela apenas
# fixa a escala de tempo dos indices. Mudar aqui reescalona MTTF, eta, etc.
HORAS_POR_NIVEL = 1000.0

# Variabilidade unidade-a-unidade da taxa de degradacao (coef. de variacao do
# log da taxa). Representa a dispersao operacional/de fabricacao que gera a
# distribuicao de vida. 0.4 = 40%.
COV_TAXA = 0.4

# Limiar de falha L = baseline + FRAC_LIMIAR * (degradacao_max - baseline).
# 0.5 coloca o limiar no meio do caminho ate a severidade maxima, gerando uma
# mistura saudavel de falhas e censuras.
FRAC_LIMIAR = 0.5

# numero de unidades simuladas por modo de falha (Monte Carlo da construcao do TTF)
N_UNIDADES = 500 if MODO_RAPIDO else 2000

# numero de reamostragens do bootstrap (IC dos parametros)
R_BOOTSTRAP = 2000 if MODO_RAPIDO else 10000

# numero de iteracoes do Monte Carlo do sistema (passo 6)
N_MC_SISTEMA = 10000 if MODO_RAPIDO else 100000

# tempo de reparo medio (MTTR) por subsistema, em horas. Usado na disponibilidade.
# Valor de engenharia (troca de rolamento/balanceamento ~ 1 a 2 turnos).
MTTR_HORAS = 24.0

SEMENTE = 42  # semente dos geradores aleatorios (reprodutibilidade)

# =============================================================================
# Modos de falha analisados
# =============================================================================
# Cada modo define:
#   id          - nome curto pra arquivos
#   nome        - rotulo bonito pros graficos
#   motor, vel  - bancada e velocidade (pasta do dataset)
#   canal       - canal do acelerometro (ch1..ch5) escolhido por fisica/Spearman
#   banda       - (fmin, fmax) Hz do indicador de degradacao
#   subsistema  - 'motor' ou 'bomba' (pro modelo de sistema do passo 6)
#   healthy     - pastas de referencia saudavel
#   severidades - pastas de severidade crescente
#
# Bandas: rolamento usa banda ALTA (1-9 kHz, impactos); desbalanceamento e
# desalinhamento usam banda BAIXA (harmonicos 1x/2x).
MODOS = [
    {
        "id": "bpfi", "nome": "Rolamento - pista interna (BPFI)",
        "motor": 2, "vel": 75, "canal": 1, "banda": (1000, 9000),
        "subsistema": "motor",
        "healthy": ["healthy 1", "healthy 2", "healthy 3"],
        "severidades": ["bearing bpfi 1", "bearing bpfi 2", "bearing bpfi 3"],
    },
    # OBS: BPFO (pista externa) e desalinhamento angular foram avaliados mas
    # descartados: a assinatura em band-RMS desses dois modos, nos canais
    # instrumentados, ficou DENTRO da variabilidade da condicao saudavel
    # (crescimento < 1, nao separavel). Rolamento fica representado pela BPFI e
    # desalinhamento pelo paralelo. Para reativar, descomente o bloco abaixo.
    # {
    #     "id": "bpfo", "nome": "Rolamento - pista externa (BPFO)",
    #     "motor": 2, "vel": 75, "canal": 2, "banda": (1000, 9000),
    #     "subsistema": "motor",
    #     "healthy": ["healthy 1", "healthy 2", "healthy 3"],
    #     "severidades": ["bearing bpfo 1", "bearing bpfo 2", "bearing bpfo 3"],
    # },
    {
        "id": "unbal_motor", "nome": "Desbalanceamento no motor",
        "motor": 4, "vel": 70, "canal": 2, "banda": (10, 200),
        "subsistema": "motor",
        "healthy": ["healthy 1", "healthy 2", "healthy 3"],
        "severidades": ["unbalance motor %d" % i for i in range(1, 7)],
    },
    {
        "id": "unbal_pump", "nome": "Desbalanceamento na bomba",
        "motor": 4, "vel": 70, "canal": 5, "banda": (10, 200),
        "subsistema": "bomba",
        "healthy": ["healthy 1", "healthy 2", "healthy 3"],
        "severidades": ["unbalance pump %d" % i for i in range(1, 4)],
    },
    {
        "id": "align_par", "nome": "Desalinhamento paralelo",
        "motor": 4, "vel": 70, "canal": 1, "banda": (10, 300),
        "subsistema": "bomba",
        "healthy": ["healthy 1", "healthy 2", "healthy 3"],
        "severidades": ["align parallel %d" % i for i in range(1, 5)],
    },
]

# Modos usados no modelo de sistema do passo 6 (um do motor, um da bomba).
MODO_SISTEMA_MOTOR = "unbal_motor"
MODO_SISTEMA_BOMBA = "unbal_pump"

# tempo de missao (horas) para avaliar R do sistema no passo 6
TEMPO_MISSAO = 2000.0
