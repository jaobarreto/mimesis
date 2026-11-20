# MIMESIS Lab · 0.0.0 Research

O Lab abre o protótipo científico sobre os seis Talksets de `synthetic-core-v1`, com oito entradas e sete respostas. Ative as fixtures na barra lateral. O Playground guarda até 50 envios na sessão do Streamlit. Cada chamada a `Experiment.query` recebe somente a mensagem atual. O Explorer lê as tabelas da projeção SQLite aberta para aquela execução. As únicas entradas do Lab são texto de consulta, seleções de interface e tamanhos predefinidos de fixtures de carga. [Fronteira experimental](../adr/0004-ISOLATED-RESEARCH-PROTOTYPE.md)

## Instalação e execução

A partir do checkout do motor em Linux, com Python 3.11 ou posterior, SQLite FTS5 e uv disponível no PATH, execute:

```sh
uv sync --locked --group lab
.venv/bin/python -m research_lab
```

Abra o endereço de loopback impresso pelo Streamlit. O grupo opcional instala as dependências do laboratório. Após a instalação, os ensaios funcionam offline. Para testar ou reproduzir as medidas em outro arquivo de saída, use:

```sh
.venv/bin/python -m pytest -q
.venv/bin/ruff check .
.venv/bin/python -m research_lab.study --fixture
.venv/bin/python -m research_lab.performance --size 100000
```

## Inspeção e diferença entre estratégias

O Inspector de cada envio exibe a trilha retornada pelo motor, incluindo critérios da política, escore bruto e escore de ordenação, candidatos bloqueados, respostas elegíveis e procedência da seleção. Os tokens exibidos são termos distintos em ordem lexical. A comparação mantém cada escala na coluna do respectivo método. [Política e implementação do protótipo](../RESEARCH_EXPERIMENT.md)

* Exact procura igualdade da chave normalizada no índice B-tree.
* Fuzzy percorre cada entrada considerando blocos contíguos coincidentes. Para cada direção calcula 2M/(m+n), onde M soma o comprimento dos blocos e m e n são os comprimentos das strings. Usa a média das duas direções, com a heurística automática desativada. O pior caso de SequenceMatcher é quadrático. [Documentação de difflib](https://docs.python.org/3/library/difflib.html#difflib.SequenceMatcher)
* Levenshtein percorre as entradas e calcula o menor número de inserções, remoções e substituições. Ordena por 1 − d/max(m,n). A implementação usa O(mn) tempo e O(n) memória auxiliar por par. Para “A janela está pronta?”, Fuzzy coloca window-p1 em terceiro lugar e Levenshtein coloca window-p2 nessa posição. A inversão, coberta pelo teste automatizado, mostra que os rankings podem diferir mesmo com as mesmas entradas e a mesma normalização.
* BM25 faz uma consulta disjuntiva ao índice invertido do FTS5. A função pondera frequência no documento, raridade do termo e comprimento do documento, com k1=1,2 e b=0,75. O motor inverte o sinal nativo para ordenar, usa cobertura de termos no mínimo e calcula a margem em relação ao melhor escore. [Fórmula do FTS5](https://sqlite.org/fts5.html#the_bm25_function)

## Benchmark técnico

Em 20 de novembro de 2026, o protocolo core-diagnostics-v1 executou seis consultas nos quatro recuperadores, alternando a ordem inicial a cada consulta. Cinco casos têm expectativas técnicas explícitas, incluindo duas consultas respondíveis e três que pedem abstenção. A sexta consulta tem julgamento nulo. As quatro abstenções nessa sondagem entram apenas na contagem operacional. A política fixture-ranking-v1 e seus limites estão no arquivo do ensaio, junto com os rankings e latências individuais. [Observações brutas](benchmark.json)

| Método | Consultas | Respostas corretas segundo a fixture | Respostas incorretas | Falsas aceitações | Abstenções totais |
|---|---:|---:|---:|---:|---:|
| Exact | 6 | 1 | 0 | 0 | 5 |
| Fuzzy | 6 | 2 | 0 | 0 | 4 |
| Levenshtein | 6 | 2 | 0 | 0 | 4 |
| BM25 | 6 | 2 | 0 | 0 | 4 |

Exact se absteve diante do erro de grafia em “Posso fechr a janela?”. Os outros três métodos selecionaram uma resposta da família esperada. A amostra é de engenharia, com expectativas definidas para a fixture. A avaliação de qualidade linguística depende de consultas independentes e julgamentos adjudicados. Research permanece aberta. [Critérios de avaliação](../EVALUATION.md)

## Carga sintética e recursos

Cada tamanho teve três execuções sequenciais em processos novos. Cada registro possui um Talkset, um prompt numerado e uma resposta. Usou-se o compilador de projeções e o recuperador exato existentes. O cronômetro de preparação inclui geração de fixtures, construção dos índices e verificações. O tempo FTS mede uma reconstrução adicional do índice pronto. O tempo de inicialização do núcleo mede a abertura de Experiment com a fixture padrão. O pico de RSS inclui o interpretador, o gerador Python e SQLite. Cada processo mediu 25 buscas em chaves determinísticas. A latência de busca exclui normalização, interface e política de resposta. As bases ocuparam zero bytes de arquivo SQLite, com tabelas e armazenamento temporário em memória. O tamanho lógico usa page_count × page_size. [Amostras, CPU, versões e digests por execução](performance.jsonl)

Ambiente observado: Intel Core i5-1235U, Linux x86-64, Python 3.14.4 e SQLite 3.46.1. Carga concorrente, frequência de CPU e cache do sistema não foram controlados. A tabela usa medianas das três execuções, exceto o p95 de busca, calculado sobre 75 observações por tamanho.

| Talksets | Preparação (ms) | Reconstrução FTS (ms) | Inicialização do núcleo (ms) | CPU do ensaio (ms) | Pico RSS (MiB) | SQLite lógico (MiB) | p95 busca exata (µs) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 100 | 3.74 | 0.21 | 1.83 | 8.63 | 23.14 | 0.08 | 11.45 |
| 1000 | 33.05 | 2.98 | 1.83 | 41.30 | 25.23 | 0.43 | 14.47 |
| 10000 | 329.01 | 27.91 | 1.98 | 355.49 | 45.48 | 3.85 | 38.38 |
| 50000 | 1789.42 | 147.16 | 1.87 | 1958.82 | 137.94 | 19.59 | 23.19 |
| 100000 | 3539.85 | 319.88 | 1.98 | 3869.18 | 253.37 | 39.55 | 24.96 |
