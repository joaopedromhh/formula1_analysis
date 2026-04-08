import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime


# load data
circuits = pd.read_csv('dataset/circuits.csv')
driver_standings = pd.read_csv('dataset/driver_standings.csv')
drivers = pd.read_csv('dataset/drivers.csv')
lap_times = pd.read_csv('dataset/lap_times.csv')
pit_stops = pd.read_csv('dataset/pit_stops.csv')
qualifying = pd.read_csv('dataset/qualifying.csv')
races = pd.read_csv('dataset/races.csv')
results = pd.read_csv('dataset/results.csv')
seasons = pd.read_csv('dataset/seasons.csv')
status = pd.read_csv('dataset/status.csv')


# relação pilotos p/ circuito

def pilotos_por_circuito(circuito_nome=None, top_n=5):

    # unir tabelas de corridas com pilotos
    resultados = results.merge(races[['raceId', 'circuitId', 'name']], on='raceId')
    resultados = resultados.merge(drivers[['driverId', 'forename', 'surname']], on='driverId')

    # filtrar pela melhor posição (considerando vitória sendo posição 1)

    vitorias = resultados[resultados['position'] == '1']

    if circuito_nome:
        circuitos = circuits[circuits['name'].str.contains(circuito_nome, case=False)]
        if len(circuitos) > 0:
            # pegar nome dos circuitos pelo ID
            circuitos_filtrados = circuitos['circuitId'].tolist()
            vitorias = vitorias[vitorias['circuitId'].isin(circuitos_filtrados)]

            top = vitorias.groupby(['driverId', 'forename', 'surname']).size().reset_index(name='vitorias')
            top = top.nlargest(top_n, 'vitorias')
            top['piloto'] = top['forename'] + ' ' + top['surname']

            print(f"\n Pilotos {top_n} com mais vitorias em {circuito_nome.upper()}:")
            for idx, row in top.iterrows():
                print(f" {row['piloto']} - {row[vitorias]}")
            return top
        else:
            # Top 5 circuitos com mais pilotos diferentes vencendo
            vitorias_por_circuito = vitorias.groupby(['circuitId', 'driverId']).size().reset_index()
            diversidade = vitorias_por_circuito.groupby('circuitId').size().reset_index(name='n_pilotos')
            diversidade = diversidade.merge(circuits[['circuitId', 'name']], on='circuitId')
            diversidade = diversidade.nlargest(5, 'n_pilotos')
            
            print("\n🏁 Circuitos com maior diversidade de vencedores:")
            for idx, row in diversidade.iterrows():
                print(f"   {row['name']} - {row['n_pilotos']} pilotos diferentes venceram")
            return diversidade

# Executar análise
pilotos_por_circuito(None)  # Mostra diversidade de circuitos
pilotos_por_circuito('Monaco', 5)  # Top 5 em Mônac