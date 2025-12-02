import os
import hmac, hashlib
import numpy as np
import pandas as pd
from faker import Faker

RANDOM_SEED = 42
rng = np.random.default_rng(RANDOM_SEED)
fake = Faker("pt_BR")
Faker.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

SALT = "troque_este_salt_com_a_sua_turma"
IDADE_BINS = [0, 17, 24, 34, 44, 54, 64, 120]
IDADE_LABELS = ["0-17","18-24","25-34","35-44","45-54","55-64","65+"]


def pseudonimiza(valor: str) -> str:
    if pd.isna(valor):
        return valor
    if not isinstance(valor, str):
        valor = str(valor)
    key = SALT.encode()
    mac = hmac.new(key, valor.encode(), hashlib.sha256).hexdigest()
    return mac[:12]


def generaliza_idade(s):
    return pd.cut(s, bins=IDADE_BINS, labels=IDADE_LABELS, include_lowest=True, right=True)


def generaliza_salario_quantis(s, q=5):
    try:
        out = pd.qcut(s, q=q, duplicates="drop")
        return out.astype(str)
    except Exception:
        return s


def anonimiza_texto_livre(txt: str) -> str:
    if pd.isna(txt):
        return txt
    return "".join("x" if ch.isdigit() else ch for ch in txt)


def gera_sintetico(n=300):
    rows = []
    for i in range(n):
        nome = fake.name()
        email = fake.email()
        cpf = fake.cpf()
        telefone = fake.phone_number()
        cidade = fake.city()
        idade = rng.integers(16, 75)
        salario = float(rng.normal(3500, 1200))
        salario = max(1200.0, round(salario, 2))
        obs = f"{nome} comprou no cartão e ligou para {telefone}."
        rows.append(dict(
            id_cliente=i+1, nome=nome, email=email, cpf=cpf, telefone=telefone,
            cidade=cidade, idade=int(idade), salario=salario, observacoes=obs
        ))
    return pd.DataFrame(rows)


def gerar_e_salvar(base_dir: str):
    raw_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    df_raw = gera_sintetico(300)

    # anonimização
    df = df_raw.copy()
    cols_remover = ["email", "cpf", "telefone"]
    df["nome_pseudo"] = df["nome"].apply(pseudonimiza)
    df = df.drop(columns=["nome"])  # remove original
    df = df.drop(columns=cols_remover)
    df["faixa_idade"] = generaliza_idade(df["idade"]).astype(str)
    df["salario_faixa"] = generaliza_salario_quantis(df["salario"], q=5)
    df["observacoes_anon"] = df["observacoes"].apply(anonimiza_texto_livre)
    df = df.drop(columns=["observacoes"])  # remove original
    rs = np.random.RandomState(RANDOM_SEED)
    df["salario_perturbado"] = (df_raw["salario"] * (1 + rs.normal(0, 0.03, size=len(df)))).round(2)

    # alvo sintético: churn (classe) correlacionada com idade e salario
    df["target"] = ((df["idade"] < 30) & (df_raw["salario"] < 3000)).astype(int)

    csv_path = os.path.join(raw_dir, 'dados_anon.csv')
    df.to_csv(csv_path, index=False)
    return csv_path


if __name__ == '__main__':
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = gerar_e_salvar(BASE_DIR)
    print(f"Dados anonimizados salvos em: {path}")
