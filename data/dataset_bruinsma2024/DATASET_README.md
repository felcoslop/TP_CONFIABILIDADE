# Dataset: Motor Current and Vibration Monitoring for Faults in an E-motor-driven Centrifugal Pump

## Referência

**Artigo:** Bruinsma, S., Geertsma, R.D., Loendersloot, R., Tinga, T.
*"Motor Current and Vibration Monitoring Dataset for various Faults in an E-motor-driven Centrifugal Pump"*
Data in Brief, 2023. DOI: 10.1016/j.dib.2023.109453

**Instituições:** Royal Netherlands Navy, Netherlands Defence Academy, University of Twente

**Contato:** sj.bruinsma.01@mindef.nl

**Licença:** CC0 (Domínio Público — uso livre sem restrições)

---

## Visão Geral

Dataset experimental coletado no **Fieldlab Techport** contendo sinais de vibração e de corrente/tensão elétrica de um conjunto motor-bomba (motor elétrico + bomba centrífuga) operando em diversas condições de falha, com múltiplos níveis de severidade.

- **2 configurações de bancada** independentes (Motor-2 e Motor-4)
- **Total de arquivos CSV:** ~1.322
- **Total de diretórios:** 261
- **Espaço em disco (descomprimido):** ~90 GB
- **Taxa de amostragem:** 20 kHz (ambos os tipos de sensor)

---

## Estrutura de Pastas

```
.
├── DATASET_README.md              ← este arquivo
├── README.txt                     ← README original (inglês, resumido)
├── 1-s2.0-S235234092301017X-main (1).pdf   ← artigo científico completo
├── Appendices/
│   ├── Other/
│   │   ├── measurement_overview.xlsx      ← tabela com velocidade, vazão e pressão por falha
│   │   └── Datasheets/
│   │       ├── Motor_MG160MA_datasheet.pdf
│   │       ├── Motor_MG180MB_datasheet.pdf
│   │       ├── Pump_NK80-160_datasheet.pdf
│   │       └── Pump_NK80-250_datasheet.pdf
│   └── Reports/
│       ├── Alignment reports/
│       │   ├── Motor 2/   (18 PDFs de alinhamento a laser)
│       │   └── Motor 4/   (17 PDFs de alinhamento a laser)
│       └── Balance reports/
│           ├── Balance Impeller 1.pdf
│           ├── Balance Impeller 2.pdf
│           └── Balance Impeller 3.pdf
└── Dataset/
    └── Dataset/
        ├── Electric/
        │   ├── Motor-2/
        │   │   ├── 50/     ← velocidade 50 Hz (correspondente a ~1500 RPM)
        │   │   ├── 75/     ← velocidade 75 Hz
        │   │   └── 100/    ← velocidade 100 Hz
        │   └── Motor-4/
        │       └── 70/     ← velocidade 70 Hz (única velocidade testada)
        └── Vibration/
            ├── Motor-2/
            │   ├── 50/
            │   ├── 75/
            │   └── 100/
            └── Motor-4/
                └── 70/
```

> Cada subpasta de velocidade contém subpastas nomeadas pelo tipo e severidade da falha (ex: `bearing bpfi 1`, `healthy 1`, `cavitation discharge 3`).

---

## Configurações de Bancada

### Motor-2

| Propriedade | Valor |
|---|---|
| Motor | MG160MA |
| Bomba | NK80-160 |
| Velocidades testadas | 50 Hz, 75 Hz, 100 Hz |
| Nº de categorias de falha | 27 |
| Relatórios de alinhamento | 18 PDFs disponíveis |

### Motor-4

| Propriedade | Valor |
|---|---|
| Motor | MG180MB |
| Bomba | NK80-250 |
| Velocidades testadas | 70 Hz (única) |
| Nº de categorias de falha | 40 |
| Relatórios de alinhamento | 17 PDFs disponíveis |

---

## Catálogo de Falhas

### Motor-2 — Falhas (27 categorias)

