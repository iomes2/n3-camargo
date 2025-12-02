from src.pipeline import run_pipeline
from src.train import train_and_evaluate
from src.deploy import save_models

if __name__ == '__main__':
    processed = run_pipeline()
    best_name, best_model, results = train_and_evaluate()
    save_models(best_model)
    print('--- Sumário ---')
    print('Resultados por algoritmo:', results)
    print('Melhor modelo:', best_name)
    print('Modelos salvos em pickle e joblib.')
