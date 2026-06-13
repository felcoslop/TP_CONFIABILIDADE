# IEEE PHM 2012 Data Challenge — PRONOSTIA Bearing Run-to-Failure Dataset

---

## ⚙️ Como obter os dados (setup obrigatório)

As pastas de dados **não estão no Git** (são grandes e estouram o limite do GitHub).
Elas estão ignoradas no `.gitignore` do projeto:

```
data/dataset_full/ieee-phm-2012-data-challenge-dataset-master/Learning_set/
data/dataset_full/ieee-phm-2012-data-challenge-dataset-master/Test_set/
data/dataset_full/ieee-phm-2012-data-challenge-dataset-master/Full_Test_Set/
```

Para rodar o pipeline (`python code/main.py`) é preciso baixar e posicionar os dados:

1. **Baixar** o `.zip` do Kaggle:
   **https://www.kaggle.com/datasets/alanhabrony/ieee-phm-2012-data-challenge**

2. **Extrair** o `.zip`. Ele contém as três pastas: `Learning_set`, `Test_set` e `Full_Test_Set`.

3. **Colar** as três pastas **dentro desta pasta**
   (`ieee-phm-2012-data-challenge-dataset-master/`), de modo que o caminho final fique
   **exatamente** assim:

```
confiabilidade/
└── data/
    └── dataset_full/
        └── ieee-phm-2012-data-challenge-dataset-master/
            ├── README.md                       ← este arquivo
            ├── DATASET_README.md               ← documentação detalhada
            ├── IEEEPHM2012-Challenge-Details.pdf
            ├── Learning_set/                    ← COLAR AQUI
            │   ├── Bearing1_1/
            │   │   ├── acc_00001.csv
            │   │   └── ...
            │   └── ...
            ├── Test_set/                        ← COLAR AQUI
            │   └── ...
            └── Full_Test_Set/                   ← COLAR AQUI
                ├── Bearing1_3/
                │   └── ...
                └── ...
```

> **Atenção:** não crie um nível extra (ex.: `Learning_set/Learning_set/...`). Logo abaixo de
> `Learning_set/` já devem aparecer as pastas `Bearing1_1`, `Bearing1_2`, etc. O `code/config.py`
> aponta para `data/dataset_full/ieee-phm-2012-data-challenge-dataset-master`.

---

**Authors:** P. Nectoux, R. Gouriveau, K. Medjaher, E. Ramasso, B. Morello, N. Zerhouni, C. Varnier
**Institution:** FEMTO-ST Institute, AS2M Department — Besançon, France
**Organizers:** IEEE Reliability Society and FEMTO-ST Institute (IEEE PHM 2012 Prognostic Challenge)
**Contact:** ieee-2012-PHM-challenge@femto-st.fr
**License:** Publicly available for research; citation of Nectoux et al. (2012) is required (see Citation)

## Introduction

This dataset contains experimental vibration and temperature data of rolling-element bearings
run to failure, acquired on the PRONOSTIA platform built at the AS2M department of the FEMTO-ST
Institute. It was released for the IEEE PHM 2012 Prognostic Challenge, whose goal was the
estimation of the Remaining Useful Life (RUL) of bearings.

The bearings were not seeded with artificial defects. Instead, a radial load exceeding the
bearing's maximum dynamic load was applied so that the components degrade naturally; each
failed bearing therefore tends to contain several concurrent defect types (balls, rings and cage).
Tests were stopped for safety once the vibration amplitude exceeded 20 g, which also defines
the end of life (and the RUL reference) used in the challenge.

The data are organised by measurement set (learning / test), then by bearing. Each bearing
folder holds one CSV file per acquisition snapshot. Vibration files are named `acc_xxxxx.csv`
and temperature files are named `temp_xxxxx.csv`.

> A total of 17 run-to-failure experiments are provided: 6 in the learning set and 11 in the
> test set, spread across three operating conditions. The bundled `IEEEPHM2012-Challenge-Details.pdf`
> contains the full description of the platform and the challenge.

## Data Explanation

### Operating Conditions

Three constant operating conditions (rotating speed and radial load) were used:

| Condition | Speed (rpm) | Radial load (N) | Bearings |
|-----------|-------------|-----------------|----------|
| 1 | 1800 | 4000 | Bearing1_1 … Bearing1_7 |
| 2 | 1650 | 4200 | Bearing2_1 … Bearing2_7 |
| 3 | 1500 | 5000 | Bearing3_1 … Bearing3_3 |

### Vibration Data

Acquired with two miniature DYTRAN 3035B (100 mV/g) accelerometers placed at 90° to each other,
radially on the outer race of the test bearing:

| Channel | Axis | Direction |
|---------|------|-----------|
| Horizontal accelerometer | X | Horizontal |
| Vertical accelerometer | Y | Vertical |

- **Sample rate:** 25.6 kHz
- **Snapshot:** 2560 samples (i.e. 1/10 s) recorded every 10 s
- **Units:** acceleration in g

### Temperature Data

Acquired with a platinum RTD PT100 (class 1/3 DIN) probe placed in a hole close to the outer ring:

- **Sample rate:** 10 Hz
- **Snapshot:** 600 samples recorded every minute
- **Units:** temperature from the RTD sensor

### CSV File Format

Each `acc_xxxxx.csv` row contains six fields; each `temp_xxxxx.csv` row contains five fields:

| File | Col 1 | Col 2 | Col 3 | Col 4 | Col 5 | Col 6 |
|------|-------|-------|-------|-------|-------|-------|
| `acc_xxxxx.csv` | Hour | Minute | Second | µ-second | Horizontal accel. | Vertical accel. |
| `temp_xxxxx.csv` | Hour | Minute | Second | 0.x second | RTD temperature | — |

Note: some bearings were recorded with vibration only (2 channels) and have no `temp_*` files.

## Dataset Location

The raw CSV files are stored under `Full_Test_Set/`, `Learning_set/` and `Test_set/`
(not included in this repository due to size). The `Test_set` holds the truncated data exactly
as given to challenge participants; the `Full_Test_Set` holds the complete run-to-failure
records (truncated portion plus the hidden remainder up to failure).

Original source and citation:

- **Reference paper (open access):** [hal-00719503](https://hal.science/hal-00719503)
- **Distribution mirror:** [Kaggle — IEEE PHM 2012 Data Challenge](https://www.kaggle.com/datasets/alanhabrony/ieee-phm-2012-data-challenge)
- **Original host (offline):** FEMTO-ST Institute, AS2M / PHM group

For detailed documentation of the full dataset structure, operating conditions, sensor
specifications and CSV format, see [`DATASET_README.md`](DATASET_README.md).

## Citation

```bibtex
@inproceedings{nectoux2012pronostia,
  title     = {{PRONOSTIA}: An Experimental Platform for Bearings Accelerated Life Test},
  author    = {Nectoux, Patrick and Gouriveau, Rafael and Medjaher, Kamal and
               Ramasso, Emmanuel and Morello, Brigitte and Zerhouni, Noureddine and
               Varnier, Christophe},
  booktitle = {IEEE International Conference on Prognostics and Health Management (PHM'12)},
  address   = {Denver, CO, USA},
  pages     = {1--8},
  year      = {2012}
}
```
