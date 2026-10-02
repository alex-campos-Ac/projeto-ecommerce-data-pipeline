import os
import random
from datetime import datetime, timedelta
import numpy as np
import pandas as pd


def gerar_base_ecommerce(num_registros=1000):
    np.random.seed(42)
    random.seed(42)

    data_inicial = datetime(2026, 1, 1)

    # 1. Tabela Dimensão Produtos
    produtos = [
        {"produto_id": 101, "nome": "Notebook Pro", "preco_unitario": 4500.00},
        {"produto_id": 102, "nome": "Mouse Sem Fio", "preco_unitario": 120.00},
        {"produto_id": 103, "nome": "Teclado Mecanico", "preco_unitario": 350.00},
        {"produto_id": 104, "nome": "Monitor 27 Pulg", "preco_unitario": 1800.00},
    ]
    df_produtos = pd.DataFrame(produtos)

    # 2. Tabela Fato Pedidos
    pedidos = []
    for i in range(1, num_registros + 1):
        prod = random.choice(produtos)
        qtd = random.randint(1, 3)
        data_pedido = data_inicial + timedelta(
            days=random.randint(0, 180), minutes=random.randint(0, 1440)
        )

        pedidos.append(
            {
                "pedido_id": f"PED-{i:05d}",
                "produto_id": prod["produto_id"],
                "quantidade": qtd,
                "data_pedido": data_pedido.strftime("%Y-%m-%d %H:%M:%S"),
                "status_pedido": random.choice(
                    ["PENDENTE", "PROCESSANDO", "ENVIADO", "CANCELADO"]
                ),
            }
        )

    df_pedidos = pd.DataFrame(pedidos)

    # 3. Tabela Fato Pagamentos
    pagamentos = []
    for idx, row in df_pedidos.iterrows():
        # Regra normal: 90% aprovado, 10% recusado/reembolsado
        if row["status_pedido"] == "CANCELADO":
            status_pag = "REEMBOLSADO"
            valor = 0.0
        else:
            status_pag = (
                "APROVADO" if random.random() > 0.1 else "AGUARDANDO_PAGAMENTO"
            )
            # Buscar preco do produto
            preco = df_produtos.loc[
                df_produtos["produto_id"] == row["produto_id"], "preco_unitario"
            ].values[0]
            valor = preco * row["quantidade"]

        pagamentos.append(
            {
                "pagamento_id": f"PAG-{idx+1:05d}",
                "pedido_id": row["pedido_id"],
                "status_pagamento": status_pag,
                "valor_receita": valor,
                "timestamp_transacao": row["data_pedido"],
            }
        )

    df_pagamentos = pd.DataFrame(pagamentos)

    # --- INSERINDO INCONSISTÊNCIAS PROPOSITARAIS ---

    # A) Duplicidades (simulando duplo clique / erro de webhook)
    duplicados_pedidos = df_pedidos.sample(n=40, random_state=42)
    duplicados_pagamentos = df_pagamentos[
        df_pagamentos["pedido_id"].isin(duplicados_pedidos["pedido_id"])
    ]

    df_pedidos = pd.concat([df_pedidos, duplicados_pedidos], ignore_index=True)
    df_pagamentos = pd.concat(
        [df_pagamentos, duplicados_pagamentos], ignore_index=True
    )

    # B) Valores Nulos em Receita (onde o pagamento foi aprovado)
    idx_nulos = df_pagamentos[
        df_pagamentos["status_pagamento"] == "APROVADO"
    ].sample(n=30, random_state=42).index
    df_pagamentos.loc[idx_nulos, "valor_receita"] = np.nan

    # C) Desnivelamento dos 8% (Pagamento APROVADO, mas Pedido continua PENDENTE)
    idx_desnivel = df_pagamentos[
        df_pagamentos["status_pagamento"] == "APROVADO"
    ].sample(n=80, random_state=99).index
    pedidos_desnivelados = df_pagamentos.loc[idx_desnivel, "pedido_id"]
    df_pedidos.loc[
        df_pedidos["pedido_id"].isin(pedidos_desnivelados), "status_pedido"
    ] = "PENDENTE"

    # Salvar arquivos CSV na pasta data/
    os.makedirs("data", exist_ok=True)
    df_produtos.to_csv("data/dim_produtos.csv", index=False)
    df_pedidos.to_csv("data/fato_pedidos_bruto.csv", index=False)
    df_pagamentos.to_csv("data/fato_pagamentos_bruto.csv", index=False)

    print("Datasets brutos gerados com sucesso na pasta 'data/'!")


if __name__ == "__main__":
    gerar_base_ecommerce()