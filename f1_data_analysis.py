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

# corridas

print("\n TABELA DE CORRIDAS")

if len(dados['races']) > 0:
    print(f"Total de corridas {len(dados['races'])}")
    print(f"Período das corridas: {dados['races']['year'].min()} a {dados['races']['year'].max()}")
    corridas_ano = dados['races'].groupby('year').size().tail(10)
    print(corridas_ano)


# circuitos

print("\n TABELA DE CIRCUITOS")

if len(dados['circuits']) > 0:
    print(f"Total de circuitos {len(dados['circuits'])}")
    circuit_name = dados['circuits']['name'].tolist()
    #print(circuit_name)


# Resultados


print("\n TABELA DE RESULTADOS")

if len(dados['results']) > 0:
    print(f"Colunas de resultados: {dados['results'].select_dtypes(include=[np.number])
                                    .columns.tolist()}")
    
    # estatisica de pontos
    if 'points' in dados['results'].columns:
        print(f"Média de pontos {dados['results']['points'].mean():.2f}")
        print(f"Maximo {dados['results']['points'].max()}") # mínimo sempre será zero
        print(f"Total distribuído: {dados['results']['points'].sum():,.0f}")


# Pit Stops

print("\n TABELA DE PIT STOPS")

if len(dados['pit_stops']) > 0:
    print(dados['pit_stops']['duration']) # dados estão em string

    # converter para numérico, forçando erros em nulos
    dados['pit_stops']['duration'] = pd.to_numeric(dados['pit_stops']['duration'], errors='coerce')

    print(f"Maior tempo de pit stop: {dados['pit_stops']['duration'].astype(float).max()} ms")
    print(f"Média de tempo de pit stop: {dados['pit_stops']['duration'].astype(float).mean():.2f} ms")
    print(f"Menor tempo de pit stop: {dados['pit_stops']['duration'].astype(float).min()} ms")
