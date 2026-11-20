# ADR 0003 · Comparação de recuperadores em Genesis

**Estado** — proposta a validar com corpus e julgamentos pt-BR.

**Contexto.** Igualdade, distância de edição e relevância por termos respondem a problemas distintos. Somar seus escores brutos produziria valores dependentes de escala e poderia atribuir confiança indevida a palavras frequentes.

**Proposta.** Implementar futuramente os três modos isolados sobre os mesmos prompts e respostas. Preservar escore nativo, orientação, motivo de abstenção e identificadores. Calibrar por método em desenvolvimento, congelar parâmetros e comparar no conjunto reservado.

**Alternativas e consequências.** Uma cascata pode economizar tempo nos acertos exatos e merece ensaio próprio. Fusão ponderada pode recuperar candidatos complementares e exige calibração e análise de ablação. A comparação isolada custa execuções adicionais e permite atribuir ganhos e perdas a cada método.

**Condição de aprovação.** Relatório pareado com relevância, falsa aceitação de desconhecidos, amostras de erro, latência e memória no alvo. A escolha de estratégia padrão e limites quantitativos depende dos resultados. [Genesis](../releases/0.0.1-GENESIS.md) · [Métricas](../EVALUATION.md)
