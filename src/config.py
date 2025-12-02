import os

# Caminhos padrão (ajuste se usar Data Lakehouse/warehouse, etc.)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_RAW = os.path.join(BASE_DIR, 'data', 'raw', 'dados_anon.csv')
DATA_PROCESSED = os.path.join(BASE_DIR, 'data', 'processed', 'dataset_processed.csv')
MODELS_DIR = os.path.join(BASE_DIR, 'models')
BEST_MODEL_PICKLE = os.path.join(MODELS_DIR, 'best_model.pkl')
BEST_MODEL_JOBLIB = os.path.join(MODELS_DIR, 'best_model.joblib')

# Coluna alvo
TARGET_COLUMN = 'target'

# Semente
RANDOM_STATE = 42

# Métricas
METRICS = ['accuracy', 'precision', 'recall', 'f1']
