# Análise de Confiabilidade de um Conjunto Motor-Bomba Centrífuga

Implementação do trabalho final da disciplina EEE017 (Confiabilidade de Sistemas,
UFMG). O código deriva índices de confiabilidade a partir de dados experimentais de
vibração de um conjunto motor-bomba e modela o sistema por Diagrama de Blocos de
Confiabilidade com simulação de Monte Carlo.

Autores: Stéphanie Pereira Barbosa, Isabella Beatriz de Souza Gomes, Felipe Costa Lopes.

Proposta completa: `../latex/Proposta_EEE017.tex`.

## 1. Visão Geral

O objetivo é responder, do ponto de vista da confiabilidade: dado um modo de falha,
qual é a vida esperada do equipamento e como a configuração do sistema afeta sua
disponibilidade? Para isso o pipeline:

1. extrai um indicador de degradação dos sinais de vibração;
2. constrói séries de tempo até a falha (TTF) por um modelo de degradação;
3. ajusta distribuições de vida (Exponencial, Weibull, Lognormal) com censura;
4. estima intervalos de confiança dos parâmetros por bootstrap;
5. calcula MTTF, R(t), taxa de falha h(t) e disponibilidade;
6. modela o sistema motor-bomba e simula série, paralelo e standby por Monte Carlo.

## 2. Dados Utilizados

Dataset público "Motor Current and Vibration Monitoring Dataset for various Faults
in an E-motor-driven Centrifugal Pump" (Bruinsma et al., 2024), armazenado em
`../data/dataset_bruinsma2024/`. São sinais de vibração (5 acelerômetros, 20 kHz) e corrente/tensão de
duas bancadas motor-bomba sob diversas falhas em vários níveis de severidade.

Cada arquivo CSV tem a coluna `time` e várias colunas numeradas, onde cada coluna é
uma repetição independente da mesma medição. A documentação detalhada do dataset
está em `../data/.../DATASET_README.md`.

Importante: o dataset é de snapshots de condição (não run-to-failure). A ponte para
a confiabilidade é descrita na metodologia.

## 3. Metodologia

### Indicador de degradação
RMS do sinal de vibração dentro de uma banda de frequência (via Welch), escolhida
pela física de cada falha e validada por correlação de Spearman com a severidade:
- rolamento: banda alta (1-9 kHz), onde aparecem os impactos;
- desbalanceamento e desalinhamento: banda baixa (10-300 Hz), harmônicos 1x/2x.

O RMS de banda larga puro não funciona para rolamento, por isso a separação por banda.

### Construção do TTF (modelo de degradação)
Como não há tempo real de falha, modelamos a degradação como crescimento
exponencial D(t) = D0 · exp(rho · t):
- cada nível de severidade vira um instante de operação (t = nível · HORAS_POR_NIVEL);
- a taxa média rho é calibrada nos dados (do saudável até a severidade máxima);
- cada unidade simulada recebe uma taxa aleatória (variabilidade operacional, que um
  dataset de snapshots não fornece sozinho);
- a unidade falha quando D cruza o limiar L;
- unidades que não cruzam até o horizonte são dados censurados à direita.

### Ajuste, IC e índices
Ajuste de Exponencial, Weibull e Lognormal por máxima verossimilhança com censura
(biblioteca `reliability`), comparação por AICc e Kolmogorov-Smirnov, median ranks de
Benard para os gráficos, IC 95% por bootstrap, e os índices MTTF, R(t), h(t) e
disponibilidade A = MTTF/(MTTF+MTTR).

### Sistema
O conjunto é motor em série com bomba (a falha de qualquer um para o conjunto).
Monte Carlo (t = F^-1(U)) avalia três configurações: série (real), paralelo e
standby (redundâncias hipotéticas). As fórmulas analíticas de disponibilidade
verificam a simulação.

## 4. Modos de Falha Analisados

