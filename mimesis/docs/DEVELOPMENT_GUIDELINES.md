# Desenvolvimento e pesquisa reproduzíveis

**Fluxo de mudança.** Identificar a capacidade e versão do [roadmap](ROADMAP.md), o comportamento atual e um caso observável que justifique a alteração. Definir a comparação antes de ajustar algoritmo, corpus ou métrica. Arquivar hipótese, condição que a refuta, critérios de encerramento, responsáveis e dependências entre repositórios.

| Mudança | Evidência a incluir na revisão |
|---|---|
| Normalização ou ranking | Consulta afetada, perfil antigo e novo, resultados no mesmo conjunto, impacto em empates e desconhecidos. |
| Formato público ou tipo de campo | Migração, compatibilidade, comportamento com artefatos antigos e revisão coordenada na MKB. |
| Novo algoritmo | Baseline, custo no notebook, limitações por variedade, origem de bibliotecas e justificativa para obrigatoriedade ou experimento opcional. |
| Dados | Origem, licença específica, revisão e nova edição de conhecimento. Uma atualização do motor consome o manifesto identificado. |
| Decisão de arquitetura | ADR com alternativas, consequências, estado, evidência e condição de revisão. |
| Documento | Fonte primária para fato externo, rótulo de proposta para escolhas locais, links aos contratos afetados e exemplo sintético quando necessário. |

A estrutura futura do motor prevê `src/mimesis` para código, `lab` e `notebooks` para exploração, `experiments` para protocolos repetíveis, `benchmarks` para execução de avaliações e `tests` para regressões. `configs` e `scripts` surgirão quando houver consumidores. `pyproject.toml` e lockfile acompanharão o primeiro ambiente instalável. A seleção da licença do código é uma decisão dos titulares.

**Pacote de experimento proposto.** Registrar `experiment_id`, hipótese, commits, `knowledge_version`, hash de dados, ambiente, parâmetros, semente quando houver sorteio, regra de particionamento, comando de reprodução, resultados por consulta, análise e decisão. Variações de tempo, identificadores de execução e metadados de ambiente ficam separadas das saídas determinísticas.

**Trabalho paralelo.** Uma pessoa responde por cada campo canônico. Consumidores submetem propostas com exemplos mínimos e lista de documentos atingidos. Uma mudança independente de texto pode avançar em paralelo. Alterar o sentido de uma chave pública requer revisão conjunta antes de liberar dados ou binários. [Instruções para agentes](../AGENTS.md) · [Decisões](adr/README.md)
