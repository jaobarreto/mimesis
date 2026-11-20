# Formatos de entrada, preservação e intercâmbio

**Proposta.** Escolher a representação que preserve a estrutura da edição e permita reencontrar o trecho. Uma transcrição TXT limpa pode ser melhor para busca, enquanto um TEI com falantes identificados carrega evidência adicional para segmentação. Registrar o formato realmente recebido e o resultado da detecção de codificação.

| Entrada candidata | Procedimento de extração | Risco a revisar |
|---|---|---|
| TXT UTF-8 | Guardar bytes originais, identificar separadores de linha e cabeçalhos. | Uma quebra visual pode cortar um turno. |
| XML, TEI | Preservar idioma, IDs, falantes, divisões e mapeamento de elementos. Ler localmente com referências externas desativadas. | Notas editoriais ou variantes podem parecer fala. |
| JSON, JSONL, CSV | Fixar versão do esquema, encoding, separador e tratamento de nulos. | Arrays, quebras internas e colunas homônimas podem perder significado. |
| EPUB, HTML | Seguir ordem de leitura declarada, distinguir notas e capítulos, guardar âncora e caminho interno. | Navegação e rodapé podem contaminar o texto. |
| PDF textual, DOCX | Usar quando faltar alternativa melhor. Revisar colunas, notas, caixas e ordem dos parágrafos. | Aparência da página e ordem de extração podem divergir. |
| PDF digitalizado | Última prioridade. Registrar página, imagem, método e versão de OCR, revisar amostra de acentos, rasuras e travessões. | Erros sistemáticos contaminam léxico e segmentação. |

| Saída interna | Unidade e convenção |
|---|---|
| TXT | Transcrição por edição, UTF-8. Normalização em arquivo separado com rastreio de offsets. |
| JSON | Manifestos e metadados estruturados com chaves em inglês. Rejeitar chaves duplicadas. |
| JSONL | Um objeto JSON completo por linha UTF-8 terminada em LF. Quebras no texto são escapadas pelo serializador. |
| CSV | Cabeçalho estável, nomes e tipos no dicionário. Registrar convenção de nulo para distingui-lo de string vazia. |
| YAML | Configuração legível, carregamento seguro sem construção de objetos arbitrários. Guardar o digest da configuração efetiva. |
| Parquet | Lotes colunares grandes, esquema e tipos verificados na fronteira. Particionar apenas por campos que favoreçam a leitura medida. |
| SQLite | Projeção operacional derivada do manifesto, com chaves externas e FTS5 quando requisitado. |
| Markdown | Decisões, fichas, guias e pareceres sem material protegido desnecessário. |

**Caminhos lógicos propostos.** `datasets/raw/<source_id>/<artifact_id>/original.<ext>` conserva o objeto recebido sob controle de acesso. `datasets/processed/` guarda derivados e mapas de origem. `datasets/curated/` conserva as revisões prontas para seleção. `datasets/rejected/` guarda recibos e motivos, sujeito a restrições de retenção. `manifests/` e `releases/` indexam lotes e edições. A presença em um diretório não promove o estado. Dados grandes ou restritos ficam em armazenamento local controlado e são referenciados por localizador e hash quando isso for permitido.

**Teste de ida e volta.** Reabrir cada JSONL e reconciliar ID, texto com aspas e quebras, acentos e revisão. No CSV, conferir nulo e vazio. Para um fragmento literário, resolver o localizador no arquivo hash-identificado e comparar o trecho com a transcrição preservada. [Metadados](METADATA_SPECIFICATION.md) · [Pipeline](DATA_PIPELINE.md)
