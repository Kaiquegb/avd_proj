from fastapi import FastAPI
import pandas as pd
import numpy as np
import boto3
import io
from sqlalchemy import create_engine
import os
from datetime import datetime, timedelta

app = FastAPI()

# Configurações via Variáveis de Ambiente
DB_USER = os.getenv("DB_USER", "admin")
DB_PASS = os.getenv("DB_PASS", "admin")
DB_HOST = os.getenv("DB_HOST", "postgres")
DB_NAME = os.getenv("DB_NAME", "weather_db")

# Conexão com Banco
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
engine = create_engine(DATABASE_URL)

# Conexão com MinIO (S3)
s3 = boto3.client('s3',
                  endpoint_url=f"http://{os.getenv('S3_ENDPOINT', 'minio:9000')}",
                  aws_access_key_id=os.getenv("S3_ACCESS_KEY", "minioadmin"),
                  aws_secret_access_key=os.getenv("S3_SECRET_KEY", "minioadmin"))

@app.on_event("startup")
def startup_event():
    # Garantir que o bucket existe
    try:
        s3.create_bucket(Bucket="raw-data")
    except:
        pass

@app.get("/ingest")
def ingest_data():
    """
    Simula a coleta de dados de estações de PE e salva no MinIO e Postgres.
    """
    # 1. Gerar Dados Simulados (Pernambuco)
    stations = ['A001_RECIFE', 'A002_PETROLINA', 'A003_CARUARU', 'A004_GARANHUNS', 'A005_ARARIPINA']
    data = []
    
    # Gerar dados dos últimos 30 dias
    start_date = datetime.now() - timedelta(days=30)
    for station in stations:
        for i in range(24 * 30): # Horas
            current_time = start_date + timedelta(hours=i)
            
            # Simulando perfis climáticos diferentes para testar o clustering
            if 'PETROLINA' in station or 'ARARIPINA' in station: # Sertão (Quente/Seco)
                temp = np.random.uniform(25, 38)
                umid = np.random.uniform(20, 50)
                precip = np.random.choice([0, 0, 0, 5])
            elif 'RECIFE' in station: # Litoral (Úmido)
                temp = np.random.uniform(22, 30)
                umid = np.random.uniform(60, 95)
                precip = np.random.choice([0, 0, 5, 15, 30])
            else: # Agreste
                temp = np.random.uniform(18, 28)
                umid = np.random.uniform(40, 80)
                precip = np.random.choice([0, 5, 10])

            data.append({
                "CODIGO_ESTACAO": station,
                "DATA": current_time,
                "TEMPERATURA": round(temp, 2),
                "UMIDADE": round(umid, 2),
                "VENTO_VELOCIDADE": round(np.random.uniform(0, 12), 2),
                "PRECIPITACAO": precip
            })

    df = pd.DataFrame(data)

    # 2. Salvar no MinIO (Raw Data - CSV)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    s3.put_object(Bucket="raw-data", Key=f"weather_pe_{datetime.now().date()}.csv", Body=csv_buffer.getvalue())

    # 3. Salvar no Postgres (Structured Data)
    df.to_sql('weather_data', engine, if_exists='replace', index=False)

    return {"status": "sucesso", "mensagem": f"{len(df)} registros processados e salvos."}