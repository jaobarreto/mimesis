# Protótipo experimental de recuperação em Research

A CLI executa quatro recuperadores independentes em CPU sobre a mesma projeção SQLite em memória. O ambiente requer Python 3.11 ou posterior com SQLite FTS5. O executável usa a biblioteca padrão. Os seis Talksets sintéticos incluem colisão intencional, negação e mudanças de pessoa. A opção obrigatória `--fixture` habilita esse repertório. Cada resultado identifica o modo `experimental_fixture`. [ADR proposto](adr/0004-ISOLATED-RESEARCH-PROTOTYPE.md)

## Instalação local

Execute na raiz do repositório. A montagem do aplicativo Python funciona offline.

```sh
python3 scripts/build_experiment.py /tmp/mimesis-experiment.pyz
python3 -I /tmp/mimesis-experiment.pyz --fixture --method exact 'Posso fechar a janela?'
python3 -I /tmp/mimesis-experiment.pyz --fixture --method fuzzy 'Posso fechr a janela?'
python3 -I /tmp/mimesis-experiment.pyz --fixture --method levenshtein 'Posso fechr a janela?'
python3 -I /tmp/mimesis-experiment.pyz --fixture --method bm25 'Podemos fazer um breve intervalo?'
python3 -I /tmp/mimesis-experiment.pyz --fixture --method exact 'A luz está pronta?'
```

O arquivo `.pyz` pode ser copiado para qualquer diretório. Para consultar diretamente do checkout, use `python3 -m research_experiment` com os mesmos argumentos. O JSON inclui entrada original e normalizada, tokens, escores, filtros, ranking de respostas antes da abstenção, proveniência da seleção e duração por consulta. Encaminhe apenas texto de ensaio, pois a CLI imprime o texto original no terminal. A duração exclui a preparação da projeção. O código de saída é 0 para resposta ou abstenção, 2 para dados de entrada inválidos e 1 para falha SQLite.

## Métodos e decisão

| Método | Escore nativo | Ordenação e mínimo |
|---|---|---|
| `exact` | Igualdade da forma normalizada | Escore 1. |
| `fuzzy` | Média das duas razões direcionais de blocos de caracteres do `SequenceMatcher` | Escore maior primeiro. Mínimo 0,79 e margem 0,04. |
| `levenshtein` | Número de inserções, remoções e substituições unitárias em pontos de código | Ordena por `1 − distância / comprimento máximo`. Mínimo 0,73 e margem 0,04. |
| `bm25` | BM25 nativo do FTS5 | Ordena por `−BM25`. Exige cobertura mínima de 60% dos tokens distintos da consulta no melhor prompt e diferença relativa de 12% para o segundo Talkset. |

A chave reaproveita NFC, casefold, NFC e redução de espaços do compilador. Igualdade e os dois métodos de caracteres preservam acentos e pontuação. A tokenização de busca usa o FTS5 `unicode61 remove_diacritics 0`. BM25 consulta a disjunção de literais obtidos com o mesmo tokenizador. A recuperação por caracteres trata variações ortográficas por similaridade. A verificação de negação usa a presença de marcadores explícitos e a verificação de pessoa usa a ordem relativa de pronomes. Ambas são heurísticas superficiais e podem excluir candidatos legítimos ou aceitar outras inversões.

O melhor prompt representa cada Talkset. A ordem lexical dos IDs resolve a ordem de apresentação em empates e escolhe a resposta elegível dentro da família. Empates entre famílias e margens insuficientes produzem abstenção. Cada escore pertence ao seu método. Os limites foram escolhidos para exercitar condições técnicas e seguem sem calibração estatística.

## Verificação e limites

```sh
uv sync --locked
uv run --locked pytest -q
uv run --locked ruff check .
```

O protótipo reconstrói o índice a cada execução. Fuzzy e Levenshtein percorrem todos os prompts. A CLI consulta somente a projeção das fixtures e registra referências de origem sintética. O fingerprint das fixtures e o digest lógico permitem repetir a mesma projeção. O experimento mede comportamento de casos controlados. A resposta a paráfrases com termos comuns pode ser observada nesses casos, enquanto a compreensão semântica, a resistência a falsos positivos e o custo em corpus maior exigem avaliação com data e ambiente fixados.

Para Genesis ainda são necessárias a curadoria humana e a autorização de uma edição piloto, sua integração e compatibilidade verificadas, consultas reservadas independentes com julgamentos adjudicados, política congelada e comparação pareada no notebook alvo, incluindo falsas aceitações e recursos. [Critérios de Genesis](releases/0.0.1-GENESIS.md)
