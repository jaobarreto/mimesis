# MKB-REA · Conhecimento de raciocínio

**Proposta arquitetural.** Guardar regras e casos declarativos que sustentem conclusões locais e rastreáveis. Uma conclusão derivada pertence à interpretação do motor. Fatos fornecidos pelo integrador permanecem identificáveis por sua própria origem.

## 1. Finalidade

Documentar o caminho entre premissas observáveis e uma recomendação interpretativa. Por exemplo, a ausência declarada de um dado necessário pode sustentar uma conclusão de que é preciso pedir esclarecimento.

## 2. Escopo

Regras simbólicas, casos comparáveis, condições de aplicação, exceções e justificativas. Eventuais modelos probabilísticos precisam de evidência e avaliação próprias. Esta especificação inicial não atribui probabilidades por conveniência editorial.

## 3. Responsabilidades

Explicitar premissas, conclusão, natureza do vínculo e limites de uso. Preservar o encadeamento de evidências, reconhecer conflitos e impedir inferências que criem fatos externos ou transformem coincidências de linguagem em causas.

## 4. Tipos de conhecimento

`rule` especifica condição e conclusão. `case` registra uma situação revisada com sinais pertinentes, interpretação e limites de analogia. Uma regra determinística e um caso recuperado devem ser distinguíveis na explicação ao consumidor.

## 5. Estrutura dos registros

Uma regra requer `premises`, operador de composição em `operator`, `conclusion` de vocabulário declarado e `rationale`. Predicados referenciam CTX. Casos descrevem `features`, `outcome` e condições de transferência. O fragmento abaixo ilustra uma regra com duas premissas fictícias.

```json
{"kind":"rule","operator":"all","premises":["c11","c12"],"conclusion":"clarification_needed","rationale":"A solicitação depende de um referente e sua ausência foi confirmada."}
```

## 6. Relações entre entidades

A regra se liga a sinais ou predicados de CTX e pode justificar uma escolha em BEH. Um caso pode citar SEM para descrever um conceito compartilhado. Ausência de valor e uma afirmação positiva sobre sua indisponibilidade devem poder ser representadas distintamente.

## 7. Metadados obrigatórios

Usar o [envelope comum](../METADATA_SPECIFICATION.md). Incluir origem e versão do vocabulário de conclusões, autor da justificativa e escopo da inferência. Origem das premissas instanciadas é registrada na trilha da execução futura.

## 8. Fontes candidatas

Regras autorais e casos construídos a partir de cenários explícitos. Afirmações de um especialista podem ser candidatas com atribuição e revisão. Literatura ficcional é fonte possível de casos interpretativos localizados, com direitos e contexto preservados.

## 9. Importação

Registrar texto da afirmação e versão de origem antes de formalizar. Separar relação condicional, preferência e correlação. Se o enunciado disser “costuma responder”, não o converter automaticamente em regra universal.

## 10. Processamento

Decompor premissas compostas, tipar seus argumentos e produzir um caso positivo, um negativo e um incompleto. Documentar exceções e testar se um caso aparentemente parecido compartilha os atributos relevantes. A seleção por similaridade não prova a conclusão.

## 11. Validação

Validar referências, tipo e aridade dos operadores, vocabulário das conclusões e término da avaliação definida pelo perfil. Para a primeira proposta, preferir regras sem recursão e rejeitar ciclos de dependência. Conclusões incompatíveis devem provocar conflito identificável ou abstenção segundo política publicada.

## 12. Indexação

Propor índices reversos por premissa e por conclusão, além de chaves de atributos dos casos. A recuperação de casos retorna possíveis analogias e mantém a lista de atributos correspondentes e divergentes.

## 13. Utilização pelo motor

O módulo de raciocínio poderá retornar conclusão, regra, evidências e resultado de cada teste. BEH poderá considerar essa conclusão ao selecionar uma resposta. No exemplo, a direção da regra impede inferir de uma pergunta de esclarecimento isolada que um referente estava ausente.

## 14. Versionamento

Alteração de premissa, operador ou prioridade modifica o comportamento e demanda nova revisão. Avaliar alcance direto e transitivo sobre regras e cenários de teste. Manter a explicação reproduzível para a versão efetivamente executada.

## 15. Limitações

Conjuntos de regras podem conter conflitos ou não cobrir casos novos. Mundo aberto e dado ausente exigem tratamento explícito. Inferências sobre causalidade ou intenção dependem de evidência adicional.

## 16. Critérios de qualidade

Exigir uma trilha completa por conclusão nos casos de aceitação. Medir cobertura de premissas e das ramificações de conflito, falsos positivos nos negativos próximos e abstenções no conjunto incompleto. Uma regra que passa apenas por concordar com o próprio exemplo de autoria ainda precisa de avaliação independente.
