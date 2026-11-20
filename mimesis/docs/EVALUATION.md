# Avaliação científica e julgamento humano

**Proposta de desenho.** A unidade de recuperação é uma consulta com conjunto julgado de `response_id` aceitáveis sob um cenário. A unidade narrativa é um cenário ou diálogo completo. Registrar versão de dados, população alvo e hipótese antes do ensaio. Identificar consultas respondíveis, ambíguas e desconhecidas. Uma coleção incompleta de julgamentos limita o que se pode dizer sobre recall. [Manning, Raghavan e Schütze](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html)

| Medida | Definição operacional | Leitura |
|---|---|---|
| Relevância | Grau 2 para resposta apropriada, 1 para parcial e 0 para incorreta. Precisão binária usa grau 2. | Publicar distribuição, critérios, exemplos adjudicados e fração sem julgamento. |
| Precisão e recall da recuperação | Para cada consulta conhecida, `precisão = TP/(TP+FP)` e `recall = TP/(TP+FN)` sobre a lista retornada. | Usar IDs únicos, explicitar profundidade e agregação macro por consulta. Denominador zero é indefinido, reportado separadamente. |
| Precision@K e Recall@K | Acertos nos primeiros K divididos por K e pelo total de IDs relevantes da consulta, respectivamente. | Posições ausentes valem zero em P@K. Fixar K antes da comparação. Para a estimativa principal de P@K e MRR@K, completar a avaliação dos candidatos no top-K da união dos métodos. Se ainda houver itens indeterminados, identificar consultas excluídas e publicar cobertura e limites tratando cada indeterminado como irrelevante ou relevante. Recall sem julgamento exaustivo do catálogo é relativo ao conjunto julgado. |
| MRR | Média de `1/r`, sendo r a posição da primeira resposta relevante e zero quando nenhuma aparece. | Se a lista foi truncada em K, rotular MRR@K. Avaliar a ordenação antes do fallback. [NIST/TREC](https://trec.nist.gov/pubs/trec10/appendices/measures.pdf) |
| Cobertura de conhecimento | Consultas do universo alvo para as quais a curadoria identifica ao menos uma resposta adequada no repertório ÷ total revisado. | Separar da cobertura de atendimento (fração respondida) e da precisão entre respostas emitidas. |
| Identificação de desconhecidos | Usar referência `answerable`, `unknown`, `ambiguous` e colunas resposta, abstenção por desconhecimento e abstenção por ambiguidade. Medir precisão/recall da identificação de desconhecidos e taxa de respostas indevidas nessa classe. | Abster-se em `answerable` é falsa rejeição. Abster-se por ambiguidade em `ambiguous` conta como acerto da política de ambiguidade. Reportar confusões de motivo e erros técnicos separadamente. |
| Repetição e diversidade | Frequência de repetição imediata de `response_id` entre pares de turnos elegíveis. `Distinct-n` = n-gramas distintos ÷ ocorrências de n-gramas. | Declarar segmentação, n e comprimento. Comparar amostras de tamanho equivalente e verificar se a variedade mantém o sentido. |
| Coerência e personalidade | Julgamento cego por cenário com personas trocadas e fatos iguais. Escala de 0 (contradição), 1 (inconclusivo/parcial) e 2 (compatível com evidência). | Reportar separadamente coerência entre turnos e aderência aos traços. Descrever distribuição e discordância. |
| Fidelidade factual | Decompor saída em afirmações verificáveis e marcar sustentada, contradita ou sem apoio. Calcular fração por classe e cobertura dos fatos exigidos. | Saída vazia é identificada separadamente. Inferências permitidas devem citar a regra e as premissas. |
| Recursos | Latência por percentil, pico de RSS, tempo de CPU, tamanho de índice e crescimento marginal. | Usar [protocolo de medição](PERFORMANCE.md) na mesma condição de qualidade. |

**Exemplo aritmético, sem medição do motor.** Para dois IDs relevantes e lista top-3 com apenas um deles na posição 2, P@3 = 1/3, R@3 = 1/2 e RR@3 = 1/2. Uma consulta sem resposta relevante esperada entra no ensaio de desconhecidos. Incluí-la como zero no recall de consultas conhecidas mudaria a pergunta científica.

### Partição, comparação e decisão

1. Separar repertório elegível, desenvolvimento e teste por obra/edições, sessão, proveniência e família de paráfrases. Buscar duplicatas normalizadas e vizinhos próximos cruzando também o índice com consultas de teste. Reagrupar colisões antes do congelamento. Correspondência exata intencional forma um diagnóstico separado. [Contrato do benchmark](../../mimesis-knowledge/docs/BENCHMARK_DATASETS.md)
2. Comparar cada método na mesma MKB, consultas, julgamentos, K, máquina e ordem de ensaio contrabalançada. Medir agregação macro e cortes por negação, grafia, extensão, variedade e classe, com denominadores. Calibrar limiares e margem apenas em desenvolvimento, congelando também o custo relativo de aceitar um desconhecido e de rejeitar um conhecido.
3. Dois avaliadores de pt-BR julgam amostra sobreposta, cegos à estratégia e com ordem aleatória. Treinar na rubrica com exemplos de desenvolvimento, registrar desacordos antes da adjudicação e publicar acordo bruto e, se pertinente à escala, kappa ponderado. Incluir os pares de julgamento originais sob acesso adequado. [Van der Lee et al.](https://aclanthology.org/W19-8643/)
4. Comparar diferenças pareadas por consulta. Estimar intervalo de incerteza por reamostragem dos grupos independentes, mantendo as consultas da mesma família juntas. Registrar semente, número de reamostragens e regra de decisão. Poucos grupos ou resultados inconclusivos exigem nova amostra. Uma diferença global pode ocultar falha sistemática em uma variedade.
5. Antes de abrir o teste, pactuar tolerância de não inferioridade para cada métrica prioritária e tetos de recursos no notebook. Bloquear contradições em fatos obrigatórios, vazamentos e regressões dos casos de aceitação. Fronteira de incerteza que não permite concluir não inferioridade fica pendente. Preservar falhas no relatório.

### Aplicação cumulativa

| Etapa | Medidas e controles adicionais |
|---|---|
| 0.0.0 Research | Cobertura documental, prontidão dos contratos, auditabilidade e integridade das futuras partições. Métricas do motor aguardam execução. |
| 0.0.1 Genesis | Precisão/recall, P@K, R@K, MRR, cobertura, falsos aceites e rejeições, recursos do sistema completo. |
| 0.0.2 Lexicon | Cortes de paráfrase, polissemia e negação com e sem expansão. |
| 0.0.3 Persona | Aderência cega a perfis e preservação de significado ao trocar persona. |
| 0.0.4 Context | Adequação após trocar um fato, contradições e abstenção quando falta requisito. |
| 0.0.5 Mythos | Cobertura e fidelidade de fatos, legibilidade e coerência por cenário. |
| 0.0.6 Logos | Diversidade sob comprimento controlado, concordância, repetição e fidelidade por proposição. |
| 0.0.7 Mnemosyne | Recuperação do antecedente correto, contradições entre turnos e isolamento entre sessões. |
| 0.0.8 Anima | Adequação da reação a estímulos, consistência de personalidade, duração e retorno ao basal. |
| 0.0.9 Sophia | Qualidade antes/depois de incorporar sugestões aprovadas, mudanças indevidas e capacidade de reversão. |
| 0.1.0 Awakening | Todas as dimensões em diálogos multivolta, com ablação por capacidade. |
| 1.0.0 Mimesis | Repetir suite integrada em combinações suportadas e após migração, inclusive custo de armazenamento acumulado. |
