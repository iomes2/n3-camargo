# Atividade N3 — Pipeline, Modelos e Deploy

Este projeto entrega a avaliação N3 com:
- Reapresentação do domínio de problema e repositório de dados
- Pipeline de dados (ETL/ELT) e breve explicação dos elementos
- Treinamento e teste com 3 algoritmos e 3 métricas
- Deploy do melhor modelo via Pickle/Joblib e um CLI simples

Estrutura:
- `data/` — dados brutos e processados (placeholders)
- `src/` — código da pipeline, treino, avaliação e deploy
- `models/` — artefatos de modelos serializados

Como rodar:
1) Instale dependências
2) Execute o pipeline e treino
3) Rode a avaliação e gere o deploy

Comandos estão na seção "Como executar".

Observação: Caso seu domínio e dataset sejam diferentes, substitua o arquivo `data/raw/dataset.csv` e ajuste `src/config.py`.
