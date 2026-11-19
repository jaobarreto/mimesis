# Compilador experimental de Research

O compilador 0.0.0 permite ensaiar localmente a transferência de Talksets entre a MKB e o motor. O perfil fechado `research-dlg-v1` admite uma origem por revisão e apenas falas autocontidas em pt-BR. A curadoria e a decisão de liberar uma edição pertencem à MKB. O código requer Python 3.11 ou posterior com SQLite e FTS5. A execução usa a biblioteca padrão.

## Executar

Na raiz do motor, informe o diretório do pacote, um destino com extensão `.sqlite` fora dele e o SHA-256 do manifesto obtido do responsável pela edição. O diretório de destino deve existir. Use um destino dedicado à projeção, sem processo de escrita concorrente.

```sh
python -m research_compiler "$pacote" "$destino" --manifest-sha256 "$digest_autorizado"
```

O recibo JSON em stdout identifica as versões da MKB, esquema, compilador, Python, SQLite e Unicode, o perfil, os digests de manifesto, configuração e conteúdo lógico e a contagem de cada relação. O erro aparece em stderr com código de saída 1. O compilador constrói um temporário no diretório do destino, confirma as chaves estrangeiras e a integridade do SQLite e do FTS5 em relação aos prompts, fecha a conexão e troca o arquivo por renomeação atômica. Uma falha anterior à troca conserva a base anterior.

## Entrada para o exportador da MKB

1. Exporte `records.jsonl` em UTF-8, um objeto completo por linha, com LF final. Cada registro usa o envelope do [contrato de metadados](../../mimesis-knowledge/docs/METADATA_SPECIFICATION.md), estado `RELEASED`, domínio `MKB-DLG`, idioma `pt-BR` e esquema `0.1.0`. O payload contém `prompts` e `responses` não vazios, cada membro com ID e texto original. Os IDs são únicos por coleção na edição.
2. Exporte `catalog.json` com as listas `sources`, `artifacts`, `rights` e `activities` conforme as colunas dos quatro cadastros do mesmo contrato. Inclua `reviews`, com um objeto por revisão selecionada contendo `record_id`, `revision`, `reviewer_ids` (dois IDs distintos) e `decision` igual a `approved`. Esse resumo pressupõe o julgamento de todos os pares e o encerramento das divergências sob custódia da MKB.
3. No cadastro de direitos, registre `decision` igual a `approved`, localizador de evidência, jurisdição, revisor, data UTC, obrigações como lista de strings e as seis operações de `scope` permitidas por este perfil: `access`, `internal_copy`, `extraction`, `transformation`, `local_query` e `redistribution`. Cabe ao responsável pela publicação conferir a evidência privada e o cumprimento das obrigações.
4. No cadastro de artefatos, registre o digest e o tamanho dos bytes originais, a origem, os direitos e o localizador sob custódia. O envelope referencia o artefato e o trecho, por exemplo `line:1` para uma fonte `application/x-ndjson`. As atividades formam uma cadeia ordenada a partir do ID do artefato. As entradas de cada passo devem estar nas saídas do anterior. O último passo inclui `record_id@revision` em `output_ids`. Os catálogos contêm somente entidades utilizadas pela seleção.
5. Grave `manifest.json` com os campos da tabela. Chaves JSON repetidas, campos extras e revisões duplicadas são erros. Calcule os digests após a serialização final. Entregue o digest aprovado do manifesto por um canal local confiável. Os originais e os comprovantes de direitos ficam na MKB. A compilação verifica as referências e os bytes transportados, e depende da atestação editorial para as autorizações e o conteúdo sob custódia.

| Campo | Convenção do piloto |
|---|---|
| `knowledge_version` | Versão independente da edição, três inteiros decimais separados por ponto. |
| `schema_version`, `build_profile` | `0.1.0` e `research-dlg-v1`. |
| `engine_compatibility` | Lista fechada de versões exatas que inclui `0.0.0` para o leitor experimental. |
| `artifacts` | Duas entradas com `path`, `byte_length`, `sha256`, referentes a `records.jsonl` e `catalog.json`. |
| `records` | Uma entrada com `record_id` e `revision` por identidade. |
| `rights_summary` | Lista de IDs dos pareceres usados nas revisões. |
| `created_at` | Instante UTC com sufixo Z. |

A projeção mantém o original e uma chave de prompt calculada por NFC, casefold, NFC e redução dos espaços. O FTS5 usa `unicode61 remove_diacritics 0`. O digest lógico cobre linhas de `talkset`, `prompt` e `response` nessa ordem, por chave binária UTF-8. Cada linha contribui com um array JSON compacto UTF-8 formado pelo nome da tabela seguido das colunas em ordem de criação e terminado em LF. Compare também os digests de manifesto e configuração para reproduzir o ensaio. Mudanças de biblioteca SQLite podem alterar os bytes físicos.

## Verificar o ensaio

```sh
uv sync --locked
uv run --locked pytest -q
uv run --locked ruff check .
```

Os casos positivos constroem dados sintéticos sob o diretório temporário dos testes. O recibo de um teste verifica o contrato técnico. A matriz de compatibilidade de uma edição real exige os resultados do lote autorizado.

O campo `sqlite_sha256` do recibo identifica os bytes finais do índice. As instruções de coleta, curadoria e exportação do pacote estão no [guia operacional da MKB](../../mimesis-knowledge/RESEARCH.md).
