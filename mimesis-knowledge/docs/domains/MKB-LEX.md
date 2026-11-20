# MKB-LEX · Conhecimento lexical

**Proposta arquitetural.** Modelar como unidade revisável uma entrada lexical em determinada língua e categoria gramatical, com grafias ou flexões atestadas. A separação de acepções pertence a [MKB-SEM](MKB-SEM.md).

## 1. Finalidade

Permitir que “chegaram” seja recuperável pela entrada de “chegar”, sem perder a forma efetiva da fonte. Ampliar o repertório reconhecível e apoiar a realização morfológica de texto.

## 2. Escopo

Lemas, flexões, locuções, grafias históricas, variantes regionais e marcas de uso. Registrar uma forma observada é uma afirmação mais restrita do que declarar duas formas intercambiáveis.

## 3. Responsabilidades

Preservar grafia e diacríticos, documentar a análise gramatical e permitir interpretações múltiplas. Vincular evidência ao local onde o uso ocorreu. Sinalizar ao consumidor quais expansões podem produzir ambiguidade.

## 4. Tipos de conhecimento

Entrada simples, expressão de várias palavras, forma flexionada e variante ortográfica. Distinguir atestação em fonte, descrição autoral revisada e forma gerada por regra. Uma forma gerada precisa ser identificada como hipótese até a validação.

## 5. Estrutura dos registros

`kind=lexical_entry`, `lemma`, `part_of_speech` e `forms` com grafia em `surface` e classificação em `form_type`. `features` aceita pares de atributo e valor do inventário morfológico versionado. Vínculos de sentido e evidência podem ser acrescentados. Definir a unidade de tokenização para locuções.

```json
{"kind":"lexical_entry","lemma":"chegar","part_of_speech":"verb","forms":[{"surface":"chegamos","form_type":"inflection","features":{"person":"first","number":"plural"}}]}
```

“Chegamos” requer contexto para distinguir leituras de tempo verbal. A ausência de uma marca de tempo no exemplo mantém a ambiguidade.

## 6. Relações entre entidades

Uma forma pode apontar a várias entradas. Uma entrada pode se ligar a vários conceitos SEM. Evidências podem vir de fragmentos LIT com âncoras. O par “sede” substantivo e “sede” em uma análise verbal ilustra por que a chave de busca normalizada aceita colisões.

## 7. Metadados obrigatórios

Usar o [envelope comum](../METADATA_SPECIFICATION.md), identificando idioma, fonte, direitos, versão do inventário gramatical e como a forma foi obtida. Para a marca “regional”, documentar a região e a evidência. Manter “desconhecida” quando a fonte não a informa.

## 8. Fontes candidatas

Vocabulário original da equipe, formas atestadas no corpus literário autorizado e recursos lexicais indicados pelo [catálogo](../DATASET_REGISTRY.md), como OpenWordNet-PT, após revisão de versão, cobertura linguística e direito sobre o item. A proveniência da definição pode diferir da proveniência da grafia.

## 9. Importação

Guardar mapeamento entre colunas ou marcação da fonte e o inventário local. Preservar cada grafia recebida, o identificador de origem e a versão do mapeamento. Entradas sem classe reconhecida ficam em revisão, com o rótulo original disponível.

## 10. Processamento

Produzir chaves auxiliares de busca sem alterar `surface`. Distinguir normalização Unicode, conversão de caixa e remoção de diacríticos. Testar “avó” e “avô” como controle de colisão. Uma heurística de sufixos apenas propõe análises e pode falhar em verbos irregulares.

## 11. Validação

Rejeitar lema vazio, feição fora do inventário ou análise que não consiga citar sua evidência. Levar colisões de chave ao índice como múltiplos resultados. Conferir se as formas propostas são compatíveis com classe, língua e período declarado.

## 12. Indexação

Propor índices por `(language, lemma, part_of_speech)` e por forma de superfície. Uma chave normalizada pode retornar mais de um `record_id`. Para locuções, incluir extensão de tokens para poder avaliar o reconhecimento do segmento completo.

## 13. Utilização pelo motor

Lexicon poderá expandir entradas de busca ou ligá-las a conceitos sem apagar a consulta original. Logos poderá consultar uma flexão curada ao realizar um parâmetro. A trilha deve identificar a entrada, a forma e a regra de normalização utilizada.

## 14. Versionamento

Mudança de marca gramatical revisa a entrada. Divisão de homógrafos antes agregados cria identidades próprias e ligação de migração. Alteração do inventário exige relatório das formas ainda sem equivalente.

## 15. Limitações

Corpus literário pode super-representar formas históricas. Redução ao lema pode apagar contrastes de tempo ou número relevantes para a intenção. O reconhecimento de uma locução em texto admite leituras literais alternativas.

## 16. Critérios de qualidade

Medir cobertura de formas em amostra reservada, ambiguidades por forma e taxa de expansões incorretas em pares contrastivos. Reportar grafias históricas separadamente. A publicação exige que toda forma distribuída seja localizável e que colisões nunca fundam identidades em silêncio.
