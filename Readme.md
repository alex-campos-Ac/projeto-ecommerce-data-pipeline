# 📊 DataCommerce — End-to-End Sales & E-Commerce Analytics Pipeline

![DataCommerce Dashboard](https://raw.githubusercontent.com/placeholder/datacommerce-dashboard.png)

## 📌 Visão Geral do Projeto

O **DataCommerce** é um projeto completo (*end-to-end*) de engenharia e análise de dados focado na consolidação, tratamento, modelagem e visualização de indicadores comerciais para e-commerce. 

A solução transforma dados transacionais brutos em um **painel executivo de alto impacto (Dark Mode UI)**, permitindo à gestão monitorar o faturamento, identificar gargalos operacionais e direcionar tomadas de decisão estratégicas.

---

## 🚀 Arquitetura & Stack de Tecnologias

A pipeline do projeto seguiu as etapas do fluxo moderno de dados:

```
[ Dados Brutos ] ➔ [ Python (ETL) ] ➔ [ SQL Database (Views) ] ➔ [ Power BI (Star Schema & DAX) ]
```

| Etapa | Tecnologia | Descrição |
| :--- | :--- | :--- |
| **ETL & Tratamento** | `Python` (`pandas`) | Limpeza de *dirty data*, remoção de duplicidades, tratamento de nulos e padronização de tipos de dados. |
| **Modelagem & Armazenamento** | `SQL Server` / `PostgreSQL` | Criação de tabelas relacionais e *Views* analíticas otimizadas para consumo direto na camada de BI. |
| **Modelagem Dimensional & DAX** | `Power BI` | Arquitetura *Star Schema* (Tabelas Fato e Dimensões) e cálculos de métricas avançadas em DAX (*Time Intelligence MoM*). |
| **UI/UX & Design Executivo** | `Figma` / `SVG` | Layout moderno em *Dark Mode*, ícones neon em transparência e *badges* dinâmicos via SVG. |

---

## 📈 Indicadores Chave (KPIs) & Métricas

- **Receita Total (R$):** Faturamento acumulado no período e variação percentual mês a mês (*Month-over-Month*).
- **Quantidade de Pedidos:** Volume total de transações processadas.
- **Ticket Médio (R$):** Razão entre a Receita Total e a Quantidade de Pedidos.
- **Taxa de Cancelamento (%):** Percentual de pedidos cancelados frente ao total de vendas.

---

## 💡 Principais Diagnósticos de Negócio

A análise dos dados consolidados no dashboard revelou três achados estratégicos para a operação:

1. **Risco de Dependência do Portfólio:** 
   - A categoria de **Eletrônicos** domina o faturamento global.
   - O produto **Notebook Pro** sozinho representa **65,3% da receita total**, sinalizando a necessidade de diversificação das estratégias de vendas.

2. **Gargalo de Operação e Qualidade (Cancelamentos):**
   - A taxa geral de cancelamento é de **10,11%**.
   - As categorias **Eletrônicos (11,09%)** e **Acessórios (10,65%)** lideram o volume de devoluções, apontando prioridade para revisão logística e controle de qualidade.

3. **Análise Temporais MoM:**
   - Acompanhamento dinâmico do comportamento de crescimento (% MoM) em comparação direta com o mês anterior.

---

## 🛠️ Como Executar o Projeto

### Pré-requisitos
* Python 3.x
* SQL Server ou PostgreSQL
* Power BI Desktop

### Passos
1. **Clonar o Repositório:**
   ```bash
   git clone https://github.com/seu-usuario/datacommerce-analytics.git
   cd datacommerce-analytics
   ```

2. **Executar a Pipeline de Tratamento (Python):**
   ```bash
   python scripts/etl_vendas.py
   ```

3. **Criação do Banco de Dados & Views (SQL):**
   Execute o script `sql/create_views.sql` no seu SGDB para estruturar a view `vw_vendas_consolidadas`.

4. **Abrir o Dashboard (Power BI):**
   Abra o arquivo `pbix/DataCommerce_Dashboard.pbix` e atualize a fonte de dados para conectar ao seu banco/view local.

---

## ✒️ Autor

Desenvolvido por **Seu Nome**  
* [LinkedIn](https://linkedin.com/in/seu-perfil) | [GitHub](https://github.com/seu-usuario)