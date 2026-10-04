USE db_ecommerce;
GO

-- 1. Teste de Duplicidade: Verificar se existe algum pedido duplicado (Esperado: 0 linhas)
SELECT 
    pedido_id, 
    COUNT(*) AS total_ocorrencias
FROM fato_pedidos
GROUP BY pedido_id
HAVING COUNT(*) > 1;

-- 2. Teste de Nulos: Verificar se restou alguma receita nula ou zerada em pagamentos APROVADOS (Esperado: 0 linhas)
SELECT 
    pagamento_id, 
    status_pagamento, 
    valor_receita
FROM fato_pagamentos
WHERE status_pagamento = 'APROVADO' 
  AND (valor_receita IS NULL OR valor_receita = 0);

-- 3. Identificação do Desvio dos 8%: Pagamentos APROVADOS cujo pedido ainda consta como PENDENTE
SELECT 
    ped.pedido_id,
    ped.status_pedido,
    pag.status_pagamento,
    pag.valor_receita
FROM fato_pedidos ped
INNER JOIN fato_pagamentos pag ON ped.pedido_id = pag.pedido_id
WHERE pag.status_pagamento = 'APROVADO' 
  AND ped.status_pedido = 'PENDENTE';