| Categoria | Nome das Pastas | Descrição Física |
|---|---|---|
| **Saudável** | `healthy 1`, `healthy 2`, `healthy 3` | Operação normal — 3 repetições independentes |
| **Saudável com ruído** | `healthy noise` | Operação normal com ruído ambiental adicional |
| **Motor original** | `new motor` | Equipamento novo como referência de baseline |
| **Rolamento BPFI** | `bearing bpfi 1/2/3` | Falha na pista interna do rolamento (Ball Pass Frequency Inner race) — 3 níveis de severidade |
| **Rolamento BPFO** | `bearing bpfo 1/2/3` | Falha na pista externa do rolamento (Ball Pass Frequency Outer race) — 3 níveis de severidade |
| **Rolamento BSF** | `bearing bsf` | Falha no elemento rolante do rolamento (Ball Spin Frequency) |
| **Rolamento contaminado** | `bearing contaminated` | Rolamento com contaminação por partículas |
| **Rolamento da bomba** | `bearing pump 1/2/3` | Falha no rolamento do eixo da bomba — 3 níveis de severidade |
| **Barra de rotor quebrada** | `broken rotor bar` | Falha elétrica no rotor gaiola de esquilo |
| **Impulsor danificado** | `impeller 1/2/3` | Falha no impulsor da bomba centrífuga — 3 níveis de severidade |
| **Pé solto no motor** | `loose foot motor` | Parafuso de fixação do motor solto |
| **Pé solto na bomba** | `loose foot pump` | Parafuso de fixação da bomba solto |
| **Pé mole no motor** | `soft foot 1/2` | Desalinhamento estrutural por apoio irregular — 2 níveis |
| **Curto-circuito no estator** | `stator short 1/2` | Falha elétrica no enrolamento do estator — 2 níveis de severidade |

### Motor-4 — Falhas (40 categorias)

| Categoria | Nome das Pastas | Descrição Física |
|---|---|---|
| **Saudável** | `healthy 1`, `healthy 2`, `healthy 3` | Operação normal — 3 repetições independentes |
| **Saudável com ruído** | `healthy noise` | Operação normal com ruído ambiental adicional |
| **Desalinhamento angular** | `align angular 1/2/3/4/5` | Desalinhamento angular do eixo — 5 níveis de severidade |
| **Desalinhamento paralelo** | `align parallel 1/2/3/4` | Desalinhamento paralelo do eixo — 4 níveis de severidade |
| **Desalinhamento combinado** | `align combination 1/2/3/4` | Desalinhamento angular + paralelo — 4 níveis de severidade |
| **Eixo empenado** | `bent shaft` | Deformação permanente no eixo de transmissão |
| **Cavitação (descarga)** | `cavitation discharge 1/2/3/4/5` | Cavitação na saída da bomba — 5 níveis de severidade |
| **Cavitação (sucção)** | `cavitation suction 1/2/3/4` | Cavitação na entrada da bomba — 4 níveis de severidade |
| **Falha no acoplamento** | `coupling 1/2/3`, `coupling 2D` | Falha no acoplamento motor-bomba — 3 níveis + modo 2D |
| **Desbalanço no motor** | `unbalance motor 1/2/3/4/5/6` | Desbalanço do rotor do motor — 6 níveis de severidade |
| **Desbalanço na bomba** | `unbalance pump 1/2/3` | Desbalanço do impulsor da bomba — 3 níveis de severidade |

---

## Formato dos Arquivos CSV

### Dados Elétricos (Corrente e Tensão)

**Caminho:** `Dataset/Dataset/Electric/Motor-{X}/{rpm}/{falha}/`

**Arquivos por condição:** 6 arquivos (ch1 a ch6)

| Canal | Grandeza Física | Unidade |
|---|---|---|
| ch1 | Corrente — Fase 1 | Ampères (A) |
| ch2 | Corrente — Fase 2 | Ampères (A) |
| ch3 | Corrente — Fase 3 | Ampères (A) |
| ch4 | Tensão — Fase 1 | Volts (V) |
| ch5 | Tensão — Fase 2 | Volts (V) |
| ch6 | Tensão — Fase 3 | Volts (V) |

