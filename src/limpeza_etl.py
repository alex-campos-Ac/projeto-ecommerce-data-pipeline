import os
import pandas as pd

# 1. Pega a pasta atual do arquivo
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# 2. Sobe um nível para a raiz do projeto
base_dir = os.path.dirname(diretorio_atual)

# 3. Entra diretamente na pasta 'data' dentro da raiz
pasta_data = os.path.join(base_dir, "data")

# 4. Lê os arquivos CSV
df_produtos = pd.read_csv(os.path.join(pasta_data, "dim_produtos.csv"))
df_pedidos = pd.read_csv(os.path.join(pasta_data, "fato_pedidos_bruto.csv"))
df_pagamentos = pd.read_csv(os.path.join(pasta_data, "fato_pagamentos_bruto.csv"))


# Convertendo para datetime
df_pedidos ['data_pedido'] = pd.to_datetime(df_pedidos['data_pedido'])
df_pagamentos ['timestamp_transacao'] = pd.to_datetime(df_pagamentos['timestamp_transacao'])

# 3. Tratamento de Duplicidades
# Regra: Manter apenas o primeiro registro considerando a chave e o timestamp
df_pedidos = df_pedidos.drop_duplicates (subset=["pedido_id", "data_pedido"], keep="first")
df_pagamentos = df_pagamentos.drop_duplicates (subset=["pagamento_id", "timestamp_transacao"], keep="first")

print("--- DADOS CARREGADOS COM SUCESSO ---")
print(f"Total de pedidos brutos: {len(df_pedidos)}")
print(f"Total de pagamentos brutos: {len(df_pagamentos)}")


# 1. Traz 'produto_id' e 'quantidade' de df_pedidos para df_pagamentos
df_pag_merged = df_pagamentos.merge(
    df_pedidos[["pedido_id", "produto_id", "quantidade"]],
    on="pedido_id",
    how="left",
)

# 2. Traz 'preco_unitario' de df_produtos
df_pag_merged = df_pag_merged.merge(
    df_produtos[["produto_id", "preco_unitario"]],
    on="produto_id",
    how="left",
)

# Aplicando regras de negócio nos nulos:
def corrigir_receita(linha):
    # Se o valor for Nulo (NaN)
    if pd.isna(linha["valor_receita"]):
        if linha["status_pagamento"] in ["REEMBOLSADO", "CANCELADO"]:
            return 0.0
        elif linha["status_pagamento"] == "APROVADO":
            return linha["quantidade"] * linha["preco_unitario"]
    return linha["valor_receita"]


# Aplica a função no DataFrame usando .apply()
df_pag_merged["valor_receita"] = df_pag_merged.apply(corrigir_receita, axis=1)

# Seleciona apenas as colunas necessárias de volta
df_pagamentos_limpo = df_pag_merged[
    [
        "pagamento_id",
        "pedido_id",
        "status_pagamento",
        "valor_receita",
        "timestamp_transacao",
    ]
]

# Conta quantos nulos sobraram na coluna de receita (Esperado: 0)
nulos_restantes = df_pagamentos_limpo["valor_receita"].isnull().sum()

print("\n--- TRATAMENTO DE NULOS CONCLUÍDO ---")
print(f"Valores nulos restantes na receita: {nulos_restantes}")


# Criar a pasta 'data/saneados' se ela não existir
pasta_saneados = os.path.join(pasta_data, "saneados")
os.makedirs(pasta_saneados, exist_ok=True)

# Salvar os arquivos CSV saneados
df_pedidos.to_csv(
    os.path.join(pasta_saneados, "fato_pedidos_limpo.csv"), index=False
)
df_pagamentos_limpo.to_csv(
    os.path.join(pasta_saneados, "fato_pagamentos_limpo.csv"), index=False
)

print(f"\n--- ARQUIVOS SANEADOS SALVOS EM: {pasta_saneados} ---")