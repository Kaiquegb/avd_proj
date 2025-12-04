from fastapi import FastAPI
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta

app = FastAPI()

# --- Configurações do Banco de Dados ---
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "weather_db")

# Cria a string de conexão e o motor do SQLAlchemy
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)

@app.get("/ingest")
def ingest_data():
    """
    Simula a coleta de dados de estações de PE e salva APENAS no Postgres.
    """
    # 1. Gerar Dados Simulados (Pernambuco)
    stations = ['A001_RECIFE', 'A002_PETROLINA', 'A003_CARUARU', 'A004_GARANHUNS', 'A005_ARARIPINA']
    data = []
    
    # Gerar dados dos últimos 30 dias
    start_date = datetime.now() - timedelta(days=30)
    for station in stations:
        for i in range(24 * 30): # Horas
            current_time = start_date + timedelta(hours=i)
            
            # Lógica de simulação climática (Tópico 7.4)
            if 'PETROLINA' in station or 'ARARIPINA' in station: # Sertão
                temp = np.random.uniform(25, 38)
                umid = np.random.uniform(20, 50)
                precip = np.random.choice([0, 0, 0, 5])
            elif 'RECIFE' in station: # Litoral
                temp = np.random.uniform(22, 30)
                umid = np.random.uniform(60, 95)
                precip = np.random.choice([0, 0, 5, 15, 30])
            else: # Agreste
                temp = np.random.uniform(18, 28)
                umid = np.random.uniform(40, 80)
                precip = np.random.choice([0, 5, 10])

            # Nomes das colunas em minúsculo para bater com o schema.sql
            data.append({
                "codigo_estacao": station,
                "data": current_time,
                "temperatura": round(temp, 2),
                "umidade": round(umid, 2),
                "vento_velocidade": round(np.random.uniform(0, 12), 2),
                "precipitacao": precip
            })

    df = pd.DataFrame(data)

    # 2. Salvar no Postgres (Structured Data)
    # if_exists='append' garante que não vamos apagar a tabela criada pelo SQL, apenas adicionar dados
    try:
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        return {"status": "sucesso", "mensagem": f"{len(df)} registros salvos no Banco de Dados com sucesso."}
    except Exception as e:
        return {"status": "erro", "mensagem": str(e)}