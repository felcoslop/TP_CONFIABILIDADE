# Análise de Confiabilidade de um Conjunto Motor-Bomba Centrífuga

Trabalho final da disciplina **EEE017 — Confiabilidade de Sistemas** (UFMG, Prof. Michel Bessani).

**Autores:**
- Stéphanie Pereira Barbosa — 2021088965
- Isabella Beatriz de Souza Gomes — 2022421587
- Felipe Costa Lopes — 2018019648

**Documento final:** [`latex/Documento_Final_EEE017.pdf`](latex/Documento_Final_EEE017.pdf)  
**Proposta:** [`latex/Proposta_EEE017.pdf`](latex/Proposta_EEE017.pdf)

---

## 1. Visão Geral

O trabalho responde, do ponto de vista da confiabilidade: dado um modo de falha em
desenvolvimento, qual a distribuição do tempo até a falha funcional do equipamento?
E quanto a configuração do sistema altera sua disponibilidade?

O pipeline em Python:

1. extrai um indicador de degradação dos sinais de vibração (RMS em banda);
2. constrói séries de tempo até a falha (TTF) por modelo de degradação exponencial;
3. ajusta distribuições de vida (Exponencial, Weibull, Lognormal) com censura à direita;
4. estima intervalos de confiança dos parâmetros por bootstrap não paramétrico;
5. calcula MTTF, R(t), taxa de falha h(t) e disponibilidade A;
6. modela o sistema (DBC motor em série com bomba) e simula série, paralelo e standby por Monte Carlo.

---

## 2. Dataset

