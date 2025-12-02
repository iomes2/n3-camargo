import pickle
import joblib
import os
import argparse
import pandas as pd
from src.config import BEST_MODEL_PICKLE, BEST_MODEL_JOBLIB


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


if __name__ == '__main__':
    predict_cli()
