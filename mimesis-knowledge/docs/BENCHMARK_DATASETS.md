# Contrato dos conjuntos de avaliação

**Proposta para o primeiro benchmark pt-BR.** Congelar separadamente o repertório que o motor poderá consultar, as consultas que o desafiam e os julgamentos de relevância. O catálogo de respostas precisa conter respostas válidas para casos conhecidos. O texto da consulta de teste e suas variantes reservadas não podem participar de índices, expansão lexical, treino, seleção de exemplos ou calibração de limiares.

| Artefato | Campos mínimos | Consumidor |
|---|---|---|
| Consultas | `query_id`, `text`, `language`, `group_id`, `split`, `scenario_id` | O executor recebe somente `query_id`, texto, idioma e fatos públicos do cenário. A alocação de grupos fica no controlador da avaliação. |
| Gabarito da consulta | `query_id`, `expected_class`, justificativa e decisão adjudicada | Acesso exclusivo do avaliador. Classes propostas: `answerable`, `unknown` e `ambiguous`. |
| Julgamentos | `query_id`, `talkset_id`, `revision`, `response_id`, `grade`, `reviewer_id`, `rationale`, `adjudication` | Avaliação cega. Pode haver várias respostas aceitáveis. |
| Grupos | `group_id`, fontes/obras/sessões vinculadas, método de deduplicação e revisões | Auditor de vazamento. |
| Manifesto da avaliação | versão, digest de cada artefato, versão do repertório, partição e procedimento de amostragem | Reprodução com a mesma população e catálogo. |

1. Atribuir famílias de origem e autoria, obra/edições, conversa e paráfrases. Construir ligações de equivalência com hashes de forma normalizada e vizinhos por n-gramas, mais revisão humana de candidatos próximos e de amostra dos não sinalizados. Os componentes conectados permanecem inteiros em `train`, `dev` ou `test`. Registrar exceções diagnósticas antecipadamente.
2. Criar consultas naturais novas por pessoas diferentes quando possível, com erros de digitação, ausência de acento, negação, paráfrases e temas fora da base. Buscar semelhança também contra os prompts indexados. Colisões conhecidas podem integrar um conjunto diagnóstico de igualdade exata, reportado à parte das métricas de generalização.
3. Associar respostas aceitáveis ou conjunto vazio após dupla revisão cega e adjudicação. Documentar cobertura de julgamentos, incluindo candidatos obtidos por diferentes métodos. Um item sem julgamento continua indeterminado. A autoridade externa decide se o fato do cenário está correto.
4. Ajustar recuperadores e limiares em `dev`, congelar política e abrir o teste para uma comparação registrada. Quando a equipe usa os erros do teste para orientar mudanças, preservar o histórico e reservar novo conjunto para confirmação.
5. Distribuir apenas os componentes autorizados. O acesso às respostas de avaliação é distinto do acesso ao repertório normal. Registrar quem liberou, quais grupos foram excluídos, sobreposições residuais e população sub-representada.

**Exemplo de julgamento didático.** Diante de “Podemos iniciar?”, réplicas autorais equivalentes a aceitar o início podem receber grau 2 (apropriada). Uma pergunta de esclarecimento pode receber grau 1 (parcial). Uma afirmação sobre evento que o cenário omite recebe 0. A rubrica proposta de Genesis considera grau 2 relevante para métricas binárias e separa o grau 1 para análise. Uma pergunta cuja resposta dependa de fato ausente é um caso próprio de abstenção. Para consulta `unknown` ou `ambiguous` pode haver gabarito sem linha de resposta apropriada. A abstenção correta tem motivo verificável. Uma pergunta de esclarecimento curada também pode ser julgada como resposta conhecida quando esse for o alvo estabelecido previamente.

O texto de uma obra é uma evidência linguística. Reutilizá-lo em perguntas e respostas de teste exige autorização e controle de família. [Medição no motor](../../mimesis/docs/EVALUATION.md) · [Curadoria](CURATION_GUIDELINES.md)
