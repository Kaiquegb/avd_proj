-- Estrutura da Tabela
CREATE TABLE IF NOT EXISTS weather_data (
    codigo_estacao VARCHAR(50),
    data TIMESTAMP,
    temperatura FLOAT,
    umidade FLOAT,
    vento_velocidade FLOAT,
    precipitacao FLOAT
);

-- View para facilitar a leitura no Jupyter (Médias Diárias)
CREATE VIEW view_medias_diarias AS
SELECT 
    codigo_estacao,
    DATE(data) as data_dia,
    AVG(temperatura) as temperatura,
    AVG(umidade) as umidade,
    AVG(vento_velocidade) as vento_velocidade,
    SUM(precipitacao) as precipitacao
FROM weather_data
GROUP BY codigo_estacao, DATE(data);