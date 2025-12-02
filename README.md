# Atividade N3 — Pipeline, Modelos e Deploy

Este projeto foi organizado para cumprir integralmente os itens da avaliação N3.

## a) Domínio de problema (1,0)
- Domínio: predição de churn (saída do cliente) em um cenário varejista fictício, usando dados anonimizados gerados a partir de registros sintéticos (N2). A variável alvo `target` representa a propensão de churn, com correlação controlada por idade e salário.
- Justificativa: o problema é clássico em Ciência de Dados, requer classificação binária e permite demonstrar pipeline, treino, métricas e deploy.

## Repositório de dados
- Escolha: Data Lake (arquivos CSV em diretórios `data/raw/` e `data/processed/`).
- Observação: a estrutura é compatível com evolução para Data Lakehouse (p.ex. Parquet/Delta). O código já inclui `pyarrow` para facilitar essa transição, caso desejado.

## b) Pipeline de dados (2,0)
Arquivo: `src/pipeline.py` (executado via `src/main.py`).
- Extração: leitura da fonte definida no repositório (`data/raw/dados_anon.csv`). Se o arquivo não existir, é gerado automaticamente por `src/anon_n2.py` com anonimização (pseudonimização, generalização e perturbação de salário).
- Transformação: limpeza de `NaN`, seleção de atributos numéricos (`idade`, `salario`, `salario_perturbado`) e normalização (`StandardScaler`). O alvo é `target`.
- Load: salvamento do dataset processado em `data/processed/dataset_processed.csv`.

Breve explicação dos elementos do pipeline:
- `extract()`: garante a disponibilidade da base anonimizando quando necessário e carrega o CSV bruto.
- `transform()`: padroniza atributos e compõe o dataset final com `X` e `y`.
- `load()`: persiste o dataset processado para consumo consistente por treino e avaliação.

## c) Treino e teste com três técnicas e três métricas (5,0)
Arquivo: `src/train.py`. São avaliados quatro algoritmos para reforçar o requisito (mínimo três):
- `LogisticRegression`, `RandomForestClassifier`, `SVC (RBF)`, `XGBClassifier`.

Métricas utilizadas (mínimo três, aqui usamos quatro):
- Accuracy: proporção de acertos globais; útil como baseline, pode ser enganosa em classes desbalanceadas.
- Precision: dos positivos preditos, quantos são realmente positivos; importante quando o custo de falso positivo é alto.
- Recall: dos positivos reais, quantos o modelo encontra; crítico quando falso negativo é mais custoso.
- F1-score: média harmônica de precision e recall; equilibra ambos e é usada para selecionar o melhor modelo.

Resultados: persistidos em `models/results.json`. O melhor modelo é selecionado pelo maior `F1`.

## d) Deploy do modelo (2,0)
Arquivo: `src/deploy.py`.
- Serialização: o melhor modelo é salvo em `models/best_model.pkl` (Pickle) e `models/best_model.joblib` (Joblib).
- Consumo: CLI de predição (`python -m src.deploy --values ...`) que carrega o modelo serializado e retorna a classe prevista.

Front-end demonstrativo:
- Pasta `front/` lê `models/results.json` e apresenta métricas e melhor modelo. Use `serve.ps1` para servir HTTP local e acessar `http://localhost:8000/front/`.

## Estrutura
- `data/` — dados brutos e processados.
- `src/` — pipeline, treino, avaliação e deploy.
- `models/` — artefatos (resultados e modelos serializados).
- `front/` — visualização dos resultados.
- `run.ps1` e `serve.ps1` — automação de execução e servidor local.

## Como executar
1) Instalar dependências:
```
powershell
python -m pip install -r .\requirements.txt
```
2) Rodar pipeline, treino e salvar modelos:
```
powershell
python -m src.anon_n2
python -m src.main
```
3) Ver resultados no front-end (opcional):
```
powershell
./serve.ps1 -Port 8000
# Abrir: http://localhost:8000/front/
```
4) Usar o modelo via CLI (opcional):
```
powershell
# Exemplo com três features (na ordem usada no treino): idade, salario, salario_perturbado
python -m src.deploy --model joblib --values 28 2500 2550
```

## Observações finais
- Caso utilize um repositório diferente (Data Warehouse/Lakehouse), ajuste `src/config.py` e as funções de `extract()` para ler da sua fonte (p.ex. Parquet/SQL) mantendo os mesmos contratos.
- Todos os itens (a–d) possuem arquivos e instruções específicas para apresentação e discussão in loco.