**Sensores:** 3× CR Magnetics CR3110 (garras de corrente) + 3× Wago 855 (pontos de tensão)

**Estrutura interna do CSV:**

```
time, 0, 1, 2, 3, ..., 29
5e-05, -11.707..., -6.299..., 2.327..., ...
0.0001, -11.457..., -7.131..., 1.665..., ...
```

- `time`: timestamp de início da janela (segundos), passo = 1/20000 s (50 µs)
- Colunas `0` a `29`: 30 amostras consecutivas do canal no domínio do tempo
- **Taxa de amostragem:** 20 kHz
- **Duração por medição:** 15 segundos (~300.000 amostras totais por canal)
- **Tamanho por arquivo:** ~160–167 MB

**Padrão de nomeação:**
```
Electric_Motor-{X}_{rpm}_time-{falha}-ch{N}.csv
Exemplo: Electric_Motor-2_50_time-healthy 1-ch1.csv
```

---

### Dados de Vibração (Acelerômetros)

**Caminho:** `Dataset/Dataset/Vibration/Motor-{X}/{rpm}/{falha}/`

**Arquivos por condição:** 5 arquivos (ch1 a ch5)

| Canal | Localização Física do Sensor | Direção |
|---|---|---|
| ch1 | Rolamento lado não-acionado do motor elétrico | Horizontal |
| ch2 | Rolamento lado acionado do motor elétrico | Vertical |
| ch3 | Rolamento lado acionado do motor elétrico | Axial |
| ch4 | Rolamento lado acionado da bomba | Horizontal |
| ch5 | Rolamento lado não-acionado da bomba | Vertical |

**Sensor:** Wilcoxon 786B-10 (acelerômetro piezoelétrico uniaxial, 100 mV/g)

**Estrutura interna do CSV:**

```
time, 0, 1, 2, 3, ..., 54
5e-05, -0.274..., -0.055..., 0.128..., ...
0.0001, 0.212..., -0.080..., -0.185..., ...
```

- `time`: timestamp de início da janela (segundos), passo = 1/20000 s (50 µs)
- Colunas `0` a `54`: 55 amostras consecutivas do canal no domínio do tempo
- **Taxa de amostragem:** 20 kHz
- **Duração por medição:** 12 segundos (~240.000 amostras totais por canal)
- **Unidade:** aceleração em *g* (gravidade)
- **Tamanho por arquivo:** ~265–290 MB

**Padrão de nomeação:**
```
Vibration_Motor-{X}_{rpm}_time-{falha}-ch{N}.csv
Exemplo: Vibration_Motor-2_50_time-healthy 1-ch1.csv
```

---

## Arquivos de Suporte

### `measurement_overview.xlsx`

Planilha com metadados operacionais de cada condição de falha:

| Coluna | Descrição |
|---|---|
| Velocidade do motor (Hz) | Frequência de operação do inversor |
| Vazão do fluido | Caudal medido na instalação hidráulica |
| Pressão de descarga | Pressão na saída da bomba |
| Nome da falha | Identificador da condição |

### Relatórios de Alinhamento (PDFs)

35 relatórios de alinhamento a laser (Motor-2: 18, Motor-4: 17) documentando o estado de alinhamento do eixo motor-bomba antes e após cada ensaio. Essenciais para validar as condições reais aplicadas nas medições de desalinhamento.

### Relatórios de Balanço (PDFs)

3 relatórios de balanceamento dinâmico dos impulsores (`Balance Impeller 1.pdf`, `2.pdf`, `3.pdf`) usados nos ensaios de desbalanço na bomba.

### Datasheets dos Equipamentos

| Arquivo | Equipamento |
|---|---|
| `Motor_MG160MA_datasheet.pdf` | Motor elétrico do Motor-2 |
| `Motor_MG180MB_datasheet.pdf` | Motor elétrico do Motor-4 |
| `Pump_NK80-160_datasheet.pdf` | Bomba centrífuga do Motor-2 |
| `Pump_NK80-250_datasheet.pdf` | Bomba centrífuga do Motor-4 |

---

