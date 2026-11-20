# Repertório experimental dlg-pilot-001

Em 19 de novembro de 2026, Codex preparou candidatos sintéticos de diálogo cotidiano em português brasileiro para experimentar recuperação local. Cada uma das dez intenções tem cinco Talksets. Os dados se destinam ao trabalho de Research. O mantenedor da edição e os revisores humanos ainda precisam ser identificados.

| Arquivo e origem | Talksets | Entradas | Respostas | Pares a revisar |
|---|---:|---:|---:|---:|
| `codex.jsonl`, material sintético redigido por Codex para o piloto | 49 | 98 | 198 | 396 |
| `contribution.jsonl`, contribuição sintética atribuída a ChatGPT e encaminhada pelo usuário, preservada em `dlg-026` | 1 | 2 | 2 | 4 |
| Total | 50 | 100 | 200 | 400 |

Cada linha contém o identificador estável `id`, a categoria `intent` e duas listas ordenadas de textos, `prompts` e `responses`. A posição de cada resposta, contada a partir de 1, forma o identificador usado pelo avaliador, por exemplo `dlg-026-r1`. A resposta é candidata para cada entrada do seu Talkset. O grupo `dlg-001` contém seis respostas, a contribuição contém duas e os demais contêm quatro. O vocabulário de categorias é Greeting, Farewell, Gratitude, Introduction, Help Request, Permission Request, Information Request, Apology, Agreement e Disagreement.

O arquivo `controls.jsonl` preserva duas entradas encaminhadas com a mesma contribuição. Cada linha contém `id`, `kind`, `talkset_id` e `text`. Um controle inverte quem deve fazer a pergunta. O outro pergunta onde fica uma biblioteca sem fornecer sua localização. Ambos são controles de avaliação. Os dados não incluem transcrições pessoais, importação de diálogos externos ou os dois exemplos de oficina da ficha inicial.

## Direitos e curadoria

A origem informada pelo usuário identifica a contribuição como geração de ChatGPT. A solicitação motivou a preparação local deste lote. Nenhuma licença de redistribuição, autorização territorial ou cessão de direitos é presumida. Uma decisão documentada por origem e operação continua pendente para a promoção e publicação de uma edição. O uso de material sintético precisa permanecer explícito nos derivados.

Os 400 pares aguardam revisão humana. Para cada par, dois revisores devem julgar independentemente se a resposta serve à formulação, preserva o registro pretendido e depende de algum fato omitido. Registrar suas decisões individuais e adjudicar desacordos antes de promover a revisão. O mesmo cuidado se aplica às classes e relevâncias propostas para a avaliação. Há zero pareceres humanos neste pacote.

## Avaliação

| Partição | Consultas | Famílias | Respondíveis | Fora de cobertura | Ambíguas |
|---|---:|---:|---:|---:|---:|
| Desenvolvimento | 15 | 13 | 11 | 2 | 2 |
| Teste exploratório | 15 | 13 | 11 | 2 | 2 |
| Diagnóstico | 3 | 1 | 1 | 2 | 0 |
| Total | 33 | 27 | 23 | 6 | 4 |

Codex escreveu as 30 consultas de desenvolvimento e teste, além das propostas de julgamento para as 33 consultas. O diagnóstico usa três textos encaminhados pelo usuário, incluindo uma entrada exata do Talkset e os dois controles. As famílias locais permanecem em uma única partição. A autoria compartilhada entre catálogo, consultas e julgamentos limita a interpretação dos resultados. Generalização para falantes reais exige coleta independente e avaliação reservada. O avaliador acessa os julgamentos separadamente do índice do motor. [Procedimento e esquema do benchmark](benchmark/README.md)

Os cinco arquivos JSONL usam UTF-8, um objeto por linha e ordem estável. A partir deste diretório, execute `sha256sum -c checksums.sha256` para conferir seus bytes. [Inventário SHA-256](checksums.sha256)
