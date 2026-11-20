# Operar o piloto de Research

Execute os comandos a partir da raiz de `mimesis-knowledge`, em Linux com Python 3.11 ou posterior e uv. Para PDF textual, o executável `pdftotext` do Poppler deve estar no PATH. A instalação inicial resolve as dependências do lock. Com os pacotes em cache, acrescente `--offline` ao uv.

```sh
uv sync --locked
(cd pilot && sha256sum -c checksums.sha256)
uv run --locked python -m mkb prepare
uv run --locked python -m mkb stats
uv run --locked python -m mkb catalog work/catalog.json
uv run --locked python -m mkb candidates work/processed.jsonl
uv run --locked python -m mkb sheet work/revisao.csv
uv run --locked python -m mkb audit
MIMESIS_COMPILER_DIR=../mimesis uv run --locked pytest -q
uv run --locked ruff check .
```

`prepare` lê exclusivamente os dois lotes sintéticos identificados no [inventário](pilot/README.md). Preserva os bytes, origem declarada, hash, revisão e linha no banco editorial `work/editorial.sqlite`. O envelope exportado identifica o artefato por SHA-256 e a atividade por revisão. A consulta SQL por `artifact.hash` recupera os bytes originais. A classificação de intenção é atribuída na elaboração e validada contra o vocabulário. Polars agrega o inventário por intenção. DuckDB totaliza os estados dos pareceres. Uma modificação do candidato exige a revisão seguinte. Preserve a identidade dos membros ao revisar e crie outro Talkset se mudar a intenção.

`catalog` exporta as origens sintéticas, direitos pendentes, artefatos, atividades e eventos iniciais. Os arquivos locais já gerados podem ser consultados diretamente. `catalog`, `sheet` e `candidates` exigem um caminho de saída novo. Podem ser repetidos com outro nome. Para reproduzir os testes sobre o piloto em outro checkout, é preciso disponibilizar localmente os cinco JSONL sob custódia e conferir o inventário. Esses dados e o diretório de trabalho estão excluídos do Git enquanto a redistribuição estiver pendente.

## Revisão em lote

Entregue cópias em branco da planilha a dois revisores identificados. Cada pessoa mantém as colunas originais, pode selecionar um subconjunto de linhas e registra `accept` ou `reject` e a justificativa. Linhas sem parecer permanecem abertas. Para a revisão de uma família, ambos julgam cada combinação. Uma rejeição unânime de qualquer par impede a liberação do Talkset inteiro nessa revisão. A pessoa responsável pela sessão fornece o identificador real de quem preencheu a planilha. O SQLite local pressupõe custódia e controle de acesso pela equipe.

```sh
uv run python -m mkb vote "$REVIEWER_ID" "$COMPLETED_CSV"
uv run python -m mkb adjudicate "$RECORD_ID" "$REVISION" "$ADJUDICATOR_ID" accept "$RATIONALE_JSON"
uv run python -m mkb curate "$CURATION_JSON"
uv run python -m mkb export "$RELEASE_DECISION_JSON" "$NEW_EDITION_DIRECTORY"
```

Somente divergências requerem adjudicação. O arquivo de justificativa contém `summary` e um objeto `pairs` com a justificativa por chave `prompt_id/response_id`. O aceite exige decisão explícita sobre todos os pares divergentes. O banco mantém o parecer original, o adjudicador e o digest da evidência.

A decisão de curadoria é JSON com `record_id`, `revision`, `artifact_sha256`, `actor`, `group_id`, `decision=curate`, `internal_research=allowed`, `reviewed_at` em UTC com Z, `evidence_locator` relativo ao arquivo e `evidence_sha256`. A revisão precisa ter a matriz completa aceita. O comprovante deve documentar o grupo, a autorização aplicável e a decisão editorial.

A decisão de edição identifica `maintainer`, `decision=release`, `knowledge_version`, `created_at`, a lista `engine_compatibility` com o leitor de Research 0.0.0, `records` com pares record_id/revision, e comprovante por localizador e digest. O objeto `rights` usa o SHA-256 de cada original como chave. Cada parecer inclui decision, scope, jurisdiction, reviewer_id, reviewed_at, obligations, evidence_locator e evidence_sha256. O responsável deve confirmar o cumprimento das obrigações, a seleção e os ensaios em sua decisão antes da exportação. O formato completo é exercitado com evidências temporárias no [teste de integração](tests/test_pilot.py). O compilador recebe o digest aprovado do manifesto. [Contrato da projeção](../mimesis/docs/RESEARCH_COMPILER.md)

## Outras fontes

```sh
uv run python -m mkb.importer "$ORIGINAL" --decision "$INTAKE_DECISION_JSON" --store work/intake
```

A decisão de entrada contém `source_id`, `rights_id`, `artifact_sha256`, `reviewer_id`, `reviewed_at` em UTC, `jurisdiction`, lista `obligations`, `evidence_locator`, `evidence_sha256` e objeto `scope` com `copy_internal` e `extract` autorizados como `allowed`. O recibo e as unidades extraídas ficam em `intakes/<intake_id>/` e os originais em `objects/<sha256>` sob a pasta escolhida. TXT mantém a linha e JSONL preserva o objeto. Os demais adaptadores mantêm localizadores do formato. Para um original externo, a seleção semântica e o mapeamento para Talksets exigem trabalho editorial específico. O limite por arquivo é 16 MiB. PDF usa extração da camada de texto, sem OCR.

## Interpretação do ensaio

O relatório de `audit` compara consultas, controles, entradas, respostas e partições, registra os digests e identifica os diagnósticos previamente conhecidos. O limiar lexical 0,82 serve para triagem. A autoria compartilhada mantém o benchmark experimental. Um avaliador independente precisa produzir ou reservar outras consultas, julgar a relevância, rever famílias e congelar os artefatos e os critérios de erro antes da comparação confirmatória. [Benchmark](pilot/benchmark/README.md)
