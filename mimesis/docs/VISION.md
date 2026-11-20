# Visão de pesquisa

A pergunta central é até que ponto um motor local consegue sustentar uma interação em pt-BR quando tem acesso a repertório conhecido, contexto explícito e uma política inspecionável de seleção. “Inteligência” designa aqui capacidades observáveis. Reconhecer um pedido conhecido, pedir esclarecimento e manter o mesmo ponto de vista são tarefas diferentes. Cada uma exige dados, um controle experimental e critérios de erro próprios.

A primeira aplicação é narrativa. Um sistema externo fornece participantes, ambiente e acontecimentos. Por exemplo, se fornece que uma janela está fechada, o motor poderá selecionar uma descrição compatível. Se omite o tempo meteorológico, inferir chuva e afirmá-la como fato comprometeria a fidelidade. Esse caso permite testar o projeto sem implementar regras de jogo. A mesma interface deve aceitar um cenário literário ou uma conversa sobre objetos de um acervo.

| Pergunta | Evidência que faria avançar a pesquisa |
|---|---|
| Quanto repertório é realmente recuperável? | Comparar equivalência exata, edição e BM25 na mesma coleção e nas mesmas consultas inéditas, incluindo entradas sem resposta. |
| Uma base de conceitos ajuda em paráfrases? | Medir ganho nas paráfrases sem palavras em comum e dano por ambiguidade ou negação. |
| Traços e contexto mudam a expressão preservando os fatos? | Avaliar pares de saídas do mesmo cenário mudando uma condição por vez, com avaliadores cegos à configuração. |
| A composição aumenta variedade útil? | Medir diversidade juntamente com contradições, concordância e repetição em sessões completas. |

**Decisão aprovada pelo escopo.** Priorizar português brasileiro, baixo custo, execução offline, dados de proveniência rastreável, evolução cumulativa e supervisão humana. O horizonte de generalização inclui outras aplicações e variedades linguísticas. O êxito em um benchmark representa evidência para a tarefa e a população testadas. A [filosofia](PHILOSOPHY.md) define como interpretar essas evidências e o [roadmap](ROADMAP.md) distribui as capacidades.
