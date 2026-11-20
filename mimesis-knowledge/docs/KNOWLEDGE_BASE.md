# Mimesis Knowledge Base

A MKB reúne os conhecimentos que o motor poderá citar ao explicar uma decisão. Sua unidade de entrega é uma seleção versionada de registros com origem e direitos identificados. Texto original, anotação humana, regra proposta e índice derivado têm funções distintas. Um trecho em que alguém faz uma pergunta pode fundamentar uma anotação sobre diálogo. Até que uma pessoa revise a relação entre entrada e resposta, esse trecho permanece evidência literária.

**Decisões da fase Research.** O projeto tem dez domínios lógicos, prioridade inicial para pt-BR, curadoria supervisionada e distribuição independente do motor. Bases externas elegíveis e autoria própria são frentes complementares. O motor consumirá dados locais e manterá rastreável o conhecimento usado em cada seleção. Esta especificação descreve uma arquitetura a construir.

## Onde registrar cada afirmação

| Uma pessoa quer registrar… | Domínio responsável | Unidade que pode ser revista |
|---|---|---|
| A ocorrência de uma fala em determinada edição | [MKB-LIT](domains/MKB-LIT.md) | Fragmento ancorado ao texto da edição |
| A grafia, flexão ou categoria de uma palavra ou locução | [MKB-LEX](domains/MKB-LEX.md) | Entrada lexical e formas atestadas |
| Uma acepção ou relação de significado delimitada | [MKB-SEM](domains/MKB-SEM.md) | Conceito ou aresta tipada |
| Enunciados que admitem o mesmo conjunto de respostas | [MKB-DLG](domains/MKB-DLG.md) | Talkset e seus membros identificados |
| Uma realização textual com posições a preencher | [MKB-NAR](domains/MKB-NAR.md) | Modelo e contrato dos seus parâmetros |
| Quais fatos um cenário precisa fornecer para uma condição ser verdadeira | [MKB-CTX](domains/MKB-CTX.md) | Definição tipada de sinal ou predicado |
| Uma preferência de expressão de uma persona ficcional | [MKB-PSY](domains/MKB-PSY.md) | Perfil, traço ou categoria emocional |
| Uma reação comunicativa elegível em certas circunstâncias | [MKB-BEH](domains/MKB-BEH.md) | Alternativa comportamental condicionada |
| Uma conclusão admissível a partir de premissas declaradas | [MKB-REA](domains/MKB-REA.md) | Regra ou caso justificado |
| Uma correção humana e a evidência para avaliá-la | [MKB-LRN](domains/MKB-LRN.md) | Observação supervisionada vinculada à versão avaliada |

Dicionários, diálogos e narrativas são também nomes de coleções físicas possíveis. O domínio pertence ao registro. Um arquivo de expressões pode originar uma entrada lexical e, após revisão independente, um conceito semântico. A coincidência de texto não estabelece identidade.

## Exemplo de derivação entre domínios

Considere a frase autoral fictícia “A luz da sala continua acesa?”. Uma anotação em LIT localizaria os caracteres na edição de origem. Uma entrada em LEX descreveria o lema “luz”. Em SEM, “luz” poderia ter mais de uma acepção, e a anotação precisaria escolher uma delas ou deixar a ligação em aberto. Em DLG, uma pessoa poderia propor “Não recebi essa informação” como resposta a consultas sobre estado desconhecido. Para perguntar pelo estado real, CTX precisaria declarar o campo que o integrador pode fornecer. A simples presença da frase na literatura não preenche esse campo. Cada transformação que gera novo conhecimento identifica as fontes e o responsável pela interpretação.

## Entregas por capacidade

| Marco do motor | Conteúdo candidato à primeira investigação | Pergunta de aceitação |
|---|---|---|
| Genesis | DLG, subconjunto autorizado de uma release compatível | É possível remontar cada associação entre entrada e resposta e excluí-la ao revogar a fonte? |
| Lexicon | LEX e SEM | Um vínculo de sentido pode ser explicado e desativado sem perder a forma original? |
| Persona e Context | PSY e CTX | O perfil e os fatos declarados pelo integrador produzem filtros reproduzíveis? |
| Mythos e Logos | NAR e derivações autorizadas de LIT | Toda afirmação factual realizada tem suporte no contexto? |
| Mnemosyne e Anima | CTX, PSY e BEH | O consumidor distingue um relato corrente de um traço estável e de uma escolha de expressão? |
| Sophia e Awakening | LRN, integração de regras e evidências REA | Uma correção aprovada gera uma nova revisão e admite comparação cega com a anterior? |

São prioridades de investigação. Uma release pode oferecer um subconjunto explícito dos domínios. Uma capacidade só se torna disponível depois de implementada e avaliada no motor. O repositório de dados não recebe sessões particulares para servir como memória operacional.

## Como propor conhecimento

Antes de importar, delimite a unidade de origem, o idioma, as permissões de derivação e o destino autorizado. Antes de curar, indique que afirmação o registro sustenta e em quais casos falha. Antes de publicar, confira o fechamento das referências, os grupos reservados à avaliação e a reprodução do artefato. Uma pendência de direitos ou de interpretação deve continuar visível no histórico. Consulte o [catálogo de fontes](DATASET_REGISTRY.md), o [pipeline](DATA_PIPELINE.md), a [arquitetura](ARCHITECTURE.md) e o [protocolo de qualidade](DATA_QUALITY.md).
