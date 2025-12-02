import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.config import DATA_RAW, DATA_PROCESSED, TARGET_COLUMN, RANDOM_STATE

# Elementos do pipeline:
# - Extração: carrega dataset da fonte definida (aqui: CSV local)
# - Transformação: limpeza, seleção de features, normalização
# - Load: salva dataset processado para consumo pelos modelos

def extract() -> pd.DataFrame:
    # Usa dataset anonimizando da N2 se existir, senão gera via anon_n2
    if not os.path.exists(DATA_RAW):
        from src.anon_n2 import gerar_e_salvar
        base_dir = os.path.dirname(os.path.dirname(__file__))
        gerar_e_salvar(base_dir)
    return pd.read_csv(DATA_RAW)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna()
    # Separa X e y
    # Seleção de features compatíveis com N2
    candidate_cols = [
        'idade', 'salario', 'salario_perturbado'
    ]
    X = df[[c for c in candidate_cols if c in df.columns]]
    y = df[TARGET_COLUMN]
    # Escalonamento de features numéricas
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=X.columns)
    processed = pd.concat([X_scaled_df, y.reset_index(drop=True)], axis=1)
    return processed

def load(processed: pd.DataFrame) -> None:
    os.makedirs(os.path.dirname(DATA_PROCESSED), exist_ok=True)
    processed.to_csv(DATA_PROCESSED, index=False)


def run_pipeline() -> pd.DataFrame:
    df = extract()
    processed = transform(df)
    load(processed)
    return processed

if __name__ == '__main__':
    run_pipeline()
    print(f"Pipeline concluído. Arquivo salvo em: {DATA_PROCESSED}")
