FROM python:3.9-slim

WORKDIR /app

# Instala dependências do sistema
RUN apt-get update && apt-get install -y libpq-dev gcc

# AQUI ESTAVA O ERRO: Removemos o "../" pois agora o contexto é a raiz
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Copia a pasta fastapi inteira para dentro do container
COPY fastapi/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]