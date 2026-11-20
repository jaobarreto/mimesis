# Princípios e consequências verificáveis

| Princípio do projeto | Consequência observável numa revisão |
|---|---|
| Offline-first, LLM-free, independência | Com dependências e pacote local preparados, desconectar a rede e repetir a sessão em CPU. Toda função obrigatória continua acessível. |
| Orientação a dados, modularidade e separação de responsabilidades | Trocar uma edição compatível da MKB dispensa alterar regras no consumidor. Trocar a busca conserva o formato dos casos e julgamentos. |
| Contexto e persona | Identificar quais fatos e traços participaram da escolha. Fato externo restringe a saída mesmo quando um traço favoreceria outra fala. |
| Explicabilidade e procedência | Partir de uma resposta, localizar candidato, política e versão, resolver a revisão do registro e chegar à fonte e aos direitos. |
| Baixo custo e reprodutibilidade | Publicar condições de medição junto à qualidade. Repetir no equipamento de referência com a partição, o índice e a configuração fixados. |
| Aprendizado supervisionado | Feedback vira sugestão identificada. Um revisor pode rejeitá-la. O repertório servido muda apenas após liberação de outra versão. |
| Evolução e não regressão | Cada versão funcional instala o produto completo, passa pelos casos obrigatórios de todas as anteriores e explica qualquer diferença nas medidas. |

**Convenção editorial.** “Decisão aprovada” exige determinação no briefing ou decisão posterior registrada por quem responde pelo projeto. “Proposta arquitetural” descreve um contrato que pode ser revisado antes de implementar. “Hipótese experimental” inclui uma observação capaz de contrariá-la. “Questão pendente” indica a decisão e a evidência necessária. “Limitação conhecida” explicita o alcance de uma capacidade ou evidência. “Informação verificada” remete a uma fonte primária ou observação local identificada.

Quando objetivos entram em conflito, preservar os fatos e os direitos é condição de elegibilidade. Entre respostas elegíveis, comparar relevância e custo. Se variar a formulação compromete fidelidade, registrar o erro por categoria antes de considerar ganho de diversidade. O histórico de decisões e os resultados experimentais têm papéis diferentes na evolução da política. [ADRs](adr/README.md) · [Avaliação](EVALUATION.md)