Dataset público **Motor Current and Vibration Monitoring Dataset for various Faults in an
E-motor-driven Centrifugal Pump** (Bruinsma et al., 2024) [[1]](#referências), armazenado em
`data/dataset_bruinsma2024/`. Licença CC0.

São sinais de vibração (5 acelerômetros Wilcoxon 786B-10, 20 kHz) de duas bancadas
motor-bomba com falhas induzidas em múltiplos níveis de severidade. Cada arquivo CSV
contém `time` + colunas `0..N`, onde cada coluna é uma repetição independente da mesma
condição.

**Importante:** o dataset é de *snapshots* de condição (não *run-to-failure*). A ponte
para a análise de confiabilidade é feita via modelo de degradação — veja a Seção 4.

---

## 3. Modos de Falha Analisados

| Modo | Subsistema | Canal | Banda |
|---|---|---|---|
| Rolamento — pista interna (BPFI) | motor | ch1 | 1–9 kHz |
| Desbalanceamento no motor | motor | ch2 | 10–200 Hz |
| Desbalanceamento na bomba | bomba | ch5 | 10–200 Hz |
| Desalinhamento paralelo | bomba | ch1 | 10–300 Hz |

A banda foi escolhida pela física da falha e validada por correlação de Spearman
com a severidade. BPFO e desalinhamento angular foram avaliados e descartados
(assinatura não separável do baseline).

---

## 4. Metodologia Resumida

### Indicador de degradação
RMS do sinal de vibração em banda de frequência via densidade espectral de Welch [[1]](#referências).
Banda alta (1–9 kHz) para rolamento (impactos); banda baixa (10–300 Hz) para
desbalanceamento e desalinhamento (harmônicos 1× e 2×).

### Construção do TTF — modelo de degradação
Baseado na abordagem de Meeker e Escobar [[3]](#referências): a degradação é modelada como
D(τ) = D₀ · exp(ρτ), com taxa média ρ̄ calibrada nos dados (baseline → severidade máxima).
Cada unidade simulada recebe taxa aleatória ρ = ρ̄ · exp(N(0, c)), injetando
variabilidade operacional. Falha quando D cruza o limiar L = μ₀ + 0,5 · (D_max − μ₀).
Unidades que não cruzam até o horizonte viram dados **censurados à direita** [[4]](#referências).

### Ajuste de distribuições
Exponencial, Weibull-2P e Lognormal ajustadas por máxima verossimilhança com censura [[4]](#referências),
seleção por AICc, verificação por Kolmogorov-Smirnov, pontos empíricos por median ranks
de Benard. Implementado com a biblioteca `reliability` [[8]](#referências).

### Bootstrap
IC 95% dos parâmetros por bootstrap não paramétrico com R = 10⁴ reamostragens,
preservando o status de censura de cada observação [[6]](#referências).

### Índices e sistema
MTTF, R(t), h(t), A = MTTF/(MTTF + MTTR = 24 h). Sistema motor+bomba em série;
Monte Carlo (t = F⁻¹(U)) para série, paralelo e standby, verificados pelas expressões
analíticas de disponibilidade [[7]](#referências).

---

## 5. Estrutura do Repositório

```
confiabilidade/
├── README.md                        ← este arquivo
├── code/
│   ├── config.py                    # caminhos, modos, constantes, MODO_RAPIDO
│   ├── utils.py                     # leitura de sinal, RMS de banda, median rank
│   ├── extrair_features.py          # passo 1: sinais -> features.csv
│   ├── construir_ttf.py             # passo 2: features -> ttf.csv
│   ├── ajustar_distribuicoes.py     # passo 3: Exp/Weibull/Lognormal
│   ├── bootstrap_ic.py              # passo 4: IC bootstrap
│   ├── indices.py                   # passo 5: MTTF, R(t), h(t), A
│   ├── sistema.py                   # passo 6: DBC + Monte Carlo
│   ├── graficos.py                  # plotagem (backend Agg)
│   ├── main.py                      # orquestra os 6 passos
│   ├── construir_dataset_tiny.py    # gera data/database_tiny/ a partir do completo
│   ├── requirements.txt
│   └── resultados/
│       ├── figuras/                 # 34 PNGs gerados
│       └── tabelas/                 # 6 CSVs com resultados numéricos
├── data/
│   ├── dataset_bruinsma2024/        # dataset original (CSVs ~80 GB, excluídos do repo)
│   └── database_tiny/               # 28 arquivos usados no trabalho (~4,4 GB, baixar via README)
└── latex/
    ├── Documento_Final_EEE017.pdf
    ├── Documento_Final_EEE017.tex
    ├── Proposta_EEE017.pdf
    └── Proposta_EEE017.tex
```

---

## 6. Como Executar

### 6.1 Pré-requisitos

```bash
pip install -r code/requirements.txt
```

Pacotes: `numpy`, `scipy`, `pandas`, `matplotlib`, `reliability`, `openpyxl`.

### 6.2 Obter os dados

**Opção A — Dataset reduzido (~4,4 GB, recomendado)**

Baixe a pasta `Vibration/` pelo link no [`data/database_tiny/README.md`](data/database_tiny/README.md)
e extraia em `data/database_tiny/`. Ou gere a partir do dataset completo:

```bash
python code/construir_dataset_tiny.py
```

Em `code/config.py`, confirme:
```python
USAR_DATASET_TINY = True
```

**Opção B — Dataset completo (~80 GB)**

Baixe de [4TU.ResearchData](https://doi.org/10.4121/2b61183e-c14f-4131-829b-cc4822c369d0) [[1]](#referências)
e extraia em `data/dataset_bruinsma2024/`. Em `code/config.py`:
```python
USAR_DATASET_TINY = False
```

### 6.3 Rodar o pipeline completo

```bash
python code/main.py
```

Controle de velocidade em `code/config.py`:

```python
MODO_RAPIDO = True   # ~1,5 s por arquivo — roda em ~30 s (validação)
MODO_RAPIDO = False  # arquivo inteiro   — roda em ~4 min (resultados finais)
```

### 6.4 Rodar passos individualmente

```bash
python code/extrair_features.py      # passo 1 (lento — lê os CSVs)
python code/construir_ttf.py         # passo 2
python code/ajustar_distribuicoes.py # passo 3
python code/bootstrap_ic.py          # passo 4
python code/indices.py               # passo 5
python code/sistema.py               # passo 6
```

O passo 1 é o único caro. Os demais leem `features.csv` e são rápidos.

---

## 7. Principais Resultados

### Por modo de falha

| Modo | Melhor ajuste | MTTF [h] | β (Weibull) | IC 95% de β | Disponibilidade |
|---|---|---|---|---|---|
| Rolamento BPFI | Lognormal | 4857 | 3,82 | [3,54; 4,13] | 0,9951 |
| Desbalanceamento motor | Lognormal | 5997 | 0,98 | [0,95; 1,01] | 0,9960 |
| Desbalanceamento bomba | Lognormal | 1836 | 1,68 | [1,62; 1,74] | 0,9871 |
| Desalinhamento paralelo | Lognormal | 2831 | 2,92 | [2,83; 3,02] | 0,9916 |

β > 1 indica desgaste crescente (curva da banheira); β ≈ 1 indica taxa constante (vida útil).

### Sistema motor-bomba (missão de 2000 h)

| Configuração | A (analítico) | A (Monte Carlo) | R(2000 h) |
|---|---|---|---|
| Série — arranjo real | 0,98316 | 0,98325 | 0,191 |
| Paralelo — redundância ativa | 0,99972 | 0,99976 | 0,348 |
| Standby — reserva fria | 0,99970 | (analítico) | 0,642 |

A redundância reduz a indisponibilidade de ~1,7 % para ~0,03 %.

---

## 8. Premissas e Limitações

- Os TTF vêm de um modelo de degradação calibrado em *snapshots*, não de falhas
  observadas no tempo. O MTTF obtido é o **tempo até a falha funcional condicionado
  a um defeito já em desenvolvimento**, não o MTBF intrínseco do equipamento saudável.
- A análise cobre 4 modos representativos em uma velocidade cada.
- A disponibilidade do *standby* foi verificada apenas analiticamente.

---

## Referências

[1] S. Bruinsma, R. D. Geertsma, R. Loendersloot e T. Tinga, "Motor current and vibration
monitoring dataset for various faults in an E-motor-driven centrifugal pump,"
*Data in Brief*, vol. 52, art. 109987, fev. 2024.
DOI: [10.1016/j.dib.2023.109987](https://doi.org/10.1016/j.dib.2023.109987) —
Dataset: [10.4121/2b61183e-c14f-4131-829b-cc4822c369d0](https://doi.org/10.4121/2b61183e-c14f-4131-829b-cc4822c369d0)

[2] P. D. T. O'Connor e A. Kleyner, *Practical Reliability Engineering*, 5ª ed.
Chichester: Wiley, 2012.

[3] W. Q. Meeker e L. A. Escobar, *Statistical Methods for Reliability Data*.
New York: Wiley-Interscience, 1998.

[4] E. A. Colosimo e S. R. Giolo, *Análise de Sobrevivência Aplicada*, 1ª ed.
São Paulo: Blucher, 2006.

[5] ISO, "Mechanical vibration — Measurement and evaluation of machine vibration — Part 3,"
*ISO 20816-3:2022*, Geneva, 2022.

[6] C. P. Robert e G. Casella, *Introducing Monte Carlo Methods with R*.
New York: Springer, 2010.

[7] E. Zio, *The Monte Carlo Simulation Method for System Reliability and Risk Analysis*.
London: Springer, 2013.

[8] M. Reid, *reliability* — a Python library for reliability engineering, Zenodo, 2024.
DOI: [10.5281/zenodo.3938000](https://doi.org/10.5281/zenodo.3938000)

[9] M. Bessani, "Notas de aula e scripts da disciplina EEE017 — Confiabilidade de Sistemas,"
UFMG, Belo Horizonte, 2026.
