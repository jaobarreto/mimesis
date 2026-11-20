# Corpus literário brasileiro

**Decisão aprovada.** Priorizar literatura brasileira em domínio público, preservar a redação original e manter formas normalizadas separadas. Uma ocorrência literária oferece evidência de uma construção em uma edição. Converter essa ocorrência em conhecimento lexical, resposta dialogal ou modelo narrativo exige uma nova afirmação revisada, com procedência ligada à primeira. O livro digital sozinho não comprova a compreensão de linguagem pelo motor. [Arquitetura da MKB](KNOWLEDGE_BASE.md) · [Perfil literário](domains/MKB-LIT.md)

## Fila de descoberta

Os dezessete nomes abaixo são prioridades do projeto. Cada linha define uma investigação posterior. A presença nesta fila não atesta que uma edição específica seja elegível.

| Autor prioritário | Questão para a seleção de amostras futuras |
|---|---|
| Machado de Assis | Separar observação do narrador, comentário dirigido ao leitor e fala de personagem. A BBM cataloga um exemplar de 1899. [Dom Casmurro](https://digital.bbm.usp.br/handle/bbm/4828) |
| José de Alencar | Comparar intervenções editoriais e grafias de edições distintas. A ficha da edição de 1865 permite identificar o exemplar e menciona a revisão de 1870. [Iracema](https://digital.bbm.usp.br/handle/bbm/4660) |
| Júlia Lopes de Almeida | Buscar mudanças de locutor dentro do parágrafo e contrastar descrição com ação. Registrar eventuais coautorias por obra. |
| Simões Lopes Neto | Identificar regionalismos atestados no trecho, vozes do narrador e grafias da edição consultada. |
| Afonso Arinos | Distinguir o escritor natural de Paracatu do jurista homônimo. Vincular o identificador de autoridade antes de calcular prazos ou atribuir obra. [Perfil do escritor na ABL](https://www.academia.org.br/publicacoes/afonso-arinos) · [Perfil do jurista](https://www2.academia.org.br/academicos/afonso-arinos-de-melo-franco/biografia) |
| Inglês de Sousa | Conferir variantes do nome na ficha e delimitar expressões em seu contexto antes de atribuir região ou acepção. |
| Lima Barreto | Separar comentários do narrador de caracterizações atribuídas a interlocutores. |
| Aluísio Azevedo | Distinguir descrição do ambiente, percepção de personagem e ação coletiva no mesmo parágrafo. |
| Joaquim Manuel de Macedo | Conferir dêiticos como “aqui” e “agora” segundo o locutor, a cena e o tempo narrado. |
| Visconde de Taunay | Relacionar o pseudônimo ou título usado na edição ao registro de autoridade e indicar quem narra cada relato. |
| Manuel Antônio de Almeida | Localizar mudança de cena, elipse temporal e continuidade de interlocutores entre parágrafos. |
| Maria Firmina dos Reis | Identificar a autoria indicada na folha de rosto, suas variantes de catálogo e o responsável por eventuais notas de edição. |
| Sílvio Romero | Registrar a função de quem organiza, recolhe ou narra, conforme a edição. O catálogo da BBM fornece uma pista para examinar créditos de coleta e introdução. [Contos populares do Brazil](https://digital.bbm.usp.br/handle/bbm/4600) |
| Bernardo Guimarães | Verificar atribuição de fala, discurso citado dentro do diálogo e construções repetidas em edições diferentes. |
| Franklin Távora | Delimitar alusões do narrador a épocas ou lugares e distinguir topônimo de marca linguística regional. |
| Carmem Dolores | Conservar a grafia do briefing como termo de busca. O Senado usa **Carmen Dolores** em edição de *Um drama na roça*. Registrar variantes e verificar a responsabilidade de cada contribuição moderna. [Edição anunciada pelo Senado](https://www12.senado.leg.br/institucional/procuradoria/comum/edicoes-tecnicas-do-senado-lanca-o-livro-um-drama-na-roca-de-carmen-dolores-volume-7-5-10-2021) |
| Domingos Olímpio | Marcar sensações atribuídas a um observador e separar marcas explicitamente descritas das inferidas pelo leitor. |

Selecionar inicialmente pares com características distintas de edição, gênero textual e dificuldade de extração. Registrar lacunas por autor, período e variedade. Uma obra mais acessível pode dominar o teste se capítulos e edições do mesmo título forem espalhados entre partições. Decidir o grupo por obra e seus descendentes antes de avaliar recuperação ou composição. [Benchmarks](BENCHMARK_DATASETS.md)

## Cadeia editorial proposta

1. Identificar autor e papel, obra, edição, arquivo obtido e representação textual derivada. Registrar publicação e data da digitalização separadamente. Prefácio, notas, traduções e imagens conservam evidência de direitos própria.
2. Preservar os bytes de origem quando permitido. Extrair um TXT UTF-8 fiel à edição com versão identificada, mantendo diacríticos, pontuação, parágrafos e limites de cena. Conservar localizadores para o fac-símile/arquivo. Se o fornecedor entregou um TXT modernizado, registrar essa condição. O original recebido pode já incorporar intervenções.
3. Registrar correções de OCR em uma representação revisada, com referência à leitura anterior, página e motivo. Conferir travessões, hifens em fim de linha, acentos, colunas e cabeçalhos de página. Gerar a forma normalizada separadamente, com a regra de normalização e a correspondência de intervalos quando uma substituição muda o comprimento.
4. Cada fragmento usa `edition_id` e `text_span`. Ancorar o intervalo no artefato textual imutável identificado e na revisão de extração. Para TXT, propor início inclusivo e fim exclusivo em pontos de código Unicode, a partir de zero. A posição de uma string já decodificada não é um deslocamento de bytes. Exercitar esse contrato com acentos combinantes. Para TEI, conservar também o identificador do elemento. [W3C Web Annotation, Text Position Selector](https://www.w3.org/TR/annotation-model/#text-position-selector) · [Normalização Unicode](https://www.unicode.org/reports/tr15/)
5. Usar `language` para o idioma/variedade atestado na passagem e metadados separados para período, evidência regional e registro. Distinguir português histórico, pt-BR contemporâneo e pt-PT. Usar `pt` quando o português for identificável e a variedade permanecer indeterminada. Um personagem, editor ou narrador pode empregar outra variedade. Local de impressão e nacionalidade do autor são indícios insuficientes. [BCP 47, RFC 5646](https://www.rfc-editor.org/info/rfc5646/)
6. Encaminhar os candidatos à classificação humana. A marcação de fala ou pensamento em TEI e os verbos dicendi podem orientar segmentação, com posterior confronto com o texto e o seu enquadramento narrativo. [TEI, elemento said](https://tei-c.org/release/doc/tei-p5-doc/en/html/ref-said.html)

## Rubrica de extração e classificação

As categorias propostas são multivaloradas. Anotar o menor intervalo que sustenta cada rótulo e conservar o contexto que permite interpretá-lo. Um identificador de entidade deve permanecer local à obra e edição enquanto sua correspondência entre edições estiver pendente. [Taxonomia](TAXONOMY.md)

| Categoria | Como propor candidato e o que marcar | Caso decisivo para revisão |
|---|---|---|
| `dialogue` — diálogo | Delimitar a troca em cena, interlocutores presentes, marcas tipográficas e narração intercalada. | Uma carta lida em voz alta pode ter o leitor e o autor citado em planos distintos. Identificar o plano narrativo. |
| `turn` — turno | Delimitar a fala de um locutor, vincular troca e ordem. Se houver interrupção pelo narrador, permitir intervalos relacionados. | Travessão interno pode introduzir um inciso. Nome ausente permite locutor incerto. Adjacência não demonstra que houve resposta direta. |
| `environment` — descrição de ambiente | Localizar atributo físico, lugar/referente e ponto de vista, incluindo descrição estática e mudança observada. | Separar previsão de evento futuro de condição atual do lugar. |
| `emotion_expression` — expressão emocional | Identificar quem sente ou manifesta, a expressão textual, polaridade/negação e se a emoção é mencionada ou inferida. | Tremor ou silêncio admitem várias leituras. Guardar o sinal observável e a incerteza, sem diagnóstico. |
| `gesture` — gesto | Marcar ação corporal concreta, agente, parte do corpo e alvo explícito, se houver. | “Dar as costas” pode designar movimento ou ruptura figurada. A leitura depende de contexto. |
| `sensation` — sensação | Anotar estímulo, modalidade sensorial e experimentador quando identificados. | Cheiro descrito no ambiente pode coexistir com percepção individual apenas quando há indício textual de quem percebe. |
| `action` — ação | Delimitar predicado, agente e participantes, tempo, negação e modalidade. | “Ia abrir”, “não abriu” e “abriu” exigem classificações distintas de realização. |
| `reaction` — reação | Vincular o ato a um estímulo pela evidência textual. Aceitar origem incerta e indicar a passagem de apoio. | O fato de dois eventos se sucederem não basta para afirmar causalidade. |
| `conflict` — conflito | Marcar participantes, objetivos incompatíveis e evidência de oposição. Um episódio pode ter vários turnos. | Discordância citada pelo narrador pode ter falantes ausentes e vozes indiretas. |
| `transition` — transição narrativa | Localizar mudança temporal, espacial, de foco ou cena, com passagens de origem e destino quando visíveis. | Mudança de parágrafo por diagramação/OCR não estabelece mudança de cena. |
| `syntactic_structure` — estrutura sintática | Preservar tokens, oração relevante e relação proposta (por exemplo, condição ou coordenação), especificando analisador ou anotador. | Inversão histórica e discurso indireto livre podem induzir uma análise sintática contemporânea incorreta. |
| `vocabulary` — vocabulário | Vincular forma atestada, intervalo, lema proposto, expressão composta e sentido contextual quando justificável. | Homógrafos e grafias históricas requerem evidência de sentido. Conservar a forma rara como ocorrência. |
| `literary_construction` — construção literária | Marcar o trecho e a hipótese interpretativa, por exemplo repetição, comparação ou alternância de voz, indicando os elementos que a sustentam. | Uma comparação específica pode servir de evidência para investigar uma construção. Generalizar a fórmula em NAR requer curadoria, abstração e direito de derivação. |

## Exemplo autoral e teste de ancoragem

No texto didático inventado `— Voltou? — perguntou Lia, fechando a janela.`, a fala ocupa `[2,9)`, a atribuição `[12,25)` e a ação `[27,44)`. A atribuição oferece evidência para identificar Lia como locutora. A pergunta deixa em aberto quem voltou. Fechar a janela é ação concomitante, com causalidade e emoção indeterminadas. O exemplo não contém resposta que possa formar por si um Talkset. O teste de curadoria deve conseguir reproduzir as três substrings pelo identificador do artefato e os intervalos, inclusive depois de criar uma segunda representação normalizada. [Curadoria](CURATION_GUIDELINES.md) · [Qualidade](DATA_QUALITY.md)\n