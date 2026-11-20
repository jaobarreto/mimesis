# MKB-DLG · Conhecimento de diálogo

**Proposta para Genesis.** Um Talkset reúne formulações de entrada e um repertório explícito de respostas curadas. A associação é editorial e deve poder ser testada sem rede, memória de sessão ou perfil de personalidade. Esta convenção pertence ao MIMESIS. As inspirações históricas não especificam seu funcionamento interno.

## 1. Finalidade

Oferecer a menor unidade de conhecimento da recuperação conversacional local. O pesquisador deve conseguir explicar qual entrada levou a qual grupo e por que uma resposta estava elegível.

## 2. Escopo

Talksets, entradas exemplares, respostas exemplares e, quando houver perfil específico, descrições de intenção. Um mesmo enunciado pode ser ambíguo entre grupos. O domínio não escolhe o algoritmo de recuperação, seu limiar de rejeição ou seu desempate.

## 3. Responsabilidades

Manter identidade dos grupos e de seus membros, coerência de sentido, compatibilidade de registro e adequação de cada resposta para **cada** formulação. Anotar restrições adicionais apenas se houver um contrato de consumidor que as aplique.

## 4. Tipos de conhecimento

Formulação de entrada, variação de entrada, realização de resposta e grupo de equivalência conversacional sob condições declaradas. Uma intenção é uma categoria humana opcional. Uma correspondência textual alta não a demonstra por si.

## 5. Estrutura dos registros

O envelope contém `domain=MKB-DLG` e a identidade do Talkset em `record_id`. O payload mínimo requer `prompts` e `responses`, duas listas não vazias. Cada membro inclui identificador estável e `text` não vazio. A chave estrangeira `talkset_id` de índices, testes e trilhas tem o valor de `record_id`. O exemplo contém apenas o payload autoral.

```json
{
  "prompts": [
    {"prompt_id":"p21","text":"Posso fazer uma pergunta?"},
    {"prompt_id":"p22","text":"Posso perguntar uma coisa?"}
  ],
  "responses": [
    {"response_id":"r71","text":"Pode perguntar."},
    {"response_id":"r72","text":"Claro. Qual é a sua dúvida?"}
  ]
}
```

## 6. Relações entre entidades

Um grupo com *m* entradas e *n* respostas expressa *m × n* pares elegíveis. No exemplo, as quatro combinações devem passar em revisão. Se uma resposta puder ser usada apenas com “quando?”, separar o grupo que inclui “onde?” antes de publicar. Uma trilha identifica versão do conhecimento, grupo, entrada recuperada e resposta escolhida.

## 7. Metadados obrigatórios

Usar o [envelope comum](../METADATA_SPECIFICATION.md), inclusive origem e direitos para contribuições próprias. Cada membro precisa ter sua origem recuperável se o grupo reunir formulações de fontes diferentes. Fixar no manifesto as versões do esquema, das regras de normalização e a seleção curada.

## 8. Fontes candidatas

Autoria original em pt-BR é um caminho inicial para produzir exemplos positivos e contraexemplos controlados. LIGHT, LIGHT WILD, PersonaChat, NPC Dialogue v2, WorryFree RolePlaying Scenarios e Video Game Dialogue Corpus são candidatos à análise individual. Língua, licença e finalidade precisam ser verificadas por componente. Tradução produz derivação com procedência própria. [Catálogo de fontes](../DATASET_REGISTRY.md)

## 9. Importação

Preservar ordem e identidade de turnos na ingestão. Propor pares somente após identificar papéis, dependências do contexto e material não conversacional. Dois turnos consecutivos podem conter pergunta e mudança de assunto. A sequência cronológica só fornece evidência candidata.

## 10. Processamento

Gerar formas normalizadas derivadas, agrupar paráfrases sugeridas e revisar a matriz de pares. Inspecionar negação, interrogativos e alteração de pessoa. “Você pode repetir?” e “Você não pode repetir?” podem compartilhar termos e exigir interpretações diferentes. Manter o texto de apresentação intacto.

## 11. Validação

Bloquear grupos sem entradas ou respostas, IDs repetidos no respectivo escopo, texto em branco e combinações contraditórias. Checar que uma resposta apta a Genesis não dependa de um fato ausente, de memória futura ou de ação externa. Casos de prompts idênticos em grupos diferentes devem ter tratamento de ambiguidade documentado.

## 12. Indexação

Propor uma linha por entrada, vinculada a `talkset_id`, e uma tabela de respostas ligadas ao mesmo grupo. Indexar texto normalizado para exact matching e testar FTS5 para BM25. O construtor preserva a ligação de volta ao texto original. Agrupar ocorrências do mesmo grupo ao comparar ranking de grupos para evitar premiar mera duplicação de paráfrases.

## 13. Utilização pelo motor

Genesis recupera entradas, pontua candidatos, agrupa por Talkset segundo uma política declarada e seleciona somente membros elegíveis. O motor pode se abster e usar fallback. Um fallback precisa aparecer na trilha como tal, sem ser contado como acerto de recuperação. Os candidatos e as pontuações devem permitir comparar exact, fuzzy e BM25 na mesma release. [Especificação de Genesis](../../../mimesis/docs/releases/0.0.1-GENESIS.md)

## 14. Versionamento

Corrigir pontuação mantendo o sentido gera nova revisão com a identidade do membro preservada. Mudança de significado cria outro membro. Dividir um Talkset exige novos grupos ou um mapeamento explícito de continuidade. A avaliação anterior continua apontando para o conjunto e a revisão originais.

## 15. Limitações

Compatibilidade entre todos os pares restringe a variedade admissível em um único grupo. Uma resposta genérica pode mascarar baixa relevância. O repertório só cobre exemplos validados e se beneficia de uma política honesta para entradas desconhecidas.

## 16. Critérios de qualidade

Auditar a matriz de elegibilidade e avaliar paráfrases reservadas, negativos próximos, consultas fora de cobertura e duplicatas entre grupos. Medir relevância da recuperação e adequação da resposta em etapas distintas. Agrupar famílias de paráfrases antes de separar desenvolvimento e avaliação. [Conjuntos de benchmark](../BENCHMARK_DATASETS.md)
