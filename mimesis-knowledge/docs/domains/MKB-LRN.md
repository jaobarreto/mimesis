# MKB-LRN · Conhecimento de aprendizagem supervisionada

**Decisão aprovada.** A evolução do repertório passa por supervisão humana e verificação de regressões. **Proposta arquitetural.** Tratar a avaliação recebida e a edição resultante como entidades distintas. Uma execução não altera sozinha os dados publicados.

## 1. Finalidade

Permitir que uma equipe investigue um erro, proponha uma correção e reavalie o resultado sem perder o comportamento e o conhecimento originalmente observados. Sophia é o marco de aprendizagem supervisionada do motor.

## 2. Escopo

Julgamentos de relevância, preferências entre realizações, correções propostas, desacordos e decisões de adjudicação. O histórico de uma execução privada só pode originar evidência quando sua coleta, finalidade e retenção tiverem sido autorizadas.

## 3. Responsabilidades

Preservar alvo e revisão avaliados, rubrica, origem do julgamento e divisão experimental. Impedir que exemplos de teste conhecidos orientem diretamente edição ou treino com posterior reutilização do mesmo teste como evidência independente.

## 4. Tipos de conhecimento

`judgment` registra rótulo de uma avaliação. `preference` compara alternativas para a mesma entrada e contexto. `correction` propõe uma mudança e a vincula ao erro. `adjudication` referencia avaliações divergentes e explicita a decisão humana.

## 5. Estrutura dos registros

Um julgamento requer `target` com `record_id` e `revision`, identificação de membro quando aplicável, `rubric_id`, `criterion`, `label`, `reason` e `case_id`. O caso fixa entrada, contexto e condições de avaliação permitidas. No exemplo fictício, o grupo alvo é um Talkset e seu `record_id` exerce o papel de `talkset_id`.

```json
{"kind":"judgment","target":{"record_id":"d23","revision":2,"response_id":"r08"},"case_id":"q15","rubric_id":"u32","criterion":"factual_fidelity","label":"fail","reason":"A resposta descreve uma janela aberta sem esse fato no caso."}
```

## 6. Relações entre entidades

Vários julgamentos independentes podem apontar para o mesmo alvo e caso. A adjudicação aponta para os julgamentos originais. Quando uma correção for aprovada, a nova revisão em DLG, NAR ou outro domínio referencia a evidência autorizada. Um julgamento pode permanecer válido historicamente mesmo após a retirada do alvo de uso operacional.

## 7. Metadados obrigatórios

Aplicar o [envelope comum](../METADATA_SPECIFICATION.md). Exigir identificação pseudonimizada de função/revisor quando adequada, data da avaliação, revisão da rubrica, família experimental e partição do caso. Se a resposta veio de execução, registrar ou resolver versão do motor, MKB, configuração e trilha autorizada.

## 8. Fontes candidatas

Casos autorais reservados para desenvolvimento, oficinas supervisionadas da equipe e feedback consentido para a finalidade documentada. Dados externos com preferências ou avaliações exigem revisão de direitos e de equivalência da rubrica. [Governança](../DATA_GOVERNANCE.md)

## 9. Importação

Receber somente os campos autorizados e separar chaves de identificação pessoal do conjunto editorial. Registrar qual versão foi mostrada e se o anotador teve acesso à identidade do sistema. Feedback sem contexto suficiente pode ser registrado como pendência, sem converter a afirmação em rótulo validado.

## 10. Processamento

Agrupar duplicações por família de caso, preservar opiniões originais e criar adjudicação com motivo. Distinguir “resposta incorreta”, “resposta correta mas pouco natural” e “não há informação para julgar”. Reservar reversões de uma correção para histórico, com referência ao motivo.

## 11. Validação

O alvo e sua revisão precisam ser recuperáveis, assim como o membro julgado, a rubrica e a entrada avaliada. Proibir um mesmo grupo de paráfrases em partições incompatíveis. Uma correção derivada de teste exposto exige marcar a exposição e reservar outros casos para a próxima avaliação independente.

## 12. Indexação

Índices por alvo/revisão, rubrica, critério, família e partição. Restringir acesso ao conteúdo de teste e impedir sua projeção no índice usado para responder. Pesquisas agregadas devem explicitar se contam julgamentos, casos ou famílias distintas.

## 13. Utilização pelo motor

Sophia poderá encaminhar sugestões para revisão e testar a nova seleção contra o baseline congelado. O motor em operação consome a release publicada. A aprovação de um rótulo isolado não instala uma correção.

## 14. Versionamento

Uma rubrica alterada recebe versão identificável e requer análise de comparabilidade. Retificação de julgamento produz nova revisão ou adjudicação, preservando o registro original quando permitido. Uma correção aceita exige versão e rastreio no domínio afetado.

## 15. Limitações

Feedback voluntário pode super-representar casos problemáticos. Repetir a mesma pergunta a vários revisores aumenta o número de julgamentos, mas a unidade de generalização pode continuar sendo apenas uma família de casos.

## 16. Critérios de qualidade

Auditar separação de partições, links para alvos e instruções de anotação. Relatar distribuição de classes, desacordos e efeito da correção sobre as capacidades anteriores em amostra independente. [Benchmarks](../BENCHMARK_DATASETS.md) e [curadoria](../CURATION_GUIDELINES.md).