| Modo | Subsistema | Canal | Banda | Categoria |
|------|------------|-------|-------|-----------|
| Rolamento BPFI | motor | ch1 | 1-9 kHz | rolamento |
| Desbalanceamento no motor | motor | ch2 | 10-200 Hz | desbalanceamento |
| Desbalanceamento na bomba | bomba | ch5 | 10-200 Hz | desbalanceamento |
| Desalinhamento paralelo | bomba | ch1 | 10-300 Hz | desalinhamento |

A pista externa do rolamento (BPFO) e o desalinhamento angular foram avaliados, mas
descartados: a assinatura em RMS de banda desses modos, nos canais disponíveis,
ficou dentro da variabilidade da própria condição saudável (não separável). Ficam
documentados, comentados, em `config.py`.

## 5. Estrutura dos Arquivos

```
code/
├── config.py                 # caminhos, modos de falha, constantes, MODO_RAPIDO
├── utils.py                  # leitura de sinal, RMS de banda, median rank
├── extrair_features.py       # passo 1: sinais -> features.csv
├── construir_ttf.py          # passo 2: features -> ttf.csv
├── ajustar_distribuicoes.py  # passo 3: ajuste Exp/Weibull/Lognormal
├── bootstrap_ic.py           # passo 4: IC por bootstrap
├── indices.py                # passo 5: MTTF, R(t), h(t), disponibilidade
├── sistema.py                # passo 6: DBC + Monte Carlo do sistema
├── graficos.py               # funções de plotagem
├── main.py                   # roda os 6 passos na ordem
└── resultados/
    ├── figuras/   # PNGs
    └── tabelas/   # CSVs
```

## 6. Como Executar

### 6.1 Pré-requisitos

- Python 3.12 ou superior
- Git (para clonar o repositório)

### 6.2 Instalação dos pacotes

Na raiz do projeto, instale todas as dependências com um único comando:

```bash
pip install -r code/requirements.txt
```

Ou manualmente:

```bash
pip install numpy scipy pandas matplotlib reliability openpyxl
```

### 6.3 Preparar o dataset

Você tem duas opções:

**Opção A — Dataset reduzido (recomendado, ~7 GB)**
Contém apenas os 28 arquivos efetivamente usados pelo trabalho final:

```bash
python code/construir_dataset_tiny.py
```

O script cria a pasta `data/database_tiny/` com a estrutura original preservada.
Depois, em `code/config.py`, confirme que a variável aponta para o tiny:

```python
# Em code/config.py, linha DATASET:
DATASET = os.path.join(RAIZ, "..", "data", "database_tiny", "Vibration")
```

**Opção B — Dataset completo (~80 GB)**
Já deve estar em `data/dataset_bruinsma2024/`.
Não é necessário nenhum comando adicional.

### 6.4 Rodar o trabalho final

```bash
cd <raiz do projeto>
python code/main.py
```

Resultados gerados em:
- `code/resultados/figuras/` — todas as figuras PNG
- `code/resultados/tabelas/` — tabelas CSV com os índices numéricos

### 6.5 Controle de velocidade

Em `code/config.py`, a variável `MODO_RAPIDO` controla quanto do sinal é lido:

```python
MODO_RAPIDO = True   # lê ~1,5 s por arquivo — roda em ~30 s (para testar)
MODO_RAPIDO = False  # lê o arquivo inteiro  — roda em ~4 min (resultados finais)
```

### 6.6 Rodar passos individuais

Cada passo pode ser rodado isoladamente. Isso é útil para regenerar só os
gráficos sem reler os CSVs (o passo 1 é o único caro):

```bash
# Passo 1 (lento — lê os CSVs grandes):
python code/extrair_features.py

# Passos 2-6 (rápidos — leem features.csv):
python code/construir_ttf.py
python code/ajustar_distribuicoes.py
python code/bootstrap_ic.py
python code/indices.py
python code/sistema.py
```

### 6.7 Observação sobre caminhos no Windows

