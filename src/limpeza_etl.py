import os
import  pandas as pd

# Configuração global
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Cria o caminho individual para cada CSV na pasta 'data'
caminho_produtos = os.path.join(base_dir, "data", "dim_produtos.csv")
caminho_pagamentos = os.path.join(base_dir, "data", "fato_pagamentos_bruto.csv")
caminho_pedidos_bruto = os.path.join(base_dir, "data", "fato_pedidos_bruto.csv")

# Teste de verificação simples
print("Produtos existe?", os.path.exists(caminho_produtos))
print("Pagamentos existe?", os.path.exists(caminho_pagamentos))
print("Pedidos existe?", os.path.exists(caminho_pedidos_bruto))