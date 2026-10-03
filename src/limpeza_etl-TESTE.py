import os
import pandas as pd


def executar_etl():
    # 1. Carregar os dados brutos
    pasta_data = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"
    )

    df_produtos = pd.read_csv(os.path.join(pasta_data, "dim_produtos.csv"))
    df_pedidos = pd.read_csv(os.path.join(pasta_data, "fato_pedidos_bruto.csv"))
    df_pagamentos = pd.read_csv(
        os.path.join(pasta_data, "fato_pagamentos_bruto.csv")
    )

    print("--- INICIANDO PROCESSAMENTO DE ETL ---")
    print(
        f"Linhas iniciais - Pedidos: {len(df_pedidos)} | Pagamentos: {len(df_pagamentos)}"
    )

    # 2. Padronização de Tipos de Dados (Datas)
    df_pedidos["data_pedido"] = pd.to_datetime(df_pedidos["data_pedido"])
    df_pagamentos["timestamp_transacao"] = pd.to_datetime(
        df_pagamentos["timestamp_transacao"]
    )

    # 3. Tratamento de Duplicidades
    # Regra: Manter apenas o primeiro registro considerando a chave e o timestamp
    df_pedidos = df_pedidos.drop_duplicates(
        subset=["pedido_id", "data_pedido"], keep="first"
    )
    df_pagamentos = df_pagamentos.drop_duplicates(
        subset=["pagamento_id", "timestamp_transacao"], keep="first"
    )

    print(
        f"Após remoção de duplicados - Pedidos: {len(df_pedidos)} | Pagamentos: {len(df_pagamentos)}"
    )

    # 4. Tratamento de Nulos na Receita
    # Merge com pedidos e produtos para recuperar o preço unitário quando necessário
    df_pag_merged = df_pagamentos.merge(
        df_pedidos[["pedido_id", "produto_id", "quantidade"]],
        on="pedido_id",
        how="left",
    ).merge(
        df_produtos[["produto_id", "preco_unitario"]],
        on="produto_id",
        how="left",
    )

    # Aplicando regras de negócio nos nulos:
    def corrigir_receita(row):
        if pd.isna(row["valor_receita"]):
            if row["status_pagamento"] in ["REEMBOLSADO", "CANCELADO"]:
                return 0.0
            elif row["status_pagamento"] == "APROVADO":
                return row["quantidade"] * row["preco_unitario"]
        return row["valor_receita"]

    df_pag_merged["valor_receita"] = df_pag_merged.apply(
        corrigir_receita, axis=1
    )

    # Limpando colunas auxiliares do merge
    df_pagamentos_limpo = df_pag_merged[
        [
            "pagamento_id",
            "pedido_id",
            "status_pagamento",
            "valor_receita",
            "timestamp_transacao",
        ]
    ]

    # 5. Validação de Qualidade de Dados (Sanity Checks)
    duplicados_restantes = df_pagamentos_limpo.duplicated(
        subset=["pagamento_id"]
    ).sum()
    nulos_restantes = df_pagamentos_limpo["valor_receita"].isnull().sum()

    print("\n--- CHECKLIST DE VALIDAÇÃO ---")
    print(f"Duplicados em pagamentos: {duplicados_restantes} (Esperado: 0)")
    print(f"Nulos em receita: {nulos_restantes} (Esperado: 0)")

    # 6. Salvar Dados Saneados
    pasta_saneados = os.path.join(pasta_data, "saneados")
    os.makedirs(pasta_saneados, exist_ok=True)

    df_pedidos.to_csv(
        os.path.join(pasta_saneados, "fato_pedidos_limpo.csv"), index=False
    )
    df_pagamentos_limpo.to_csv(
        os.path.join(pasta_saneados, "fato_pagamentos_limpo.csv"), index=False
    )

    print(
        f"\nBase limpa salva com sucesso em: {pasta_saneados}\n--- ETL FINALIZADO ---"
    )


if __name__ == "__main__":
    executar_etl()