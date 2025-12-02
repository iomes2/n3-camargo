import os
import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from src.config import DATA_PROCESSED, TARGET_COLUMN, RANDOM_STATE, MODELS_DIR

ALGORITHMS = {
    'logistic_regression': LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
    'random_forest': RandomForestClassifier(n_estimators=200, random_state=RANDOM_STATE),
    'svm_rbf': SVC(kernel='rbf', probability=True, random_state=RANDOM_STATE),
    'xgboost': XGBClassifier(n_estimators=200, max_depth=4, subsample=0.9, colsample_bytree=0.9, random_state=RANDOM_STATE)
}


def load_processed() -> pd.DataFrame:
    return pd.read_csv(DATA_PROCESSED)


def train_and_evaluate():
    df = load_processed()
    X = df.drop(columns=[TARGET_COLUMN])
    y = df[TARGET_COLUMN]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=RANDOM_STATE, stratify=y
    )

    results = {}

    for name, model in ALGORITHMS.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'precision': float(precision_score(y_test, y_pred, zero_division=0)),
            'recall': float(recall_score(y_test, y_pred, zero_division=0)),
            'f1': float(f1_score(y_test, y_pred, zero_division=0))
        }

    os.makedirs(MODELS_DIR, exist_ok=True)
    with open(os.path.join(MODELS_DIR, 'results.json'), 'w') as f:
        json.dump(results, f, indent=2)

    # Seleciona melhor por F1
    best_name = max(results.keys(), key=lambda k: results[k]['f1'])
    best_model = ALGORITHMS[best_name]

    return best_name, best_model, results


if __name__ == '__main__':
    best_name, _, results = train_and_evaluate()
    print('Resultados:')
    for k, v in results.items():
        print(k, v)
    print(f"Melhor modelo: {best_name}")
