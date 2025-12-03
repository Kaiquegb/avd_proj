FROM jupyter/scipy-notebook:latest

USER root
# Instalar bibliotecas extras necessárias para o projeto
RUN pip install boto3 psycopg2-binary mlflow tb-mqtt-client

USER jovyan