import pickle
import joblib
import os
import argparse
import json
import pandas as pd
from typing import Dict
from src.config import BEST_MODEL_PICKLE, BEST_MODEL_JOBLIB, MODELS_DIR


def save_models(model) -> None:
    # Serializa com pickle e joblib
    with open(BEST_MODEL_PICKLE, 'wb') as f:
        pickle.dump(model, f)
    joblib.dump(model, BEST_MODEL_JOBLIB)


def load_model_pickle():
    with open(BEST_MODEL_PICKLE, 'rb') as f:
        return pickle.load(f)


def load_model_joblib():
    return joblib.load(BEST_MODEL_JOBLIB)


def predict_cli():
    parser = argparse.ArgumentParser(description='CLI de predição com modelo treinado')
    parser.add_argument('--model', choices=['pickle', 'joblib'], default='joblib')
    parser.add_argument('--values', nargs='+', type=float, required=True,
                        help='Valores das features na ordem usada no treino')
    args = parser.parse_args()

    model = load_model_joblib() if args.model == 'joblib' else load_model_pickle()
    X = pd.DataFrame([args.values])
    y_pred = model.predict(X)
    print(int(y_pred[0]))


def _best_from_results(results: Dict[str, Dict[str, float]]):
    if not results:
        return None, None
    best_name = max(results.keys(), key=lambda k: results[k].get('f1', 0.0))
    return best_name, results[best_name]


def show_results_log():
    """
    Exibe um log amigável dos resultados de teste (metrics) e melhor modelo.
    Lê models/results.json e imprime uma tabela alinhada.
    """
    path = os.path.join(MODELS_DIR, 'results.json')
    if not os.path.exists(path):
        print('[Resultados] Arquivo models/results.json não encontrado. Rode o treino primeiro (python -m src.main).')
        return
    with open(path, 'r') as f:
        results = json.load(f)

    # Cabeçalho
    print('\n===== Avaliação dos Modelos (Teste) =====')
    header = f"{'Algoritmo':<20} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>6}"
    print(header)
    print('-' * len(header))

    # Linhas
    for name, m in results.items():
        acc = float(m.get('accuracy', 0.0))
        prec = float(m.get('precision', 0.0))
        rec = float(m.get('recall', 0.0))
        f1 = float(m.get('f1', 0.0))
        print(f"{name:<20} {acc:>9.3f} {prec:>10.3f} {rec:>8.3f} {f1:>6.3f}")

    best_name, best_metrics = _best_from_results(results)
    if best_name:
        print('\n>> Melhor modelo (por F1):')
        print(f"   - {best_name} | F1={best_metrics.get('f1', 0.0):.3f} | Acc={best_metrics.get('accuracy', 0.0):.3f} | Prec={best_metrics.get('precision', 0.0):.3f} | Rec={best_metrics.get('recall', 0.0):.3f}")
    print('========================================\n')


if __name__ == '__main__':
    # Se executado diretamente sem args, mostra resultados bonitos.
    import sys
    if len(sys.argv) > 1:
        predict_cli()
    else:
        show_results_log()
