from src.pipeline import run_pipeline
from src.train import train_and_evaluate
from src.deploy import save_models, show_results_log

if __name__ == '__main__':
    processed = run_pipeline()
    best_name, best_model, results = train_and_evaluate()
    save_models(best_model)
    show_results_log()
    print('Modelos salvos em pickle e joblib.')
