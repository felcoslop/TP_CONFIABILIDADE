# Análise de Confiabilidade de Rolamentos sob Carga Acelerada (PRONOSTIA)

Trabalho final da disciplina **EEE017 — Confiabilidade de Sistemas** (UFMG, Prof. Michel Bessani).

**Autores:**
- Stéphanie Pereira Barbosa — 2021088965
- Isabella Beatriz de Souza Gomes — 2022421587
- Felipe Costa Lopes — 2018019648

**Documento final:** [`latex/Documento_Final_EEE017.pdf`](latex/Documento_Final_EEE017.pdf)
**Apresentação:** [`latex/apresentacao/apresentacao.pdf`](latex/apresentacao/apresentacao.pdf)

---

## 1. Visão Geral

O trabalho responde, do ponto de vista da confiabilidade: qual a distribuição do tempo
até a falha de um rolamento operando sob carga acelerada? E quanto a configuração do
sistema (uma unidade ou com redundância) altera sua disponibilidade?

O pipeline em Python, em 6 passos:

1. extrai um indicador de degradação (RMS de vibração em banda) de cada *snapshot*;
2. extrai o tempo até a falha (TTF) real de cada rolamento — *run-to-failure*, sem censura;
3. ajusta distribuições de vida (Exponencial, Weibull, Log-normal) por máxima verossimilhança;
4. estima intervalos de confiança dos parâmetros da Weibull por *bootstrap* não paramétrico;
5. calcula MTTF, confiabilidade R(t), taxa de falha h(t) e disponibilidade A;
6. modela um sistema (DBC com 2 rolamentos) e simula série, paralelo e *standby* por Monte Carlo.

---

## 2. Dataset

