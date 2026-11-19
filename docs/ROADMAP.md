# Roadmap oficial

| Versão | Codinome | Objetivo |
|---|---|---|
| 0.0.0 | Research | Pesquisa e engenharia de dados |
| 0.0.1 | Genesis | Recuperação textual |
| 0.0.2 | Lexicon | Similaridade semântica |
| 0.0.3 | Persona | Personalidades intercambiáveis |
| 0.0.4 | Context | Seleção contextual |
| 0.0.5 | Mythos | Narração de ambientes |
| 0.0.6 | Logos | Composição procedural de textos |
| 0.0.7 | Mnemosyne | Memória conversacional |
| 0.0.8 | Anima | Simulação de reações emocionais |
| 0.0.9 | Sophia | Aprendizado supervisionado |
| 0.1.0 | Awakening | Integração das capacidades |
| 1.0.0 | Mimesis | Primeira versão estável |

**Decisão aprovada.** A partir de Genesis, cada linha exige instalação local, execução de ponta a ponta em CPU e preservação das capacidades anteriores. Uma biblioteca, um notebook ou uma métrica isolada não satisfaz o critério de encerramento. Os domínios citados abaixo são dependências de informação. O tamanho dos lotes e os limiares quantitativos serão fixados antes do primeiro teste reservado de cada etapa.

| Versão | Requisito e dependências | Entregável cumulativo | Aceitação específica | Evidência para encerrar |
|---|---|---|---|---|
| Research | Fronteiras do motor, MKB, proveniência e direitos. Depende do briefing e de fontes verificáveis. | Documentação dos dois repositórios, contratos e desenho do piloto. | Rastrear uma fala da interação ao original e à decisão de direitos no desenho. Cobrir dez domínios, avaliações e contingências. | Revisar documentação. Encerramento integral da fase ainda requer piloto coletado, curado e validado e decisão de prontidão para Genesis. |
| Genesis | Consumir MKB-DLG compatível e consultas pt-BR julgadas. | Produto local de consulta, ranking, fallback, trilha e comparador. | Recuperar fala conhecida, abster-se em desconhecida e reproduzir os candidatos dos três controles. | Instalação limpa, relatório de comparação, matriz de compatibilidade e limites registrados. |
| Lexicon | Reusar Genesis, MKB-LEX/SEM com relações autorizadas e sentidos. | Expansão ou comparação conceitual explicável no mesmo fluxo. | Melhorar casos de paráfrase segundo critério pré-fixado e preservar negação e homônimos de controle. | Ablação com/sem relação, por sentido e registro linguístico, mais suíte Genesis. |
| Persona | Perfis intercambiáveis de MKB-PSY e expressão rotulada. | Seleção de voz por traço e saída com motivo. | Alternar perfil no mesmo cenário, preservar conteúdo factual e isolar perfis entre sessões. | Julgamento cego de pares e rastreio até o traço. |
| Context | Contexto externo tipado, MKB-CTX e candidatos condicionais. | Aplicação de condições positivas, negativas e desconhecidas. | Perturbar um atributo por vez e testar ausência, contradição e expiração. | Suite de pares contrafactuais e histórico de decisões sobre precedência. |
| Mythos | Fatos de ambiente autorizados e MKB-NAR. | Descrição de um ambiente a partir de um instantâneo. | Cobrir atributos obrigatórios, omitir ou esclarecer os desconhecidos, preservar persona e contexto. | Julgamento factual por proposição e avaliação narrativa por cenário. |
| Logos | Planos narrativos de Mythos, gramática e léxico flexionável. | Composição de sentenças com origem de cada slot. | Concordância de gênero/número, slots ausentes tratados e término garantido. | Relatório de fidelidade, diversidade e casos de gramática. |
| Mnemosyne | Sessões identificadas e eventos com origem, duração e escopo. | Recuperação de informação entre turnos na mesma sessão. | Atualização de fato vence observação antiga, expiração funciona e sessões ficam isoladas. | Replay de sequências e avaliação de contradições por turno. |
| Anima | Persona, contexto, memória, MKB-PSY/BEH. | Reações simuladas condicionadas e temporárias. | Variar estímulo mantendo fatos e explicar mudança e retorno do estado. | Avaliação cega de adequação e testes de transição e limites. |
| Sophia | Feedback atribuído, MKB-LRN e fluxo de aprovação. | Sugestão, revisão humana, edição candidata e retorno à anterior válida. | Feedback pendente não altera resposta servida. Promoção requer avaliação em dados isolados. | Histórico de aprovação/rejeição e comparação das duas edições. |
| Awakening | Todas as capacidades e pacotes anteriores. | Motor integrado com uma interface de sessão e trilha completa. | Executar cenário multivolta cobrindo busca, emoção, memória, composição e revisão. | Instalação offline e replay da cadeia integrada com matriz de dependências. |
| Mimesis | Awakening validado, contratos públicos e política de compatibilidade. | Primeira distribuição estável, instruções de operação, migração e recuperação. | Consumidor independente instala e reproduz cenário de referência, migra dados suportados e restaura uma edição válida. | Matriz pública testada, limites de suporte e revisão das pendências bloqueadoras. |

O mesmo [protocolo de avaliação](EVALUATION.md) identifica as métricas pertinentes a cada degrau. As especificações de [Research](releases/0.0.0-RESEARCH.md) e [Genesis](releases/0.0.1-GENESIS.md) detalham as duas primeiras entregas.
