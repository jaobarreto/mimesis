# MKB-PSY · Conhecimento psicológico ficcional

**Proposta arquitetural.** Descrever personas intercambiáveis como preferências observáveis de expressão. Estados emocionais simulados são convenções narrativas com evidência e duração explícitas. Os perfis pertencem a personagens ou interlocutores ficcionais definidos externamente.

## 1. Finalidade

Permitir que a mesma proposição seja expressa em estilos coerentes e avaliáveis. Por exemplo, uma persona lacônica pode preferir uma resposta breve preservando a mesma informação de uma realização elaborada.

## 2. Escopo

Traços de expressão, perfis, motivações ficcionais e categorias emocionais utilizadas para guiar linguagem. As escalas são locais ao projeto. O domínio não atribui diagnósticos, sentimentos reais de pessoas nem identidades a interlocutores.

## 3. Responsabilidades

Definir cada traço em termos observáveis, distinguir disposição estável de estado transitório e explicitar prioridades em caso de preferências conflitantes. O integrador escolhe o perfil ou informa um estado autorizado. Preferências não substituem fatos externos.

## 4. Tipos de conhecimento

`trait` descreve um eixo de expressão, `profile` uma composição de traços, `emotion_category` um rótulo e suas condições de interpretação, `motivation` uma orientação ficcional declarada. Cada definição deve indicar um exemplo positivo e um limite de interpretação.

## 5. Estrutura dos registros

Um traço requer `key`, definição observável e âncoras de escala. Um perfil contém `traits`, lista de referências aos traços e seus níveis. Na proposta ordinal inicial, `low`, `medium` e `high` só têm sentido pelas âncoras definidas pelo traço. Categorias emocionais descrevem evidência admitida e persistência proposta, sem registrar eventos de sessão no corpus.

```json
{"kind":"profile","traits":[{"trait_id":"t08","level":"high"},{"trait_id":"t31","level":"low"}]}
```

Por hipótese, se `t08` medir preferência por concisão e `t31` preferência por formalidade, a combinação favoreceria frases curtas e informais. A anotação das variantes deve sustentar essa leitura.

## 6. Relações entre entidades

Um perfil agrega vários traços. Um traço pode estar em muitos perfis. BEH relaciona condições a formas de agir e DLG/NAR oferecem realizações variadas. CTX informa a situação. Um trecho LIT com expressão emocional pode fundamentar um rótulo após revisão independente.

## 7. Metadados obrigatórios

Usar o [envelope comum](../METADATA_SPECIFICATION.md), identificando autor da rubrica, idioma e registro, revisão das âncoras e origem dos exemplos. Para emoção, explicitar o agente ficcional que poderia declará-la e os limites de inferência.

## 8. Fontes candidatas

Perfis e pares de realizações criados pela equipe. PersonaChat e LIGHT são candidatos à pesquisa de representação de personas, sujeitos a direitos, idioma e transferência de domínio. Material literário identificado pode fornecer exemplos datados de estilo. [Catálogo](../DATASET_REGISTRY.md)

## 9. Importação

Separar descrições declaradas de um perfil das deduções de um anotador. Preservar ambiguidade e marcas culturais de origem. Só adaptar para pt-BR após analisar autorização, naturalidade e equivalência do contraste a avaliar.

## 10. Processamento

Criar pares mínimos autorais com o mesmo conteúdo factual e mudança de estilo. Para uma descrição de concisão, variar extensão e testar se a frase curta omitiu uma condição essencial. Rotular alterações de conteúdo para excluí-las de comparações de estilo puro.

## 11. Validação

Bloquear níveis fora da escala declarada, traços duplicados no mesmo perfil e rubricas que não permitam diferenciar as âncoras. Testar perfil ausente, combinação conflitante e emoção transitória. A ausência de evidência de um estado não o converte em estado oposto.

## 12. Indexação

Indexar por `trait_id`, nível, perfil e categoria emocional. Para o ranking futuro, preparar identificadores estáveis de afinidade entre traços e variantes. Os pesos do algoritmo pertencem à configuração experimental do motor.

## 13. Utilização pelo motor

Persona poderá escolher entre realizações igualmente válidas. Anima poderá modular a reação emocional sob condições declaradas. Incluir na trilha o perfil, a revisão, os traços usados e a variante escolhida. A fidelidade aos fatos tem precedência sobre a escolha estilística.

## 14. Versionamento

Uma escala redefinida exige revisar os perfis e comparações anteriores. Uma correção editorial de definição pode manter a identidade. Registrar se comparações de versões usam as mesmas âncoras e exemplos equivalentes.

## 15. Limitações

Categorias culturais e emocionais não são universais. Percepção de formalidade depende da situação. Uma preferência por frases curtas não determina, sozinha, personalidade ou intenção.

## 16. Critérios de qualidade

Comparar realizações às cegas com contexto fixo, pedindo julgamentos separados de fidelidade factual e adequação ao perfil. Relatar concordância dos anotadores, empates e indícios de estereotipação. Excluir exemplos que dependam de dados pessoais ou diagnósticos.
