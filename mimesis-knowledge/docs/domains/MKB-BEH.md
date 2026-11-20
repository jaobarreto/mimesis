# MKB-BEH · Conhecimento comportamental

**Proposta arquitetural.** Representar alternativas de expressão ou reação comunicativa sob condições explícitas. Uma alternativa pode gerar uma fala ou descrever uma reação ficcional autorizada. Alterar o estado de um sistema externo requer decisão desse sistema.

## 1. Finalidade

Separar a escolha de uma reação, como pedir esclarecimento, da frase exata que a realiza. Isso permite investigar por que a mesma persona age de forma diferente diante de uma informação presente ou ausente.

## 2. Escopo

Atos de diálogo, respostas expressivas e políticas curadas de elegibilidade. O domínio pode descrever candidatos e preferências. A execução externa de ações, a criação de eventos objetivos e as regras específicas de um jogo pertencem ao integrador.

## 3. Responsabilidades

Declarar precondições, tipo de reação, realizadores elegíveis e modo de abstenção. Distinguir condições obrigatórias de preferências em empates. Conservar uma explicação legível para cada vínculo entre condição e comportamento.

## 4. Tipos de conhecimento

Um `behavior` descreve uma reação reutilizável. Exemplos de classes são `ask_clarification`, `acknowledge` e `express_uncertainty`. A execução de uma árvore de comportamento ou de uma política de utilidade é uma investigação futura do motor.

## 5. Estrutura dos registros

Um registro requer `act`, `requires` (referências a predicados), `realizations` (referências a Talksets ou modelos compatíveis) e `effect_scope`. Na proposta inicial, `output_only` limita o efeito à expressão emitida. Uma lista vazia de guardas requer justificativa para uso universal.

```json
{"kind":"behavior","act":"ask_clarification","requires":["c42"],"realizations":[{"talkset_id":"d19"}],"effect_scope":"output_only"}
```

O predicado hipotético `c42` afirmaria que faltou um referente necessário e que um pedido de esclarecimento é pertinente nesta interação.

## 6. Relações entre entidades

Uma reação referencia CTX para elegibilidade e DLG ou NAR para realização. PSY pode modular a preferência entre alternativas já habilitadas. REA pode fornecer uma conclusão local explicitamente identificada. A ligação a um Talkset tem como alvo seu `record_id`.

## 7. Metadados obrigatórios

Aplicar o [envelope comum](../METADATA_SPECIFICATION.md), informar finalidade do ato, revisão das guardas, autoridade dos sinais e evidência que sustenta a realização. Registrar o escopo de efeito em todos os comportamentos de uso operacional.

## 8. Fontes candidatas

Cenários autorais controlados e pares contrastivos. Reações extraídas de narrativa literária ou diálogo externo podem inspirar hipóteses desde que o item e a transformação sejam elegíveis. Um comportamento descrito em literatura não fornece por si uma política geral.

## 9. Importação

Separar situação anterior, comportamento observado e consequência narrada. Importar cada elemento como candidato com origem. Se o antecedente for apenas inferido, manter esse fato visível ao revisor.

## 10. Processamento

Converter descrições vagas em condições testáveis. Para “perguntou de novo porque não entendeu”, distinguir o ato observável de pedir esclarecimento da eventual inferência sobre compreensão. Construir um caso vizinho em que o referente já esteja disponível.

## 11. Validação

Todas as guardas e realizações devem resolver no manifesto e ter tipo compatível. Proibir referências a operações externas como efeitos do registro. Testar guardas satisfeitas, falsas e desconhecidas. Se duas reações forem elegíveis, o registro descreve alternativas e permite que o consumidor explique sua escolha.

## 12. Indexação

Índices invertidos por ato, predicado e `effect_scope`. Manter dependentes de cada guarda para facilitar revisão. Só pré-calcular combinações quando houver evidência de que o ganho compensa o crescimento do índice.

## 13. Utilização pelo motor

Em Context ou Anima, o motor avalia guardas, identifica alternativas e seleciona uma realização sob a política declarada. Ao escolher “pedir esclarecimento”, pode emitir uma pergunta. Isso não modifica a entidade ou fato a esclarecer.

## 14. Versionamento

Mudança nas guardas altera o conjunto de situações elegíveis e exige nova revisão, testes contrafactuais e reavaliação dos consumidores. Divisão de um ato amplo em dois atos especializados cria identidades distintas e mapa de migração.

## 15. Limitações

Um mesmo gesto pode realizar vários atos, e explicações literárias sobre motivação podem ser ambíguas. Políticas repetitivas podem pedir esclarecimento em ciclos mesmo quando cada turno isolado parece válido.

## 16. Critérios de qualidade

Verificar zero realizações com guarda obrigatória falsa nos casos de aceitação, coerência entre ato e resposta e cobertura dos caminhos de abstenção. Medir repetição em sequências curtas e revisar situações em que o comportamento reforça uma inferência sem evidência.
