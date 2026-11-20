# Dicionário de dados

Esta proposta distingue a identidade de uma afirmação, a revisão que se pode citar e o artefato em que ela aparece. O esquema de transporte completo, os campos administrativos exigidos e as condições por estágio estão na [especificação de metadados](METADATA_SPECIFICATION.md). As páginas de domínio definem o conteúdo de `payload`. Os tipos abaixo são lógicos, independentes de JSONL ou SQLite.

## Envelope de um registro estruturado

| Campo | Tipo lógico e cardinalidade | Significado e teste |
|---|---|---|
| `record_id` | Identificador textual opaco, 1 | Mantém a identidade nas revisões. Igualdade de texto, título, caminho ou hash não implica igualdade de registros. |
| `revision` | Inteiro positivo, 1 | Junto de `record_id`, identifica o conteúdo revisado. Detectar conteúdo ou referências divergentes sob a mesma chave. O estado projetado pode variar entre instantâneos e é reconstituído do histórico. |
| `domain` | Código, 1 | Um dos dez valores `MKB-*` da taxonomia. Derivação que muda o tipo da afirmação produz um registro relacionado. |
| `schema_version` | Texto com três componentes numéricos, 1 | Determina como interpretar o envelope e o perfil de domínio. Um leitor deve recusar incompatibilidades antes de interpretar dados. |
| `language` | Etiqueta BCP 47, 1 | Idioma do conteúdo representado, conforme o perfil de metadados. `pt-BR` é prioritário. Preservar evidência sobre região, período e conhecimento incompleto. |
| `source_id` | Referência ao catálogo, 1 | Unidade de procedência primária, inclusive autoria própria. Derivações com múltiplas origens identificam todos os antecedentes na procedência. |
| `rights_id` | Referência à decisão de direitos, 1 | Discrimina material/versão, permissões e restrições aplicáveis. A mera presença do identificador não aprova a liberação. |
| `provenance` | Estrutura rastreável, 1 | Contém `artifact_id`, `locator` e `activity_ids` em ordem de aplicação. Permite recuperar o artefato, o local e as atividades responsáveis. Para fontes agregadas, registrar contribuição de cada origem e verificar as condições cumulativas. |
| `status` | Enumeração, 1 | `RAW`, `PROCESSED`, `CURATED`, `RELEASED` ou `REJECTED`. Um objeto bruto pode ter seus dados administrativos em manifesto próprio. |
| `payload` | Objeto tipado pelo perfil, 1 | Conteúdo que recebe revisão humana. Uma classificação inferida deve identificar a sua condição e o seu autor. |

Estados de revisão podem ser descritos por eventos e manifestos. A promoção posterior não autoriza reescrever os bytes de uma revisão já publicada. O [pipeline](DATA_PIPELINE.md) define como obter o estado efetivo em cada instantâneo. O [versionamento](VERSIONING.md) disciplina a retirada de um item publicado.

## Chaves e relações

| Objeto ou campo | Interpretação proposta | Cardinalidade ou restrição |
|---|---|---|
| Identidade e revisão | `(record_id, revision)` | Um registro pode ter várias revisões históricas. Cada release operacional seleciona uma por identidade. |
| `*_id` para referência entre registros | Identidade do registro alvo | Resolver na mesma seleção versionada. Verificar domínio e subtipo esperado, além da existência. Ligações de auditoria a alvos históricos devem fixar a revisão e podem ser resolvidas em inventário arquivado. |
| `talkset_id` | Chave estrangeira cujo valor é o `record_id` de um Talkset | Uma projeção de entradas ou respostas carrega a chave do grupo. O documento canônico não duplica sua identidade no payload. |
| `prompt_id`, `response_id` | Identificadores estáveis de membros do Talkset | IDs de prompts são únicos entre prompts e IDs de respostas entre respostas em toda a edição. Referência externa a um membro inclui grupo e release/revisão. Mudanças editoriais preservam sua identidade quando o sentido permanece. |
| `source_id`, `rights_id` | Referências administrativas | Resolver contra versões preservadas de catálogo e decisões no manifesto. Podem preceder um registro linguístico. |
| Ancestral de derivação | Referência a artefato e localizador ou a registro e revisão | Citar a versão efetivamente usada. Referências documentais podem apontar a catálogo restrito. |
| `knowledge_version`, `engine_compatibility` | Edição da MKB e lista fechada de versões de motor testadas | Pertencem ao contrato de release, em conjunto com `schema_version`. |

**Exemplo.** A referência a um julgamento de “resposta inadequada” precisa incluir a identidade da resposta, a do Talkset e a revisão julgada. Se apenas o texto for guardado, duas respostas homógrafas tornam a correção ambígua. Se uma sugestão resultar em edição, a revisão seguinte e a decisão do revisor permitem auditar a mudança.

## Unidades de conhecimento e âncoras

| Domínio | Unidade e chaves específicas documentadas | Natureza da evidência |
|---|---|---|
| [LIT](domains/MKB-LIT.md) | Obra, edição e fragmento com `edition_id` e `text_span` | Ocorrência em uma representação textual fixa |
| [LEX](domains/MKB-LEX.md) | Entrada com `lemma`, `part_of_speech` e `forms` | Forma e uso linguístico |
| [SEM](domains/MKB-SEM.md) | Conceito ou relação com `subject_id`, `predicate`, `object_id` | Distinção de sentido com justificativa |
| [DLG](domains/MKB-DLG.md) | Talkset com `prompts` e `responses` | Juízo editorial de adequação de resposta |
| [NAR](domains/MKB-NAR.md) | Modelo com `pattern` e `slots` | Realização textual condicionada |
| [CTX](domains/MKB-CTX.md) | Sinal ou predicado sobre sinais tipados | Significado de informação fornecida |
| [PSY](domains/MKB-PSY.md) | Perfil, traço ou categoria emocional | Convenção de representação ficcional |
| [BEH](domains/MKB-BEH.md) | Comportamento com guardas e realização | Escolha de expressão admitida |
| [REA](domains/MKB-REA.md) | Regra ou caso com conclusão derivada | Passo explicável de inferência |
| [LRN](domains/MKB-LRN.md) | Julgamento sobre alvo e revisão | Evidência humana para correção e avaliação |

Campos ausentes só são válidos quando o perfil os declara opcionais. Uma lista vazia, uma negação explícita e um valor desconhecido expressam coisas diferentes. A publicação deve falhar se um campo obrigatório desaparecer silenciosamente numa conversão. A política de coerção e os formatos admitidos estão em [Formatos](DATA_FORMATS.md).

## Critérios de aceite do futuro validador

Duas revisões incompatíveis sob a mesma chave acusam conflito mesmo que venham de lotes distintos. Um identificador de obra onde se espera edição acusa erro de tipo. Uma referência documental a insumo de acesso restrito precisa ser distinguida de uma dependência executável ausente. Uma revisão publicada deve ser localizável a partir de uma trilha de decisão, mesmo após atualização do banco local.
