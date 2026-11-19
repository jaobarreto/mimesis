# ADR 0004 · Protótipo científico isolado durante Research

**Estado** — proposta para revisão dos mantenedores. O pedido de execução experimental autoriza o ensaio técnico isolado. A adoção dessa fronteira como regra geral permanece em avaliação.

**Contexto.** O roadmap, as instruções do motor e o escopo reservam a implementação funcional para Genesis. Há interesse em verificar antecipadamente se a projeção suporta recuperação, ranking e abstenção reproduzíveis. O piloto da MKB aguarda direitos e revisão humana.

**Proposta.** Permitir uma CLI científica 0.0.0 com fixtures próprias, em memória, selecionadas explicitamente. Reutilizar a projeção relacional e seu perfil de normalização. A CLI tem identidade experimental, entrada independente e nenhum caminho para carregar uma edição externa ou os conjuntos reservados. Medidas obtidas com fixtures documentam comportamento técnico. A prontidão de Genesis segue o roadmap e os critérios de avaliação vigentes.

**Alternativas e consequências.** Esperar Genesis permitiria testar o recuperador diretamente com uma edição autorizada e adiaria a verificação da interface. Abrir a CLI a qualquer SQLite reduziria o trabalho de integração posterior e perderia a garantia de separação na entrada. A projeção em memória oferece casos reproduzíveis e restringe a evidência ao pequeno conjunto experimental.

**Evidência e revisão.** Os casos técnicos cobrem os métodos isolados, trilha, ambiguidades, ausência de candidatos e integridade SQLite. Revisar este ADR antes de abrir uma entrada para edições da MKB, comparar métodos em dados adjudicados ou adotar a política experimental em uma distribuição oficial. [Protótipo](../RESEARCH_EXPERIMENT.md) · [Genesis](../releases/0.0.1-GENESIS.md)
