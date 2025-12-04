# Pipeline de Análise Climática de Pernambuco (Tópico 7.4)

**Disciplina:** Análise e Visualização de Dados - 2025.2  
**Instituição:** CESAR School  
**Equipe:**
* [Kaique Alves] 
* [Ícaro Sampaio] 

---

## 📌 Sobre o Projeto
Este projeto implementa um pipeline completo de Engenharia de Dados utilizando Docker. O objetivo é coletar, armazenar, processar e visualizar dados meteorológicos para identificar perfis climáticos (Clusters) nas estações de Pernambuco.

**Tópico Escolhido:** 7.4 - Agrupar Estações Meteorológicas por Perfil.

## 🏗️ Arquitetura
O sistema é composto pelos seguintes serviços em containers:
1.  **FastAPI (Porta 8000):** Simulação e ingestão de dados climáticos.
2.  **PostgreSQL (Porta 5432):** Data Warehouse para armazenamento estruturado.
3.  **Jupyter Lab (Porta 8888):** Ambiente de Análise de Dados e Machine Learning (K-Means).
4.  **MLFlow (Porta 5000):** Registro de experimentos e métricas.
5.  **ThingsBoard (Porta 80):** Dashboard interativo para visualização de mapas.
6.  **MinIO (Porta 9000):** Object Storage (S3 Compatible).

---

## 🚀 Como Executar

### Pré-requisitos
* Docker e Docker Compose instalados.

### Passo a Passo
1.  **Clonar o repositório:**
    ```bash
    git clone [SEU_LINK_GITHUB]
    cd AVD_PROJ
    ```

2.  **Subir a infraestrutura:**
    ```bash
    docker-compose up -d --build
    ```
    *Aguarde alguns minutos até que todos os containers estejam "Healthy".*

3.  **Ingerir os Dados (ETL):**
    * Acesse a documentação da API: [http://localhost:8000/docs](http://localhost:8000/docs)
    * Execute o endpoint **`GET /ingest`**.
    * Verifique se retornou "Status 200".

4.  **Executar a Análise (Jupyter):**
    * Pegue o token de acesso no terminal: `docker logs jupyter_lab`
    * Acesse: [http://localhost:8888](http://localhost:8888)
    * Abra a pasta `notebooks` e execute o arquivo `analise_clima.ipynb`.

5.  **Visualizar o Dashboard:**
    * Acesse: [http://localhost](http://localhost)
    * **Login:** `tenant@thingsboard.org`
    * **Senha:** `tenant`
    * Vá em "Dashboards" > "Mapa Climático PE".

---

## 📊 Resultados
O modelo identificou com sucesso 3 clusters climáticos distintos, visualizados no mapa do ThingsBoard:
* **Cluster 0 (Vermelho):** Região do Sertão (Araripina).
* **Cluster 1 (Azul):** Região Litorânea (Recife).
* **Cluster 2 (Verde):** Região de Transição (Petrolina).

---
*Projeto desenvolvido para fins acadêmicos.*
