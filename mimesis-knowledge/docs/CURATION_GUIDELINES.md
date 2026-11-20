# Guia de curadoria e adjudicação

**Decisão aprovada.** A MKB depende de conhecimento validado pela equipe e de aprendizado supervisionado. Só revisões elegíveis para a finalidade declarada podem chegar à release. **Proposta de protocolo.** O trabalho do curador é decidir qual afirmação cada unidade de evidência sustenta, para que serve e onde deixa de valer.

## Revisar um registro

1. Resolver o par `record_id`, `revision`, o perfil `domain` e a origem que o envelope identifica. Ler a passagem no contexto, recuperar `provenance.artifact_id`, aplicar `locator` à representação correta e verificar as transformações em `activity_ids`. Conferir direito de acesso antes de abrir originais restritos.
2. Identificar a unidade de afirmação. Uma ocorrência observada pertence a LIT. Um julgamento de adequação exige DLG ou LRN conforme seu objeto. Se o registro mistura ocorrência e inferência, preservar a ocorrência e propor o derivado com sua própria revisão. [Perfis de domínio](KNOWLEDGE_BASE.md)
3. Julgar o idioma, a variedade conhecida, a data e o registro de uso. Preservar vozes de narrador, personagem e editor. Em textos históricos, rotular a evidência, indicar dúvidas e evitar modernizar a versão usada para os intervalos. [Corpus literário](LITERARY_CORPUS.md)
4. Ler exemplos positivo e limítrofe da categoria. Estabelecer `observed`, `inferred` ou `uncertain` segundo a [taxonomia](TAXONOMY.md). Guardar intervalo ou fato que sustenta cada interpretação, incluindo negação, hipótese, citação e ironia. Uma interpretação incerta pode continuar documentada para pesquisa. O uso operacional exige que o perfil permita essa incerteza.
5. Detectar identidades repetidas e famílias próximas. Reunir versões de uma mesma obra, conversa, prompt, tradução ou paráfrase segundo a unidade de avaliação. A exata duplicação de bytes pode compartilhar armazenamento. Ocorrências linguísticas em obras distintas conservam suas procedências. [Benchmarks](BENCHMARK_DATASETS.md)
6. Registrar responsável, versão da rubrica, parecer, motivo e momento. Se a revisão resolve as objeções, promover a `CURATED`. Se o problema é corrigível, documentar uma nova revisão. Se inviabiliza a candidata, registrar `REJECTED` com os dados autorizados. O histórico de uma revisão anterior continua citável nos limites de guarda definidos. [Pipeline](DATA_PIPELINE.md)

## Perguntas por tipo de material

| Material | Prova que o curador deve produzir | Falha que a revisão deve detectar |
|---|---|---|
| Ocorrência literária | Reproduzir intervalo e atribuição, registrar incerteza de locutor e cotejar imagem ou edição quando elegível | OCR converteu travessão em hífen e fundiu duas falas |
| Entrada lexical ou relação semântica | Citar forma, lema/acepção e evidência. Checar direção, escopo e restrições de sentido | Similaridade gráfica confundida com sinonímia ou antônimo aplicado à acepção errada |
| Talkset | Para cada variante de entrada, conferir **cada** resposta ativa. Listar contraexemplo, pressuposto de contexto e registro linguístico | Uma resposta correta para uma pergunta no presente inventa fato quando aplicada à variante no passado |
| Modelo narrativo | Exercitar posições preenchidas, ausentes e ambíguas em cenários mínimos. Rastrear cada afirmação factual ao contexto e cada escolha estilística à regra | Um adjetivo acrescenta clima ou emoção que a entrada não informou |
| Persona, reação ou regra | Precisar a quem se aplica, as precondições e os casos que exigem abstenção | Uma preferência expressiva vira afirmação psicológica sobre qualquer pessoa, ou uma regra trata desconhecido como falso |
| Julgamento de avaliação | Fixar alvo e revisão, rubrica e classe de uso. Aceitar múltiplas respostas justificadas e manter a trilha de adjudicação | Uma resposta fora do conjunto julgado recebe automaticamente nota de irrelevância |

## Calibração e desacordos

**Proposta.** Antes de trabalhar em volume, selecionar um pequeno lote estratificado por domínio, fonte e dificuldade, com ambiguidades deliberadas e exemplos simples. Dois anotadores aplicam a mesma rubrica de forma independente, sem ler os rótulos um do outro. Medir separadamente acerto de fronteiras, acordo de categoria, atribuição de locutor e adequação das respostas. Acordo percentual, distribuição das classes e contagem de itens sem decisão ajudam a interpretar a concordância corrigida pelo acaso. [Qualidade](DATA_QUALITY.md)

No desacordo, preservar as leituras e a evidência de cada anotador. O adjudicador decide entre ajustar fronteira, escolher rótulo, admitir múltiplos rótulos, manter indeterminado, corrigir a extração ou rejeitar. Registrar motivo com exemplo e contraexemplo novo quando a divergência revela uma lacuna na rubrica. Mudanças de instrução têm versão e exigem localizar os registros que dependiam da definição anterior para revalidação. Se houver apenas um revisor disponível, declarar isso e distinguir revisão individual de concordância independentemente aferida.

**Exemplo didático.** Diante de “Fechou a porta quando ouviu o ruído”, dois anotadores concordam sobre ação e percepção. Um propõe “medo”, o outro julga apenas simultaneidade. O texto sustenta a ação e sua relação temporal com a percepção. Manter emoção indeterminada sem contexto adicional. Se uma passagem anterior documentar medo explícito, ancorar a nova leitura também nessa passagem.

## Resultado e repasse

Entregar contagem por decisão e classe, amostras de discrepância, registros aceitos com seus grupos de partição e riscos de generalização. Uma ausência de falantes nomeados pode ser aceitável em LIT e impeditiva para uma tarefa de atribuição de turnos. Um texto literário histórico pode ser aceito para investigação lexical e ficar fora de um perfil de diálogos atuais. A release precisa descrever o recorte autorizado por direito e uso. [Governança](DATA_GOVERNANCE.md) · [Versionamento](VERSIONING.md)\n