**IEEE PHM 2012 Data Challenge — Plataforma PRONOSTIA** (Nectoux et al., 2012)
[[1]](#referências), do Instituto FEMTO-ST.

A bancada aplica **carga radial extrema** a rolamentos de esferas, acelerando a fadiga
até a falha (*run-to-failure*). São **17 rolamentos** levados à falha, em **3 condições
de operação**:

| Rolamento | Condição | Rotação | Carga |
|---|---|---|---|
| `Bearing1_1` | 1 | 1800 RPM | 4000 N |
| `Bearing1_2` | 1 | 1800 RPM | 4000 N |
| `Bearing1_3` | 1 | 1800 RPM | 4000 N |
| `Bearing1_4` | 1 | 1800 RPM | 4000 N |
| `Bearing1_5` | 1 | 1800 RPM | 4000 N |
| `Bearing1_6` | 1 | 1800 RPM | 4000 N |
| `Bearing1_7` | 1 | 1800 RPM | 4000 N |
| `Bearing2_1` | 2 | 1650 RPM | 4200 N |
| `Bearing2_2` | 2 | 1650 RPM | 4200 N |
| `Bearing2_3` | 2 | 1650 RPM | 4200 N |
| `Bearing2_4` | 2 | 1650 RPM | 4200 N |
| `Bearing2_5` | 2 | 1650 RPM | 4200 N |
| `Bearing2_6` | 2 | 1650 RPM | 4200 N |
| `Bearing2_7` | 2 | 1650 RPM | 4200 N |
| `Bearing3_1` | 3 | 1500 RPM | 5000 N |
| `Bearing3_2` | 3 | 1500 RPM | 5000 N |
| `Bearing3_3` | 3 | 1500 RPM | 5000 N |

Vibração medida por 2 acelerômetros (horizontal e vertical, 25,6 kHz). Cada *snapshot*
tem 2.560 amostras (0,1 s), gravado a cada 10 s; o ensaio para quando a vibração
ultrapassa **20 g** (falha funcional). Usa-se a **aceleração horizontal**.

> **Os dados não estão no repositório** (são grandes). Baixe do Kaggle e posicione as
> pastas conforme
> [`data/dataset_full/ieee-phm-2012-data-challenge-dataset-master/README.md`](data/dataset_full/ieee-phm-2012-data-challenge-dataset-master/README.md).

**Por que PRONOSTIA é run-to-failure (e não *snapshots* de condição):** cada rolamento é
operado do estado são até a falha, então o TTF é **medido diretamente** (tempo do último
*snapshot*), sem necessidade de modelo de degradação nem censura.

---

## 3. Metodologia Resumida

### Indicador de degradação
RMS da vibração em **banda larga (10 Hz – 10 kHz)** via densidade espectral de Welch.
A fadiga gera impactos de banda larga cuja energia (RMS) cresce monotonicamente com a
degradação.

### Extração do TTF
O TTF de cada rolamento é o **tempo do seu último *snapshot*** (instante da falha,
vibração > 20 g). Todos os 17 são falhas confirmadas (**censura = 0**).

### Ajuste de distribuições
Exponencial (λ), Weibull-2P (β, η) e Log-normal (µ, σ) ajustadas por **máxima
verossimilhança** [[4]](#referências). Seleção pelo **AICc** (menor vence), verificação
por Kolmogorov-Smirnov, pontos empíricos por *median ranks* de Benard.

### Bootstrap
IC 95% de β e η por *bootstrap* não paramétrico com R = 10⁴ reamostragens
[[5]](#referências).

### Índices e sistema
MTTF, R(t) = exp(−(t/η)^β), h(t) e A = MTTF/(MTTF + MTTR), com MTTR = 24 h. Sistema
hipotético com 2 rolamentos; Monte Carlo (t = F⁻¹(U)) para série, paralelo e *standby*,
verificados pelas expressões analíticas de disponibilidade [[6]](#referências).

---

## 4. Estrutura do Repositório

```
confiabilidade/
├── README.md                        ← este arquivo
├── code/
│   ├── config.py                    # caminhos, 17 rolamentos, constantes, MODO_RAPIDO
│   ├── utils.py                     # leitura de snapshot, RMS de banda (Welch)
│   ├── extrair_features.py          # passo 1: snapshots -> features.csv
│   ├── construir_ttf.py             # passo 2: features -> ttf.csv (último snapshot)
│   ├── ajustar_distribuicoes.py     # passo 3: Exp/Weibull/Lognormal + AICc
│   ├── bootstrap_ic.py              # passo 4: IC bootstrap
│   ├── indices.py                   # passo 5: MTTF, R(t), h(t), A
│   ├── sistema.py                   # passo 6: DBC 2 rolamentos + Monte Carlo
│   ├── graficos.py                  # plotagem (backend Agg)
│   ├── main.py                      # orquestra os 6 passos
│   ├── requirements.txt
│   └── resultados/
│       ├── figuras/                 # PNGs gerados
│       └── tabelas/                 # CSVs com resultados numéricos
├── data/
│   └── dataset_full/ieee-phm-2012-data-challenge-dataset-master/
│       ├── README.md                # instruções de download (Kaggle)
│       ├── Learning_set/   Test_set/   Full_Test_Set/   (excluídos do repo)
└── latex/
    ├── Documento_Final_EEE017.tex / .pdf
    └── apresentacao/apresentacao.tex / .pdf
```

---

## 5. Como Executar

### 5.1 Pré-requisitos

```bash
pip install -r code/requirements.txt
```

Pacotes: `numpy`, `scipy`, `pandas`, `matplotlib`, `reliability`, `openpyxl`.

### 5.2 Obter os dados

Baixe do **Kaggle** e posicione as pastas (`Learning_set`, `Test_set`, `Full_Test_Set`)
seguindo o
[README do dataset](data/dataset_full/ieee-phm-2012-data-challenge-dataset-master/README.md).
O `code/config.py` aponta para
`data/dataset_full/ieee-phm-2012-data-challenge-dataset-master`.

### 5.3 Rodar o pipeline completo

```bash
python code/main.py
```

Controle de velocidade em `code/config.py`:

```python
MODO_RAPIDO = True   # lê 1 a cada 10 snapshots — rápido (validação)
MODO_RAPIDO = False  # lê todos os snapshots   — resultados finais
```

O passo 1 (extração de features) é o único caro (lê milhares de CSVs). Os demais leem a
`features.csv` e são rápidos.

---

## 6. Principais Resultados

### Distribuição de vida (17 rolamentos)

| Melhor ajuste | β (Weibull) | IC 95% de β | η [h] | MTTF [h] | Disponibilidade |
|---|---|---|---|---|---|
| Weibull | 1,80 | [1,39; 2,88] | ≈4,5 | ≈4,0 | 0,145 |

β > 1 ⇒ falha por **desgaste/fadiga** (taxa de falha crescente — região de desgaste da
curva da banheira).

### Sistema com 2 rolamentos (missão de 2 h)

| Configuração | A | R(2 h) |
|---|---|---|
| Série | 0,021 | 0,636 |
| Paralelo (ativo) | 0,042 | 0,869 |
| *Standby* (reserva fria) | 0,114 | 0,965 |

A ordenação **Standby > Paralelo > Série** é a esperada. MTTF do conjunto em série ≈ 3 h.

> **Observação:** MTTF e disponibilidade são baixos **por construção** — trata-se de um
> *Ensaio Acelerado de Vida* (carga colossal força a falha em horas), com MTTF da ordem
> do MTTR de 24 h. Os números validam a **metodologia**, não representam a vida de campo.

---

## Referências

[1] P. Nectoux, R. Gouriveau, K. Medjaher, E. Ramasso, B. Morello, N. Zerhouni e C. Varnier,
"PRONOSTIA: An experimental platform for bearings accelerated degradation tests,"
*IEEE Int. Conf. on Prognostics and Health Management (PHM'12)*, Denver, CO, 2012, pp. 1–8.
Dataset: [Kaggle — IEEE PHM 2012 Data Challenge](https://www.kaggle.com/datasets/alanhabrony/ieee-phm-2012-data-challenge).

[2] P. D. T. O'Connor e A. Kleyner, *Practical Reliability Engineering*, 5ª ed. Wiley, 2012.

[3] W. Q. Meeker e L. A. Escobar, *Statistical Methods for Reliability Data*. Wiley-Interscience, 1998.

[4] E. A. Colosimo e S. R. Giolo, *Análise de Sobrevivência Aplicada*, 1ª ed. Blucher, 2006.

[5] C. P. Robert e G. Casella, *Introducing Monte Carlo Methods with R*. Springer, 2010.

[6] E. Zio, *The Monte Carlo Simulation Method for System Reliability and Risk Analysis*. Springer, 2013.

[7] M. Reid, *reliability* — a Python library for reliability engineering, Zenodo, 2024.
DOI: [10.5281/zenodo.3938000](https://doi.org/10.5281/zenodo.3938000)

[8] M. Bessani, "Notas de aula e scripts da disciplina EEE017 — Confiabilidade de Sistemas," UFMG, 2026.
