USE db_ecommerce;
GO

-- 1. Tabela Dimensão Produtos
CREATE TABLE dim_produtos (
    produto_id INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL
);

-- 2. Tabela Fato Pedidos
CREATE TABLE fato_pedidos (
    pedido_id VARCHAR(20) PRIMARY KEY,
    produto_id INT NOT NULL,
    quantidade INT NOT NULL,
    data_pedido DATETIME NOT NULL,
    status_pedido VARCHAR(30) NOT NULL,
    CONSTRAINT FK_pedidos_produtos FOREIGN KEY (produto_id) 
        REFERENCES dim_produtos(produto_id)
);

-- 3. Tabela Fato Pagamentos
CREATE TABLE fato_pagamentos (
    pagamento_id VARCHAR(20) PRIMARY KEY,
    pedido_id VARCHAR(20) NOT NULL,
    status_pagamento VARCHAR(30) NOT NULL,
    valor_receita DECIMAL(10,2) NOT NULL,
    timestamp_transacao DATETIME NOT NULL,
    CONSTRAINT FK_pagamentos_pedidos FOREIGN KEY (pedido_id) 
        REFERENCES fato_pedidos(pedido_id)
);
GO


--Adicionando diretamente da pasta

USE db_ecommerce;
GO

-- 1. Importar Produtos
BULK INSERT dim_produtos
FROM 'E:\Estudo Análise de Dados\PROJETOS GITHUB\ENTREVISTA\projeto-ecommerce-data-pipeline\data\dim_produtos.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001' -- UTF-8
);

-- 2. Importar Pedidos
BULK INSERT fato_pedidos
FROM 'E:\Estudo Análise de Dados\PROJETOS GITHUB\ENTREVISTA\projeto-ecommerce-data-pipeline\data\saneados\fato_pedidos_limpo.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001'
);

-- 3. Importar Pagamentos
BULK INSERT fato_pagamentos
FROM 'E:\Estudo Análise de Dados\PROJETOS GITHUB\ENTREVISTA\projeto-ecommerce-data-pipeline\data\saneados\fato_pagamentos_limpo.csv'
WITH (
    FIRSTROW = 2,
    FIELDTERMINATOR = ',',
    ROWTERMINATOR = '\n',
    CODEPAGE = '65001'
);
GO