# DATASET_README — Subconjunto database_tiny

Documentação detalhada do subconjunto de dados utilizado no trabalho final da
disciplina **EEE017 — Confiabilidade de Sistemas** (UFMG, Prof. Michel Bessani).

---

## 1. Origem e Licença

| Campo | Valor |
|---|---|
| Dataset original | *Motor Current and Vibration Monitoring Dataset for various Faults in an E-motor-driven Centrifugal Pump* |
| Autores | S. Bruinsma, R.D. Geertsma, R. Loendersloot, T. Tinga |
| Instituições | Royal Netherlands Navy · Netherlands Defence Academy · University of Twente |
| Publicação | *Data in Brief*, vol. 52, art. 109987, fev. 2024 |
| DOI artigo | [10.1016/j.dib.2023.109987](https://doi.org/10.1016/j.dib.2023.109987) |
| DOI dataset | [10.4121/2b61183e-c14f-4131-829b-cc4822c369d0](https://doi.org/10.4121/2b61183e-c14f-4131-829b-cc4822c369d0) |
| Licença | **CC0** — Domínio Público (uso livre, sem restrições) |

---

## 2. O que é o database_tiny

O dataset original ocupa **~80 GB** e contém 1.277 arquivos CSV cobrindo 67 categorias
de falha em duas bancadas motor-bomba. Para este trabalho foram necessários apenas
**28 arquivos** (4 modos de falha × canal único por modo), totalizando **~4,4 GB**.

| Métrica | Valor |
|---|---|
| Arquivos no dataset original | ~1.277 CSVs |
| Arquivos neste subconjunto | 28 CSVs |
| Tamanho original | ~80 GB |
| Tamanho do subconjunto | ~4,4 GB |
| Redução | ~94,5% |

### Critério de Seleção

Para cada modo de falha, o canal do acelerômetro e a banda de frequência foram
escolhidos por análise empírica: calculou-se o RMS de vibração em diferentes bandas
para cada canal e verificou-se qual combinação produzia **correlação de Spearman ≥ 0,89**
entre o indicador e a severidade crescente da falha. Apenas combinações com indicador
monotonicamente crescente foram mantidas.

---

## 3. Arquivos Incluídos

### 3.1 Motor-2 — Velocidade 75 Hz — Canal ch1

**Falha:** Defeito na pista interna do rolamento (BPFI — Ball Pass Frequency Inner race)  
**Indicador:** RMS de vibração na banda **1–9 kHz** (impactos de alta frequência típicos de rolamento)  
**Acelerômetro ch1:** Mancal lado não-acionado do motor, direção horizontal

| Arquivo | Condição | Tipo |
|---|---|---|
| `Vibration_Motor-2_75_time-healthy 1-ch1.csv` | healthy 1 | baseline saudável — repetição 1 |
| `Vibration_Motor-2_75_time-healthy 2-ch1.csv` | healthy 2 | baseline saudável — repetição 2 |
| `Vibration_Motor-2_75_time-healthy 3-ch1.csv` | healthy 3 | baseline saudável — repetição 3 |
| `Vibration_Motor-2_75_time-bearing bpfi 1-ch1.csv` | bearing bpfi 1 | defeito BPFI — severidade 1 (mais leve) |
| `Vibration_Motor-2_75_time-bearing bpfi 2-ch1.csv` | bearing bpfi 2 | defeito BPFI — severidade 2 |
| `Vibration_Motor-2_75_time-bearing bpfi 3-ch1.csv` | bearing bpfi 3 | defeito BPFI — severidade 3 (mais severa) |

**Tamanho por arquivo:** healthy ~290 MB · bpfi ~74 MB  
**Crescimento do indicador:** baseline 0,43 g → severidade 3: 0,57 g (×1,34, Spearman = 1,00)

---

### 3.2 Motor-4 — Velocidade 70 Hz — Canal ch2

**Falha:** Desbalanceamento no rotor do motor  
**Indicador:** RMS de vibração na banda **10–200 Hz** (harmônicos 1× e 2× da rotação)  
**Acelerômetro ch2:** Mancal lado acionado do motor, direção vertical

| Arquivo | Condição | Tipo |
|---|---|---|
| `Vibration_Motor-4_70_time-healthy 1-ch2.csv` | healthy 1 | baseline saudável — repetição 1 |
| `Vibration_Motor-4_70_time-healthy 2-ch2.csv` | healthy 2 | baseline saudável — repetição 2 |
| `Vibration_Motor-4_70_time-healthy 3-ch2.csv` | healthy 3 | baseline saudável — repetição 3 |
| `Vibration_Motor-4_70_time-unbalance motor 1-ch2.csv` | unbalance motor 1 | desbalanceamento motor — severidade 1 |
| `Vibration_Motor-4_70_time-unbalance motor 2-ch2.csv` | unbalance motor 2 | desbalanceamento motor — severidade 2 |
| `Vibration_Motor-4_70_time-unbalance motor 3-ch2.csv` | unbalance motor 3 | desbalanceamento motor — severidade 3 |
| `Vibration_Motor-4_70_time-unbalance motor 4-ch2.csv` | unbalance motor 4 | desbalanceamento motor — severidade 4 |
| `Vibration_Motor-4_70_time-unbalance motor 5-ch2.csv` | unbalance motor 5 | desbalanceamento motor — severidade 5 |
| `Vibration_Motor-4_70_time-unbalance motor 6-ch2.csv` | unbalance motor 6 | desbalanceamento motor — severidade 6 (mais severa) |

**Tamanho por arquivo:** healthy ~290 MB · unbalance ~75 MB  
**Crescimento do indicador:** baseline 0,049 g → severidade 6: 0,095 g (×1,95, Spearman = 0,89)

---

### 3.3 Motor-4 — Velocidade 70 Hz — Canal ch5

**Falha:** Desbalanceamento no impulsor da bomba  
**Indicador:** RMS de vibração na banda **10–200 Hz**  
**Acelerômetro ch5:** Mancal lado não-acionado da bomba, direção vertical

| Arquivo | Condição | Tipo |
|---|---|---|
| `Vibration_Motor-4_70_time-healthy 1-ch5.csv` | healthy 1 | baseline saudável — repetição 1 |
| `Vibration_Motor-4_70_time-healthy 2-ch5.csv` | healthy 2 | baseline saudável — repetição 2 |
| `Vibration_Motor-4_70_time-healthy 3-ch5.csv` | healthy 3 | baseline saudável — repetição 3 |
| `Vibration_Motor-4_70_time-unbalance pump 1-ch5.csv` | unbalance pump 1 | desbalanceamento bomba — severidade 1 |
| `Vibration_Motor-4_70_time-unbalance pump 2-ch5.csv` | unbalance pump 2 | desbalanceamento bomba — severidade 2 |
| `Vibration_Motor-4_70_time-unbalance pump 3-ch5.csv` | unbalance pump 3 | desbalanceamento bomba — severidade 3 (mais severa) |

**Tamanho por arquivo:** healthy ~291 MB · unbalance pump 51–75 MB  
**Crescimento do indicador:** baseline 0,089 g → severidade 3: 0,104 g (×1,17, Spearman = 1,00)

---

### 3.4 Motor-4 — Velocidade 70 Hz — Canal ch1

**Falha:** Desalinhamento paralelo do eixo motor-bomba  
**Indicador:** RMS de vibração na banda **10–300 Hz** (harmônicos de desalinhamento)  
**Acelerômetro ch1:** Mancal lado não-acionado do motor, direção horizontal

| Arquivo | Condição | Tipo |
|---|---|---|
| `Vibration_Motor-4_70_time-healthy 1-ch1.csv` | healthy 1 | baseline saudável — repetição 1 |
| `Vibration_Motor-4_70_time-healthy 2-ch1.csv` | healthy 2 | baseline saudável — repetição 2 |
| `Vibration_Motor-4_70_time-healthy 3-ch1.csv` | healthy 3 | baseline saudável — repetição 3 |
| `Vibration_Motor-4_70_time-align parallel 1-ch1.csv` | align parallel 1 | desalinhamento paralelo — severidade 1 |
| `Vibration_Motor-4_70_time-align parallel 2-ch1.csv` | align parallel 2 | desalinhamento paralelo — severidade 2 |
| `Vibration_Motor-4_70_time-align parallel 3-ch1.csv` | align parallel 3 | desalinhamento paralelo — severidade 3 |
| `Vibration_Motor-4_70_time-align parallel 4-ch1.csv` | align parallel 4 | desalinhamento paralelo — severidade 4 (mais severa) |

**Tamanho por arquivo:** healthy ~290 MB · align parallel 74–99 MB  
**Crescimento do indicador:** baseline 0,094 g → severidade 4: 0,308 g (×3,29, Spearman = 1,00)

---

## 4. Estrutura de Diretórios

```
database_tiny/
├── README.md              ← instruções de download
├── DATASET_README.md      ← este arquivo
└── Vibration/
    ├── Motor-2/
    │   └── 75/
    │       ├── healthy 1/
    │       │   └── Vibration_Motor-2_75_time-healthy 1-ch1.csv
    │       ├── healthy 2/  ...
    │       ├── healthy 3/  ...
    │       ├── bearing bpfi 1/
    │       │   └── Vibration_Motor-2_75_time-bearing bpfi 1-ch1.csv
    │       ├── bearing bpfi 2/  ...
    │       └── bearing bpfi 3/  ...
    └── Motor-4/
        └── 70/
            ├── healthy 1/   (ch1, ch2 e ch5 — compartilhado pelos 3 modos do Motor-4)
            ├── healthy 2/   ...
            ├── healthy 3/   ...
            ├── unbalance motor 1/ → unbalance motor 6/   (ch2)
            ├── unbalance pump 1/  → unbalance pump 3/    (ch5)
            └── align parallel 1/ → align parallel 4/    (ch1)
```

---

## 5. Formato dos Arquivos CSV

Cada arquivo contém dados de **um único canal** de vibração em **uma única condição**:

```
time, 0, 1, 2, 3, ..., 54
5e-05, -0.274, -0.055, 0.128, ...
0.0001,  0.212, -0.080, -0.185, ...
```

| Campo | Descrição |
|---|---|
| `time` | Instante de tempo (s), passo = 1/20.000 = 50 µs |
| colunas `0` a `54` | Cada coluna = uma **repetição independente** da mesma medição |
| Taxa de amostragem | 20 kHz |
| Duração por medição | 12 s → ~240.000 linhas por arquivo |
| Unidade | Aceleração em **g** (gravidade) |
| Repetições | Healthy: até 55 repetições · Falhas: 15–20 repetições |

### Por que múltiplas colunas?

O dataset original armazena cada canal como uma matriz **(tempo × repetições)**,
onde cada coluna representa uma execução independente do mesmo experimento. O código
do trabalho trata cada coluna como uma amostra estatisticamente independente da mesma
condição, aumentando o tamanho efetivo da amostra para o cálculo do RMS médio.

---

## 6. Modos Descartados (avaliados, não incluídos)

Os modos abaixo foram analisados mas descartados por não apresentarem indicador de
degradação separável da condição saudável nos canais disponíveis:

| Modo | Motivo do descarte |
|---|---|
| Rolamento BPFO (pista externa) | RMS de banda alta **menor** nas falhas que no saudável (crescimento < 1) |
| Desalinhamento angular | RMS de banda baixa nos canais testados ficou dentro da variabilidade do baseline |

Esses modos ficam disponíveis no dataset completo para análise futura com outras
features (kurtosis, envelope, etc.).

---

## 7. Configuração do Código

Para usar este subconjunto, em `code/config.py`:

```python
USAR_DATASET_TINY = True   # aponta para data/database_tiny/
MODO_RAPIDO = False        # lê o sinal inteiro (~4 min, resultados finais)
```

Para rodar:

```bash
python code/main.py
```
