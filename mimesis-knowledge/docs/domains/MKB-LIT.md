# MKB-LIT · Conhecimento literário

**Decisão aprovada.** Priorizar literatura brasileira em domínio público, preservar a grafia original e manter representações normalizadas separadas. O modelo abaixo é uma proposta editorial. A verificação de direitos alcança cada edição, transcrição e contribuição adicional.

## 1. Finalidade

Permitir que uma anotação sobre uma passagem seja conferida na edição exata de onde foi extraída. Isso sustenta a pesquisa de construções, ritmos, turnos e escolhas lexicais em pt-BR.

## 2. Escopo

Autores identificados ou incertos, obras, edições, representações textuais e fragmentos. Distinguir autoria da obra, responsabilidade editorial, transcrição e digitalização. Uma edição traduzida tem histórico linguístico e de direitos próprio.

## 3. Responsabilidades

Preservar a fonte e suas divisões internas, identificar intervenções editoriais e documentar a seleção e a ancoragem. A eventual reutilização conversacional exige um derivado revisado em DLG ou NAR.

## 4. Tipos de conhecimento

Separar evidência textual, estrutura editorial e classificação interpretativa. Fala citada, troca de turno, narração, gesto ou discurso indireto livre podem exigir mais de um rótulo e diferentes níveis de certeza.

## 5. Estrutura dos registros

Quatro perfis propostos sob `payload.kind`. `author` guarda `display_name` e variantes documentadas. `work` guarda `title` e `author_ids`, com indicação explícita de autoria indeterminada quando pertinente. `edition` associa `work_id`, identificação editorial e a representação textual imutável. `fragment` requer `edition_id`, `text_span` e `categories`. O intervalo é semiaberto, começa em zero e é contado em pontos de código Unicode no TXT extraído identificado por `text_artifact_id`. Registrar a codificação e as quebras exatas dessa representação. A normalização gera outra representação e outro mapa de posições.

Recorte fictício de payload para a passagem autoral “A porta rangeu.”. O intervalo inclui o ponto final.

```json
{"kind":"fragment","edition_id":"e17","text_span":{"text_artifact_id":"a42","start":0,"end":15},"categories":["action"]}
```

## 6. Relações entre entidades

Uma obra pode ter várias edições e vários autores. Uma edição tem vários fragmentos. Sobreposições são permitidas em anotações de naturezas diferentes. Um fragmento derivado por SEM, LEX ou NAR continua apontando para a representação correta mesmo depois de uma nova transcrição.

## 7. Metadados obrigatórios

Além do [envelope comum](../METADATA_SPECIFICATION.md), identificar a edição consultada, a representação ancorada, o método de extração, a revisão da classificação e a variedade linguística conhecida. Data de composição, edição e digitalização devem ocupar campos distintos quando disponíveis. Uma data ou um atribuidor desconhecido deve ser declarado como tal.

## 8. Fontes candidatas

Avaliar OBras/Linguateca, Wikisource, Portal Domínio Público, Brasiliana Digital, Biblioteca Nacional Digital e Project Gutenberg por item. Em paralelo, usar prosa original da equipe para testar anotação e extração. As prioridades autorais e a política para variação histórica estão no [plano do corpus](../LITERARY_CORPUS.md).

## 9. Importação

Preferir TXT, XML/TEI, EPUB ou HTML estruturado. Identificar versão e guardar o hash do original autorizado. Preservar cabeçalho, divisões e marcas editoriais em uma camada intermediária. Para digitalização em imagem sem alternativa, registrar página e incerteza de OCR. TEI documenta marcação de citações, mudanças editoriais e referências internas. [TEI P5, Core](https://tei-c.org/release/doc/tei-p5-doc/en/html/CO.html)

## 10. Processamento

Segmentar capítulos e parágrafos antes de inferir turnos por travessão ou aspas. Marcar narrador intercalado e falante desconhecido. Extrair caracteres do TXT fixado antes de modernizar ortografia. Revisar amostras de cada edição para perceber cabeçalhos repetidos, hifenização de quebra de linha e discurso indireto confundido com fala.

## 11. Validação

Verificar existência de edição e artefato, `0 ≤ start < end ≤ comprimento`, e reprodução do trecho pelo intervalo. Se “rangeu” muda de posição após expansão ortográfica, a âncora antiga continua vinculada à versão original. Conferir amostras contra o arquivo recebido e separar falha de OCR de grafia histórica.

## 12. Indexação

Indexar `work_id`, `edition_id`, categoria e intervalo. Um índice textual histórico e outro normalizado podem apoiar a pesquisa se a licença permitir. O índice derivado registra a versão da normalização. Liberar literatura para análise não concede automaticamente uso de seus fragmentos como respostas.

## 13. Utilização pelo motor

Um módulo narrativo futuro poderá recuperar um modelo curado que cite fragmentos como evidência. O motor preservará a cadeia de derivação e verificará o perfil de uso aprovado. Genesis pode funcionar exclusivamente com Talksets próprios.

## 14. Versionamento

Nova edição recebe nova identidade. Correção da transcrição exige nova versão do artefato e realinhamento explícito de todos os intervalos afetados. Nunca deslocar silenciosamente a âncora de um fragmento publicado.

## 15. Limitações

Amostras preservadas por bibliotecas têm vieses de época, gênero e acesso. Ausência de uma construção no corpus não prova sua inexistência. Travessões podem iniciar enumeração, diálogo ou intervenção do narrador.

## 16. Critérios de qualidade

Rejeitar fragmentos com âncoras irrecuperáveis ou atribuição inventada. Registrar, por edição e categoria, a fração de âncoras recuperáveis, a taxa de correções de OCR na amostra e os desacordos entre anotadores. Agrupar a obra e suas edições na divisão experimental para conter vazamento textual.
