# MKB-CTX · Conhecimento contextual

**Proposta arquitetural.** Catalogar os sinais que uma aplicação pode fornecer e os predicados que a seleção pode consultar. O significado de um sinal é versionável. O valor observado num momento pertence à execução e à autoridade que o forneceu.

## 1. Finalidade

Permitir que duas aplicações representem o mesmo tipo de circunstância por um contrato explícito, preservando a distinção entre um fato informado, uma negação e a ausência de informação.

## 2. Escopo

Definições de campos contextuais, tipos, unidades, valor desconhecido, origem autorizada, validade e predicados de elegibilidade. O contrato deve poder representar entidades fornecidas por qualquer integrador sem incorporar as regras particulares de sua aplicação.

## 3. Responsabilidades

Documentar significado, unidade e domínio de cada sinal. Definir como o consumidor trata um dado vencido, conflitante ou ausente. O integrador retém a autoridade para fornecer ou atualizar os fatos objetivos.

## 4. Tipos de conhecimento

`signal` descreve um campo de entrada. `predicate` descreve uma comparação pura sobre sinais e literais tipados. Escopos possíveis incluem enunciado atual, turno ou contexto externo. Um cadastro de predicados não dá à MKB acesso a sessões de usuários.

## 5. Estrutura dos registros

Para `signal`, requerer `key`, `value_type`, `scope`, `authority` e política `missing`. Para `predicate`, identificar o sinal em `signal_id`, o operador, os operandos e a política para valor desconhecido. Nomes de chaves são distintos da identidade opaca do registro.

```json
{"kind":"signal","key":"room_lit","value_type":"boolean","scope":"external_context","authority":"caller","missing":"unknown"}
```

## 6. Relações entre entidades

Um predicado pode ser reutilizado por BEH, NAR ou REA. Um modelo narrativo que afirme luminosidade depende de um fato atualmente válido. Um perfil PSY pode afetar a expressão, mas não muda o sinal `room_lit`. A identidade de uma ocorrência contextual pertence à entrada do motor.

## 7. Metadados obrigatórios

Aplicar o [envelope comum](../METADATA_SPECIFICATION.md) e registrar origem da convenção, versão do inventário de tipos e responsável pela autoridade declarada. Indicar unidade, validade e política de ausência sempre que pertinentes. O idioma descreve as anotações textuais do perfil.

## 8. Fontes candidatas

Contratos autorais de integração, pares de cenários sintéticos e anotações de corpus sobre o contexto explicitado, após revisão. Um conjunto externo pode sugerir um conceito sem definir sua semântica para todas as aplicações MIMESIS.

## 9. Importação

Receber descrição de campo, tipo, unidade e exemplo fictício. Mapear o vocabulário de origem ao vocabulário estável. Revisar campos com nomes parecidos e significados distintos, como “claro” significando luminosidade ou clareza de comunicação.

## 10. Processamento

Normalizar unidades com transformações documentadas. Especificar tabela ternária para predicados críticos. Para `room_lit == true`, os resultados propostos são verdadeiro se o valor é verdadeiro, falso se é falso e desconhecido se faltar ou já não for válido. Uma exigência positiva só admite o primeiro caso.

## 11. Validação

Verificar tipo e autoridade do sinal, compatibilidade de operadores e política de expiração. Testar `false`, ausência, `null` quando previsto, tipo errado e fonte contraditória. O consumidor deve distinguir rejeição do contrato de entrada de mera inelegibilidade de um candidato.

## 12. Indexação

Indexar por chave, tipo e escopo. Manter referência reversa dos predicados a seus sinais para análise de impacto. Para um contexto instanciado, a implementação futura pode resolver as chaves em memória durante a requisição.

## 13. Utilização pelo motor

Context poderá excluir respostas com fatos não sustentados e registrar o resultado de cada predicado. Mythos pode selecionar realizadores compatíveis. Uma trilha pode indicar chave e resultado derivado preservando limites de privacidade dos valores de sessão.

## 14. Versionamento

Alterar `room_lit` de booleano para uma medida de iluminância muda o contrato e requer migração ou identidade distinta. Adicionar uma forma de expressar ausência exige rever predicados que supunham apenas dois estados. Registrar a versão da aplicação no experimento quando sua codificação afetar o dado.

## 15. Limitações

Integrações podem apresentar fatos contraditórios ou incompletos. Regras temporais exigem um relógio ou ordenação fornecida pelo ambiente. A ausência de um dado não autoriza inferir seu oposto.

## 16. Critérios de qualidade

Exigir simetria dos testes contrafactuais para verdadeiro, falso e desconhecido, estado observável em decisões e rastreabilidade da autoridade. Medir decisões que afirmam fato sem evidência, cobertura de abstenção e divergências por integração.
