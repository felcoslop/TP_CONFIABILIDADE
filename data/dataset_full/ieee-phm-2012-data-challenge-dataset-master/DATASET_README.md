# Dataset: IEEE PHM 2012 Data Challenge — PRONOSTIA Bearing Run-to-Failure

## Referência

**Artigo:** Nectoux, P., Gouriveau, R., Medjaher, K., Ramasso, E., Morello, B., Zerhouni, N., Varnier, C.
*"PRONOSTIA: An Experimental Platform for Bearings Accelerated Life Test"*
IEEE International Conference on Prognostics and Health Management (PHM'12), Denver, CO, USA, 2012, pp. 1–8.
HAL: hal-00719503 — https://hal.science/hal-00719503

**Instituição:** FEMTO-ST Institute, departamento AS2M — Besançon, França

**Organização do desafio:** IEEE Reliability Society e FEMTO-ST Institute (IEEE PHM 2012 Prognostic Challenge)

**Contato:** ieee-2012-PHM-challenge@femto-st.fr

**Licença:** Disponibilizado publicamente para pesquisa. Publicações que utilizem os dados devem
citar o artigo de Nectoux et al. (2012). A FEMTO-ST não associou uma licença formal (ex.: CC0/CC-BY);
o uso livre está condicionado à citação obrigatória.

---

## Visão Geral

Dataset experimental coletado na plataforma **PRONOSTIA** (FEMTO-ST, departamento AS2M), contendo
sinais de **vibração** e **temperatura** de rolamentos de esferas levados até a falha
(*run-to-failure*) sob carga radial acelerada. Foi disponibilizado para o **IEEE PHM 2012 Prognostic
Challenge**, cujo objetivo era a estimativa da **vida útil remanescente (RUL — Remaining Useful Life)**
dos rolamentos.

Características distintivas:

- **Degradação natural:** os rolamentos **não** recebem defeito artificial pré-induzido. Aplica-se
  uma carga radial superior à carga dinâmica máxima do rolamento (4000 N), de modo que a degradação
  ocorre naturalmente. Como consequência, um rolamento falho costuma conter **vários defeitos
  simultâneos** (esferas, pistas interna/externa e gaiola).
- **Critério de parada:** o ensaio é interrompido, por segurança, quando a amplitude de vibração
  ultrapassa **20 g**. Esse instante define o fim de vida (e a referência de RUL no desafio).
- **3 condições de operação** (velocidade de rotação e carga radial constantes por ensaio)
- **17 ensaios run-to-failure no total:** 6 de treinamento + 11 de teste
- **Duração dos ensaios:** de aproximadamente 1 h a 7 h (alta variabilidade)
- **Taxa de amostragem:** 25,6 kHz (vibração) e 10 Hz (temperatura)

Nesta cópia (redistribuição GitHub / [Kaggle](https://www.kaggle.com/datasets/alanhabrony/ieee-phm-2012-data-challenge)), o dataset acompanha o relatório oficial
`IEEEPHM2012-Challenge-Details.pdf`, que descreve em detalhe a plataforma, os sensores e o desafio.

---

## Estrutura de Pastas

```
.
├── IEEEPHM2012-Challenge-Details.pdf   ← relatório oficial do desafio (plataforma + sensores)
├── README.md                           ← README resumido (inglês)
├── DATASET_README.md                   ← este arquivo
│
├── Learning_set/                       ← conjunto de treinamento (6 rolamentos, run-to-failure completo)
│   ├── Bearing1_1/
│   ├── Bearing1_2/
│   ├── Bearing2_1/
│   ├── Bearing2_2/
│   ├── Bearing3_1/
│   └── Bearing3_2/
│
├── Test_set/                           ← conjunto de teste TRUNCADO (11 rolamentos, como no desafio)
│   ├── Bearing1_3/  ... Bearing1_7/
│   ├── Bearing2_3/  ... Bearing2_7/
│   └── Bearing3_3/
│
└── Full_Test_Set/                      ← conjunto de teste COMPLETO até a falha (11 rolamentos)
    ├── Bearing1_3/  ... Bearing1_7/
    ├── Bearing2_3/  ... Bearing2_7/
    └── Bearing3_3/
```

> Cada pasta de rolamento contém os arquivos CSV daquele ensaio: arquivos de vibração
> `acc_00001.csv`, `acc_00002.csv`, … e (quando disponíveis) arquivos de temperatura
> `temp_00001.csv`, `temp_00002.csv`, …

**Diferença entre `Test_set` e `Full_Test_Set`:** no desafio, os 11 rolamentos de teste foram
**truncados** (o participante recebia apenas o início da degradação e precisava prever o restante).
A pasta `Test_set` contém exatamente esses dados truncados; a pasta `Full_Test_Set` contém o ensaio
**completo até a falha** (a parte truncada **mais** o restante oculto). Exemplo de consistência:
para o `Bearing1_3`, o `Full_Test_Set` possui 2375 arquivos `acc` e o `Test_set` possui 1802;
a diferença (573 arquivos × 10 s) equivale a 5730 s, que é exatamente a RUL real publicada para
esse rolamento.

---

## A Plataforma PRONOSTIA

A PRONOSTIA é composta por três partes principais:

| Parte | Função | Detalhes |
|---|---|---|
| **Rotativa** | Aciona o eixo de suporte do rolamento | Motor assíncrono de 250 W com redutor; velocidade nominal do motor de 2830 rpm, mantendo o eixo secundário abaixo de 2000 rpm |
| **Carga (degradação)** | Aplica força radial no rolamento de teste | Atuador pneumático (cilindro) + braço de alavanca + sensor de força; carga até a carga dinâmica máxima do rolamento (4000 N), regulada por regulador eletro-pneumático digital |
| **Medição** | Aquisição dos sinais de saúde | 2 acelerômetros + 1 sonda de temperatura RTD; medidas operacionais (força, velocidade, torque) amostradas a 100 Hz |

---

## Condições de Operação

| Condição | Velocidade (rpm) | Carga radial (N) | Rolamentos |
|---|---|---|---|
| 1 | 1800 | 4000 | Bearing1_1 … Bearing1_7 |
| 2 | 1650 | 4200 | Bearing2_1 … Bearing2_7 |
| 3 | 1500 | 5000 | Bearing3_1 … Bearing3_3 |

Convenção de nomeação `BearingX_Y`: **X** é a condição de operação (1, 2 ou 3) e **Y** é o número
sequencial do ensaio dentro daquela condição.

---

## Conjunto de Treinamento (Learning Set) — 6 rolamentos

Dados de degradação completos (run-to-failure). A coluna **Arquivos** segue a contagem oficial do
desafio (soma de arquivos de vibração + temperatura); **Canais** = 3 indica vibração + temperatura,
= 2 indica somente vibração.

| Rolamento | Condição | Data do ensaio | Arquivos | Canais | Duração | Sinais |
|---|---|---|---|---|---|---|
| Bearing1_1 | 1 | 2010-12-01 | 3269 | 3 | 7h47m00s | vibração + temperatura |
| Bearing1_2 | 1 | 2011-04-06 | 1015 | 3 | 2h25m00s | vibração + temperatura |
| Bearing2_1 | 2 | 2011-05-06 | 1062 | 3 | 2h31m40s | vibração + temperatura |
| Bearing2_2 | 2 | 2011-06-17 | 797  | 2 | 2h12m40s | vibração |
| Bearing3_1 | 3 | 2011-04-07 | 604  | 3 | 1h25m40s | vibração + temperatura |
| Bearing3_2 | 3 | 2011-06-28 | 1637 | 2 | 4h32m40s | vibração |

---

## Conjunto de Teste (Test Set) — 11 rolamentos

Dados truncados no desafio. A coluna **RUL real** é o valor que os participantes deviam estimar
(tempo restante, em segundos, a partir do ponto de truncamento até a falha real).

| Rolamento | Condição | Data do ensaio | Arquivos (trunc.) | Canais | Duração (trunc.) | RUL real |
|---|---|---|---|---|---|---|
| Bearing1_3 | 1 | 2010-11-17 | 1802 | 2 | 5h00m10s | 5730 s |
| Bearing1_4 | 1 | 2010-12-07 | 1327 | 3 | 3h09m40s | 339 s  |
| Bearing1_5 | 1 | 2011-04-13 | 2685 | 3 | 6h23m30s | 1610 s |
| Bearing1_6 | 1 | 2011-04-14 | 2685 | 3 | 6h23m29s | 1460 s |
| Bearing1_7 | 1 | 2011-04-15 | 1752 | 3 | 4h10m11s | 7570 s |
| Bearing2_3 | 2 | 2011-05-19 | 1202 | 2 | 3h20m10s | 7530 s |
| Bearing2_4 | 2 | 2011-05-26 | 713  | 3 | 1h41m50s | 1390 s |
| Bearing2_5 | 2 | 2011-05-27 | 2337 | 3 | 5h33m30s | 3090 s |
| Bearing2_6 | 2 | 2011-06-07 | 572  | 2 | 1h35m10s | 1290 s |
| Bearing2_7 | 2 | 2011-06-08 | 200  | 2 | 0h28m30s | 580 s  |
| Bearing3_3 | 3 | 2011-04-08 | 410  | 3 | 0h58m30s | 820 s  |

> A pasta `Full_Test_Set` contém o ensaio completo de cada um desses 11 rolamentos (parte truncada
> acima + o restante até a falha). Use `Full_Test_Set` quando precisar de rótulos de RUL contínuos
> ao longo de todo o ciclo de vida; use `Test_set` para reproduzir exatamente as condições do desafio.

---

## Formato dos Arquivos CSV

Os arquivos são ASCII com valores separados por vírgula, **sem cabeçalho de coluna**, um arquivo por
aquisição (*snapshot*). Há dois tipos:

### Arquivos de vibração — `acc_xxxxx.csv`

| Coluna | Grandeza | Unidade |
|---|---|---|
| 1 | Hora | h |
| 2 | Minuto | min |
| 3 | Segundo | s |
| 4 | Micro-segundo | µs |
| 5 | Aceleração horizontal | g |
| 6 | Aceleração vertical | g |

- **Sensor:** 2× acelerômetro miniatura DYTRAN 3035B (IEPE/LIVM, 100 mV/g), posicionados a 90° entre
  si, radialmente na pista externa do rolamento (um no eixo horizontal, outro no vertical).
- **Taxa de amostragem:** 25,6 kHz
- **Snapshot:** 2560 amostras (1/10 s) registradas a cada 10 s → cada `acc_*.csv` tem 2560 linhas.

### Arquivos de temperatura — `temp_xxxxx.csv`

| Coluna | Grandeza | Unidade |
|---|---|---|
| 1 | Hora | h |
| 2 | Minuto | min |
| 3 | Segundo | s |
| 4 | Fração de segundo (0,x s) | s |
| 5 | Temperatura (sensor RTD) | °C |

- **Sensor:** RTD de platina PT100 (classe 1/3 DIN, IEC 751), instalado em um furo próximo à pista
  externa do rolamento.
- **Taxa de amostragem:** 10 Hz
- **Snapshot:** 600 amostras registradas a cada minuto → cada `temp_*.csv` tem 600 linhas.

> Nem todos os rolamentos possuem arquivos de temperatura: os ensaios marcados com "2 canais"
> registraram apenas vibração e não contêm arquivos `temp_*`.

---

## Especificações do Rolamento de Teste

| Propriedade | Valor |
|---|---|
| Diâmetro externo (D) | 32 mm |
| Diâmetro interno (d) | 20 mm |
| Espessura (B) | 7 mm |
| Carga estática nominal | 2470 N |
| Carga dinâmica nominal | 4000 N |
| Velocidade máxima | 13000 rpm |
| Diâmetro dos elementos rolantes | 3,5 mm |
| Número de elementos rolantes (Z) | 13 |
| Diâmetro da pista externa (De) | 29,1 mm |
| Diâmetro da pista interna (Di) | 22,1 mm |
| Diâmetro médio (Dm) | 25,6 mm |

---

## Estatísticas do Dataset (esta cópia)

| Métrica | Valor |
|---|---|
| Ensaios run-to-failure (oficiais) | 17 (6 treino + 11 teste) |
| Condições de operação | 3 |
| Pastas `Learning_set` | 6 rolamentos — 7534 arquivos `acc` + 850 `temp` |
| Pastas `Test_set` (truncado) | 11 rolamentos — 13959 arquivos `acc` + 1726 `temp` |
| Pastas `Full_Test_Set` (completo) | 11 rolamentos — 17355 arquivos `acc` + 2168 `temp` |
| Total de arquivos CSV | ~43.592 |
| Tamanho por snapshot de vibração | 2560 linhas |
| Tamanho por snapshot de temperatura | 600 linhas |

---

## Uso Recomendado para Machine Learning

### Carregamento de um snapshot de vibração

```python
import pandas as pd

cols_acc = ["hour", "minute", "second", "microsecond", "accel_h", "accel_v"]
df = pd.read_csv(
    r"Learning_set/Bearing1_1/acc_00001.csv",
    header=None, names=cols_acc
)
# accel_h e accel_v em g; 2560 linhas correspondentes a 1/10 s amostrado a 25,6 kHz
```

### Reconstrução do sinal contínuo de um rolamento

```python
import glob, os
import numpy as np
import pandas as pd

def carregar_rolamento(pasta):
    arquivos = sorted(glob.glob(os.path.join(pasta, "acc_*.csv")))
    sinais = []
    for f in arquivos:
        d = pd.read_csv(f, header=None,
                        names=["h","m","s","us","accel_h","accel_v"])
        sinais.append(d[["accel_h","accel_v"]].to_numpy())
    return np.concatenate(sinais, axis=0)  # (n_snapshots*2560, 2)

sinal = carregar_rolamento("Learning_set/Bearing1_1")
```

### Estratégia de rótulos (RUL)

```python
import re

def condicao_e_ensaio(nome_pasta):
    # "Bearing1_3" -> condicao=1, ensaio=3
    m = re.search(r"Bearing(\d)_(\d)", nome_pasta)
    return int(m.group(1)), int(m.group(2))

# RUL real publicada para os rolamentos de teste (em segundos), a partir do ponto de truncamento:
RUL_TESTE = {
    "Bearing1_3": 5730, "Bearing1_4": 339,  "Bearing1_5": 1610,
    "Bearing1_6": 1460, "Bearing1_7": 7570, "Bearing2_3": 7530,
    "Bearing2_4": 1390, "Bearing2_5": 3090, "Bearing2_6": 1290,
    "Bearing2_7": 580,  "Bearing3_3": 820,
}
```

Para rótulos contínuos ao longo da vida (regressão de RUL), assume-se comumente decaimento linear
do tempo total do ensaio (em `Full_Test_Set`) até 0 no instante da falha (último snapshot).

---

## Notas Importantes

1. **Sem informação de modo de falha:** o desafio não fornece o tipo de defeito; a degradação é
   natural e geralmente envolve múltiplos componentes ao mesmo tempo. Modelos baseados apenas em
   assinaturas de frequência teóricas (BPFI, BPFO, BSF, L10) tendem a não corresponder às observações.

2. **Variabilidade alta:** a vida dos rolamentos varia de ~1 h a ~7 h, mesmo na mesma condição de
   operação, o que torna a estimativa de RUL desafiadora com poucos exemplos de treino.

3. **Dois sensores de vibração:** cada arquivo `acc_*` traz simultaneamente as acelerações horizontal
   e vertical. Para análises multicanal, ambas estão no mesmo arquivo (colunas 5 e 6).

4. **Temperatura ausente em parte dos ensaios:** rolamentos com "2 canais" não têm arquivos `temp_*`.
   Pipelines que usam temperatura devem tratar essa ausência (ou restringir-se aos sinais de vibração,
   prática comum na literatura).

5. **Truncamento:** ao reproduzir o desafio, use `Test_set` (dados truncados) para treino/predição e
   compare a RUL estimada com `RUL_TESTE`. Use `Full_Test_Set` apenas para análises do ciclo de vida
   completo ou para construir rótulos contínuos.

6. **Função de pontuação do desafio:** o erro é convertido em erro percentual; subestimar a RUL
   (predição tardia) é penalizado mais brandamente do que superestimar (predição além da vida real),
   conforme definido no relatório oficial.

---

## Citação

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