## Estatísticas do Dataset

| Métrica | Valor |
|---|---|
| Total de arquivos | ~1.322 |
| Arquivos CSV (dados) | ~1.277 |
| Arquivos PDF (relatórios/artigo) | ~43 |
| Arquivo Excel (overview) | 1 |
| Condições de falha únicas — Motor-2 | 27 categorias × 3 velocidades = 81 condições |
| Condições de falha únicas — Motor-4 | 40 categorias × 1 velocidade = 40 condições |
| Canais elétricos por condição | 6 arquivos (3 correntes + 3 tensões) |
| Canais de vibração por condição | 5 arquivos (5 acelerômetros) |

---

## Uso Recomendado para Machine Learning

### Carregamento de um canal específico

```python
import pandas as pd

# Exemplo: corrente fase 1, Motor-2, 50 Hz, condição saudável
caminho = r"Dataset\Dataset\Electric\Motor-2\50\healthy 1\Electric_Motor-2_50_time-healthy 1-ch1.csv"
df = pd.read_csv(caminho)

# Colunas: 'time' + colunas '0' a '29' (dados de corrente em Ampères)
# Cada linha = janela temporal com 30 amostras consecutivas a 20 kHz
```

### Estratégia de rótulos

Para classificação de falhas, o rótulo é derivado diretamente do caminho da pasta:

```python
import os

def extrair_rotulo(caminho_arquivo):
    partes = caminho_arquivo.replace("\\", "/").split("/")
    # Estrutura: .../Motor-{X}/{rpm}/{FALHA}/arquivo.csv
    return partes[-2]  # ex: "bearing bpfi 1", "healthy 1", "cavitation discharge 3"
```

### Correspondência entre canais elétricos e físicos

```python
mapeamento_eletrico = {
    "ch1": "corrente_fase_1_A",
    "ch2": "corrente_fase_2_A",
    "ch3": "corrente_fase_3_A",
    "ch4": "tensao_fase_1_V",
    "ch5": "tensao_fase_2_V",
    "ch6": "tensao_fase_3_V",
}

mapeamento_vibracao = {
    "ch1": "motor_nde_horizontal_g",
    "ch2": "motor_de_vertical_g",
    "ch3": "motor_de_axial_g",
    "ch4": "bomba_de_horizontal_g",
    "ch5": "bomba_nde_vertical_g",
}
# NDE = Non-Driven End | DE = Driven End
```

---

## Notas Importantes

1. **Segmentação por janela:** Os CSVs armazenam os dados em formato de janela deslizante — cada linha representa um instante `time` com as N colunas seguintes (0 a 29 para elétrico; 0 a 54 para vibração) sendo as N amostras da série temporal naquele intervalo.

2. **Arquivos separados por canal:** Cada canal físico (corrente/tensão/acelerômetro) está em um arquivo CSV distinto. Para análise multicanal é necessário mesclar os arquivos pela coluna `time`.

3. **Tamanho dos arquivos:** Cada arquivo CSV ocupa entre 160 MB e 290 MB. Para datasets de treinamento em ML, considere converter para formato binário (Parquet, HDF5) para performance.

4. **Sincronização temporal:** A coluna `time` usa o mesmo epoch de referência dentro de cada condição de falha, permitindo alinhamento entre canais elétrico e vibração para análise fusão de modalidades (data fusion).

5. **Consistência entre Motor-2 e Motor-4:** As duas bancadas possuem conjuntos de falhas complementares (não idênticos). Motor-2 foca em falhas mecânicas de rolamento e elétricas; Motor-4 foca em desalinhamento, cavitação e desbalanço.

---

## Citação

```bibtex
@article{bruinsma2023motor,
  title   = {Motor Current and Vibration Monitoring Dataset for various Faults 
             in an E-motor-driven Centrifugal Pump},
  author  = {Bruinsma, S. and Geertsma, R.D. and Loendersloot, R. and Tinga, T.},
  journal = {Data in Brief},
  year    = {2023},
  doi     = {10.1016/j.dib.2023.109453},
  note    = {License: CC0}
}
```