Os caminhos do dataset original passam de 260 caracteres (limite MAX_PATH do
Windows). O código aplica o prefixo `\\?\` automaticamente via
`utils.caminho_longo()`. Se rodar no dataset tiny (pasta de nome curto), isso
não é necessário, mas o código funciona nos dois casos.

## 7. Saídas

Tabelas (`resultados/tabelas/`):
- `features.csv` - indicador de degradação por repetição/condição;
- `ttf.csv` - tempos até a falha com indicador de censura;
- `parametros.csv` - parâmetros ajustados e AICc das três distribuições;
- `bootstrap_ic.csv` - IC 95% de beta e eta;
- `indices.csv` - MTTF, taxa de falha, beta, disponibilidade, estágio na banheira;
- `sistema.csv` - disponibilidade (analítica e MC) e R na missão por configuração.

Figuras (`resultados/figuras/`), por modo de falha:
- `p1_assinatura_*` - indicador de degradação vs severidade;
- `p2_ttf_*` - histograma dos TTF construídos;
- `p3_weibull_*` - papel de probabilidade Weibull;
- `p3_cdf_*` - ajuste das três distribuições sobre a empírica;
- `p4_bootstrap_*` - distribuição bootstrap de beta e eta;
- `p5_indices_*` - R(t), h(t) e f(t);
- `p5_R_banda_*` - R(t) com banda de confiança 95%;

E do sistema:
- `p6_sistema_R.png` - R(t) do sistema (série, paralelo, standby);
- `p6_disponibilidade.png` - disponibilidade por configuração;
- `resumo_modos.png` - MTTF e beta de todos os modos.

## 8. Principais Resultados (base completa)

Índices por modo de falha:

| Modo | Melhor dist. (AICc) | MTTF [h] | beta Weibull | Estágio |
|------|---------------------|----------|--------------|---------|
| Rolamento BPFI | Lognormal | 4857 | 3.82 | desgaste |
| Desbalanceamento no motor | Lognormal | 5997 | 0.98 | taxa ~ constante |
| Desbalanceamento na bomba | Lognormal | 1836 | 1.68 | desgaste |
| Desalinhamento paralelo | Lognormal | 2831 | 2.92 | desgaste |

As quatro escolhem a Lognormal pelo AICc, o que é coerente com o mecanismo de
degradação exponencial com taxa aleatória (que gera vida lognormal). A Weibull é
mantida para a leitura do beta: rolamento e desalinhamento ficam na região de
desgaste (beta > 1), enquanto o desbalanceamento no motor fica próximo de taxa
constante (beta ~ 1).

Sistema motor-bomba (disponibilidade e confiabilidade na missão de 2000 h):

| Configuração | A (analítico) | A (Monte Carlo) | R(2000 h) |
|--------------|---------------|------------------|-----------|
| Série (real) | 0.98316 | 0.98325 | 0.191 |
| Paralelo | 0.99972 | 0.99976 | 0.348 |
| Standby | 0.99970 | (analítico) | 0.642 |

A disponibilidade por Monte Carlo bate com a analítica (diferença na 3ª casa),
validando a simulação. A redundância (paralelo/standby) reduz a indisponibilidade de
~1,7% para ~0,03% e eleva bastante a confiabilidade na missão.

## 9. Premissas e Limitações

- O dataset é de snapshots, não de vida real; os TTF vêm de um modelo de degradação,
  não de falhas observadas no tempo. A escala de tempo (`HORAS_POR_NIVEL`) e a
  variabilidade da taxa (`COV_TAXA`) são premissas de modelagem, documentadas em
  `config.py`; mudá-las reescalona/realarga as distribuições, mas não muda as
  comparações relativas entre modos e configurações.
- A disponibilidade do standby é verificada apenas analiticamente (a simulação
  correta da reserva fria com reparo está fora do escopo).

## 10. Referências

- S. Bruinsma et al., "Motor current and vibration monitoring dataset...", Data in
  Brief, 2024.
- P. O'Connor, A. Kleyner, "Practical Reliability Engineering", 5ª ed., Wiley.
- Notas de aula e scripts da disciplina EEE017 (Prof. Michel Bessani), UFMG.
