# MKB-NAR · Conhecimento narrativo

**Proposta arquitetural.** Catalogar realizações narrativas e as condições factuais e linguísticas de seu uso. O motor pode verbalizar o que recebeu da aplicação e compor variações de estilo preservando o conteúdo autorizado.

## 1. Finalidade

Sustentar a narração de ambientes em Mythos e a composição procedural em Logos. Cada expressão que acrescente uma qualidade objetiva precisa de uma entrada verificável ou de uma autorização explícita do sistema de origem.

## 2. Escopo

Descrições, sensações, gestos, ações e reações informadas, transições discursivas e modelos de realização. Limitar o modelo aos efeitos textuais. A existência de personagens, locais, acontecimentos e relações temporais depende dos dados autorizados pelo integrador.

## 3. Responsabilidades

Explicitar quais dados um modelo consome, quais afirmações faz e quais concordâncias requer. Preservar registro de uso, variedade de português e evidência editorial dos modelos derivados.

## 4. Tipos de conhecimento

`template` representa uma realização com parâmetros. O campo `category` pode marcar `environment`, `sensation`, `action`, `reaction` ou `transition`. Variantes podem compartilhar um mesmo significado desde que seus compromissos factuais sejam equivalentes.

## 5. Estrutura dos registros

Um modelo requer `pattern`, `slots`, `category` e `assertions`. Cada slot informa nome, tipo, sinal autorizado que o alimenta e obrigatoriedade. Cada afirmação associa a leitura factual a esse sinal ou a uma condição. A notação de chaves é ilustrativa, sua gramática executável depende de especificação futura. Exemplo autoral de relatório de percepção fornecida pela aplicação.

```json
{
  "kind":"template","category":"sensation",
  "pattern":"O som percebido foi {reported_sound}.",
  "slots":[{"name":"reported_sound","type":"noun_phrase","signal_id":"c09","required":true}],
  "assertions":[{"meaning":"reported_sound","signal_id":"c09"}]
}
```

## 6. Relações entre entidades

Um modelo referencia definições de sinais em CTX e pode usar entradas LEX para flexão ou PSY para variantes de registro. Se derivado de uma passagem LIT, citar o fragmento e a revisão. Dois modelos que ligam os mesmos slots podem ter significados diferentes, por exemplo, “ouve-se” e “ouviu-se”.

## 7. Metadados obrigatórios

Além do [envelope comum](../METADATA_SPECIFICATION.md), documentar origem do padrão, idioma e variedade, inventário de tipos de slots e a revisão do contrato de afirmações. Para material adaptado, permitir recuperar tanto a fonte quanto as operações editoriais.

## 8. Fontes candidatas

Modelos escritos pela equipe, fragmentos literários com direitos conferidos e exemplos narrativos de corpora candidatos quando a adaptação textual for autorizada. O conteúdo de um jogo externo requer avaliação por componente. [Registro de fontes](../DATASET_REGISTRY.md)

## 9. Importação

Capturar a passagem e suas condições observáveis. Um curador distingue o texto concreto, a estrutura reutilizável e os fatos necessários para uma nova realização. Se a fonte permitir somente análise, preservar a restrição ao avaliar a divulgação do derivado.

## 10. Processamento

Propor substituições localizadas e testar concordância, regência e pontuação do entorno. Para “o céu voltou a escurecer”, explicitar que “voltou” pressupõe escurecimento anterior. Só admitir a forma se essa pressuposição estiver satisfeita no contexto.

## 11. Validação

Todo marcador no padrão deve corresponder a um slot declarado. Todo slot obrigatório precisa ser fornecido e todo valor deve ser tratado como dado. Recusar chamadas arbitrárias e referências externas. Testar dado ausente, ruído/ausência de ruído e variação de gênero e número. Se faltar um requisito, desabilitar a variante.

## 12. Indexação

Indexar categoria, conjuntos de sinais requeridos, idioma e marcas de registro. Uma estrutura invertida por sinal pode reduzir os modelos a testar. Só reordenar por estilo após aplicar as condições factuais e gramaticais da variante.

## 13. Utilização pelo motor

Mythos seleciona uma descrição compatível com o ambiente já informado. Logos realiza os slots, registra os sinais usados e preserva o contexto de entrada. Um modelo que descreve ação passada só pode ser usado quando essa ação constar dos fatos recebidos.

## 14. Versionamento

Mudança em slot obrigatório ou no significado pressuposto exige nova revisão do modelo e revalidação dos consumidores. Registrar separadamente alterações de texto e de condições. Novas famílias semânticas recebem identidade própria.

## 15. Limitações

Modelos podem soar repetitivos, omitir implicações pragmáticas ou combinar partes gramaticais de forma inábil. Variação aleatória reduz a repetição apenas se as variantes permanecerem equivalentes no contexto observado.

## 16. Critérios de qualidade

Aplicar testes contrafactuais trocando um fato por vez e exigir ausência de afirmações objetivas sem suporte nos exemplos de aceitação. Julgar naturalidade, concordância e repetição em amostra cega. Reportar a cobertura com denominador explícito de contextos elegíveis.
