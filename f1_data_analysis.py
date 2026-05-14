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
    print(f"Nacionalidades: {dados['drivers'].nunique()}")

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


# === Análise de insights ===

# Pilotos com mais vitórias

# -- assumindo que a última corrida do ano terá a posição final do corredor

def analise_vitorias():
    drivers = dados['drivers']
    driver_standings = dados['driver_standings']
    races = dados['races']

    # encontrar ultima corrida
    ultima_corrida = races.groupby('year')['round'].max().reset_index()
    ultima_corrida = ultima_corrida.merge(
        races[['year', 'round', 'raceId']],
        on=['year', 'round'] # análise por ano e corrida
    )

    # clasficação final
    classificacao_final = driver_standings.merge(
        ultima_corrida[['year', 'raceId']], # merge no raceId comum das tabelas
        on='raceId'
    )

    vencedores = classificacao_final[classificacao_final['position'] == 1].copy()

    vencedores = vencedores.merge(
        drivers[['driverId', 'forename', 'surname']],
        on='driverId' #merge no dirverId comum das tabelas
    )
    vencedores['piloto'] = vencedores['forename'] + ' ' + vencedores['surname'] # monta a string do nome

    # contagem de titulos

    titulos = vencedores.groupby(['piloto']).size().reset_index(name='titulos')
    titulos = titulos.sort_values('titulos', ascending=False)

    print("\nPilotos com mais vitórias:")
    for i, (_, row) in enumerate(titulos.head(10).iterrows(), 1):
        print(f" {i}. {row['piloto']:30s}) - {row['titulos']}  títulos")

    return titulos

titulos = analise_vitorias()


# relação piloto por circuito

def analise_pilotos_circuitos():
    drivers = dados['drivers']
    results = dados['results']
    races = dados['races']
    circuits = dados['circuits']

    # vitoria quando position = 1
    vitorias = results[results['position'] == 1].copy()

    vitorias = vitorias.merge(races[['raceId', 'circuitId', 'name']], on='raceId')
    vitorias = vitorias.merge(drivers[['driverId', 'forename', 'surname']], on='driverId')
    vitorias = vitorias.merge(circuits[['circuitId', 'name']], on='circuitId')

    #dentro de vitorias, definir nome
    vitorias['piloto'] = vitorias['forename'] + ' ' + vitorias['surname']
        
# relação piloto por circuito

def analise_pilotos_circuitos(circuito_nome=None, top_n=5):
    drivers = dados['drivers']
    results = dados['results']
    races = dados['races']
    circuits = dados['circuits']

    # vitoria quando position = 1
    vitorias = results[results['position'] == 1].copy()

    vitorias = vitorias.merge(races[['raceId', 'circuitId', 'name']], on='raceId')
    vitorias = vitorias.merge(drivers[['driverId', 'forename', 'surname']], on='driverId')
    vitorias = vitorias.merge(circuits[['circuitId', 'name']], on='circuitId')

    #dentro de vitorias, definir nome
    vitorias['piloto'] = vitorias['forename'] + ' ' + vitorias['surname']

    if circuito_nome:
        vitorias_circuito = vitorias[vitorias['name_y'].str.contatins(circuito_nome, case=False)]
        top_pilotos = vitorias_circuito.groupby('piloto').size().reset_index(name='vitorias')
        top_pilotos = top_pilotos.sort_values('vitorias', ascending=False).head(top_n)

        print(f"\nPilotos com mais vitórias no circuito {circuito_nome}:")

        for i, (_, row) in enumerate(top_pilotos.iterrows(), 1):
            print(f" {i}. {row['piloto']} - {row['vitorias']} vitórias")
        return top_pilotos
    else:
        print("finalizar")
    
