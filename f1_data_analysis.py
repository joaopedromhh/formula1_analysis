import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# load data (nome + caminho)

arquivos = {
    'circuits': 'dataset/circuits.csv',
    'driver_standings': 'dataset/driver_standings.csv',
    'drivers': 'dataset/drivers.csv',
    'lap_times': 'dataset/lap_times.csv',
    'pit_stops': 'dataset/pit_stops.csv',
    'qualifying': 'dataset/qualifying.csv',
    'races': 'dataset/races.csv',
    'results': 'dataset/results.csv',
    'seasons': 'dataset/seasons.csv',
    'status': 'dataset/status.csv'
}


dados = {}

for nome, caminho in arquivos.items():
    try:
        dados[nome] = pd.read_csv(caminho)
        print(f"[OK] {nome:20s}: {len(dados[nome]):8,} registros")
    except Exception as e:
        print(f"[ERRO] {nome:20s}: {e}")
        dados[nome] = pd.DataFrame()

print("Dados carregados")

# explorar o dataset

# geral

for nome, df in dados.items():
    if len(df) > 0:
        print(f" -- {nome.upper()} --")
        print(f" Registros: {len(df):,}")
        print(f" Colunas {df.shape[1]}")
        print(f" Colunas {list(df.columns)}")
        print(f" Valores nulos: {df.isnull().sum().sum()}")


# explorar bases

# pilotos

print("\n TABELA DE PILOTOS")

if len(dados['drivers']) > 0:
    print(f"Total Pilotos: {len(dados['drivers'])}")
    print(f"Nacionalidades: {dados['drivers']['nationality'].nunique()}")
    





