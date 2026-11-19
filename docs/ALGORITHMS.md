# Catálogo de técnicas

As 23 fichas descrevem o que cada técnica calcula, em quais condições seu custo é viável e que observação justificaria usá-la. A versão indicada é uma **proposta de investigação**. Genesis tem três candidatos obrigatórios à comparação. A adoção de qualquer vencedor depende dos ensaios. A [bibliografia comentada](REFERENCES.md) identifica as fontes e os limites de cada atribuição.

| Família | Técnicas |
|---|---|
| Recuperação lexical | [Exact Matching](#exact-matching) · [Pattern Matching](#pattern-matching) · [Fuzzy Matching](#fuzzy-matching) · [Levenshtein Distance](#levenshtein-distance) · [BM25](#bm25) · [TF-IDF](#tf-idf) · [Cosine Similarity](#cosine-similarity) · [N-grams](#n-grams) |
| Decisão e inferência | [Weighted Ranking](#weighted-ranking) · [Weighted Random Selection](#weighted-random-selection) · [Decision Trees](#decision-trees) · [Finite State Machines](#finite-state-machines) · [Bayesian Inference](#bayesian-inference) · [Knowledge Graphs](#knowledge-graphs) |
| Controle e experiência | [Utility AI](#utility-ai) · [Behavior Trees](#behavior-trees) · [GOAP](#goap) · [Case-Based Reasoning](#case-based-reasoning) |
| Composição e representação | [Formal Grammars](#formal-grammars) · [Markov Chains](#markov-chains) · [Procedural Text Generation](#procedural-text-generation) · [Semantic Search](#semantic-search) · [Vector Embeddings](#vector-embeddings) |

Uma consulta pode ter **semelhança lexical** com “o portão está aberto?” e sentido oposto em “o portão está fechado?”. **Similaridade semântica** considera sentidos e relações. **Intenção** é um rótulo operacional para o que se pede, por exemplo confirmar um estado. **Inferência** combina premissas para sustentar uma conclusão, com justificativa e escopo de validade. **Composição** realiza em texto um conteúdo autorizado. O acerto em uma tarefa não mede automaticamente o acerto nas demais.

Nas estimativas abaixo, N é o número de entradas indexadas, C o de candidatos considerados, K o limite pedido, m e n são comprimentos em unidades declaradas, D é a dimensão de um vetor. Cada ficha explicita suas hipóteses adicionais. Custos são estimativas assintóticas, sem medições neste projeto. O experimento deve distinguir construção do índice, consulta e memória residente. Critérios comuns, partições e medidas estão em [Avaliação](EVALUATION.md) e [Desempenho](PERFORMANCE.md).

## Recuperação lexical

### Exact Matching

- **Conceito e matemática.** Igualdade de chaves normalizadas. A pontuação é 1 se as sequências coincidem, 0 no restante. Uma política de normalização define quais grafias recebem a mesma chave. NFC resolve equivalências canônicas sem eliminar a oposição entre “pode” e “pôde”. [Unicode UAX #15](https://www.unicode.org/reports/tr15/)
- **Operação, entrada e saída.** Recebe a consulta, aplica o mesmo perfil usado nas entradas do índice e procura a chave inteira. Devolve todos os identificadores de Talksets elegíveis sob a chave, inclusive os empates.
- **Aplicação e dependências.** Linha de base para frases curadas, saudações e variantes atestadas. Exige versão do normalizador, índice de igualdade e política explícita para chaves vazias e colisões.
- **Custo.** Com B-tree, busca em O(log N) comparações de chave mais a leitura dos C resultados e o custo de normalizar a consulta. Em entradas com prefixos longos, uma comparação de chave custa até O(m+n).
- **Limitações e alternativas.** Debaixo de grafia inédita, a resposta relevante pode desaparecer. Colapsar acentos ou eliminar negação confunde perguntas distintas. Alternativas são aliases curados e busca fuzzy.
- **Avaliação e versão.** Genesis 0.0.1. Medir candidatos corretos no topo, cobertura, colisões entre respostas incompatíveis e acerto da abstenção em chaves ausentes. Repetir com Unicode composto e decomposto e com mudança real de acento.

### Pattern Matching

- **Conceito e matemática.** Um padrão p define uma linguagem L(p). A condição de ativação é a pertinência da entrada a L(p). Um autômato finito pode reconhecer um subconjunto regular. [Documentação do RE2](https://github.com/google/re2)
- **Operação, entrada e saída.** Um curador publica um padrão ancorado e os campos permitidos. A aplicação sobre uma sequência de símbolos devolve identificador da regra e capturas com posição. Padrões sobre fatos estruturados podem aplicar predicados de igualdade em vez de texto.
- **Aplicação e dependências.** Reconhecer uma construção restrita, como um pedido de reformulação, ou uma condição contextual. Precisa de catálogo versionado, convenção de fronteiras de palavra, idioma e precedência para sobreposições.
- **Custo.** Para R padrões regulares fixos com execução linear no comprimento, varredura independente O(Rm), com constantes dependentes dos padrões. Motores com busca retroativa podem ter comportamento muito pior. Medir compilação à parte.
- **Limitações e alternativas.** Uma regra abrangente demais captura contextos impróprios. Alternativas são chave exata, léxico e classificador supervisionado. Um padrão escrito para uma construção histórica requer revisão antes de ser reutilizado em pt-BR contemporâneo.
- **Avaliação e versão.** Context 0.0.4. Medir precisão por regra, conflitos entre regras, custo de execução e cobertura incremental sobre a recuperação pura. Examinar frases semelhantes com escopo sintático diferente.

### Fuzzy Matching

- **Conceito e matemática.** Família de comparadores aproximados de grafia. Uma candidata é a similaridade normalizada de Levenshtein s = 1 − d/max(m,n), com limites e tratamento de cadeia vazia explícitos. Por sua vez, fuzz.ratio do RapidFuzz emprega Indel normalizada. Os dois comparadores têm semânticas diferentes. [Manual do RapidFuzz](https://rapidfuzz.github.io/RapidFuzz/Usage/fuzz.html)
- **Operação, entrada e saída.** Compara a pergunta normalizada às entradas, ordena por escore decrescente, preserva identificadores e o nome do comparador. Uma regra calibrada pode rejeitar o melhor candidato.
- **Aplicação e dependências.** Recuperar pequenas variações, acentos e erros de digitação. Exige política de caracteres e normalização, comparador fixo, limite de custo e biblioteca local opcional.
- **Custo.** Com distância por programação dinâmica, C comparações entre cadeias de comprimentos até m e n custam O(Cmn) no método direto. Pré-selecionar candidatos reduz C, mas pode perder o item correto. Ranquear com heap limitado custa O(C log(K+1)).
- **Limitações e alternativas.** “É” e “era” mostram a fragilidade de consultas curtas. Um erro em nome próprio, quantidade ou negação pode alterar o sentido. Alternativas incluem igualdade, n-gramas e BM25.
- **Avaliação e versão.** Genesis 0.0.1, em braço independente. Comparar acerto em erros ortográficos, falsos aceites em pares de alto risco semântico, MRR e custo por tamanho de repertório. Ajustar o limiar apenas na partição de desenvolvimento.

### Levenshtein Distance

- **Conceito e matemática.** d(i,0)=i e d(0,j)=j. Para i,j positivos, d(i,j) é o mínimo entre d(i−1,j)+1, d(i,j−1)+1 e d(i−1,j−1)+[xᵢ≠yⱼ]. Cada inserção, remoção ou substituição custa uma unidade. [Manning, Raghavan e Schütze, cap. 3](https://www.cambridge.org/highereducation/books/introduction-to-information-retrieval/669D108D20F556C5C30957D63B5AB65C)
- **Operação, entrada e saída.** Preenche mínimos sobre prefixos de duas sequências. Devolve uma distância inteira. Reconstruir inserções e remoções requer manter ou recomputar informação sobre o caminho.
- **Aplicação e dependências.** Comparador candidato dentro do braço fuzzy. “casa” e “caso” distam uma substituição. Declarar se a unidade é ponto de código ou grafema e se há normalização prévia.
- **Custo.** O(mn) tempo e O(min(m,n)) memória para a distância com duas linhas. Uma matriz completa para retroceder no caminho usa O(mn) memória. Limites por banda só mantêm equivalência dentro das condições estabelecidas.
- **Limitações e alternativas.** Troca de letras adjacentes pode custar duas edições. A distância cresce com comprimento e desconhece significado. Alternativas são Damerau–Levenshtein, Indel ou Jaccard de n-gramas.
- **Avaliação e versão.** Genesis 0.0.1, sem constituir um quarto método no ensaio obrigatório. Conferir identidade, simetria, diferença de comprimentos, acentos e custo em grafias longas. Comparar versões otimizadas à definição sobre um conjunto pequeno com distâncias conhecidas.

### BM25

- **Conceito e matemática.** Para consulta em termos simples, a contribuição de t combina a raridade IDF(t) com f(t,d)(k₁+1) / [f(t,d)+k₁(1−b+b·len(d)/avglen)]. Somam-se as contribuições. O crescimento com frequência satura e o comprimento é corrigido em relação à coleção. [Robertson e Zaragoza](https://doi.org/10.1561/1500000019)
- **Operação, entrada e saída.** Cada entrada do Talkset torna-se unidade de recuperação. A consulta encontra entradas nas listas invertidas dos termos. O ranking devolve os identificadores e o escore bruto. A função bm25() do SQLite FTS5 dá o **menor** valor à melhor correspondência, com k₁=1,2 e b=0,75 fixos nessa implementação. Registrar a direção evita inverter o ranking. [Manual FTS5, §5.1.1](https://www.sqlite.org/fts5.html)
- **Aplicação e dependências.** Favorecer expressões informativas em perguntas com várias palavras. Exige FTS5 local para esta variante, snapshot estável, estatísticas da coleção e convenção sobre termos, frases e diacríticos. Valores de implementações distintas podem ter escalas distintas.
- **Custo.** Depende das listas percorridas. Com P ocorrências visitadas e seleção em heap, um modelo de trabalho é O(P+C log(K+1)), fora leitura e tokenização. Uma ordenação completa pode custar O(C log C). Termos muito frequentes e índices frios elevam a latência.
- **Limitações e alternativas.** Relevância estimada por frequência deixa de fora paráfrases sem vocabulário comum. Frases curtas empatam com facilidade. Scores variam com a coleção. Alternativas são TF-IDF/cosseno e expansão por léxico curado.
- **Avaliação e versão.** Genesis 0.0.1, em braço independente. Comparar P@K, MRR e identificação de desconhecidos, com consultas curtas, longas e termos comuns. Verificar ordenação, empates, token ausente e comportamento em mudança de release da MKB.

### TF-IDF

- **Conceito e matemática.** Um peso possível é w(t,d)=tf(t,d)·log(N/df(t)). O termo df conta documentos da coleção que contêm t. Existem formas logarítmicas de tf, versões suavizadas de idf e normalizações vetoriais que alteram o resultado. [Guia de extração de atributos](https://scikit-learn.org/stable/modules/feature_extraction.html)
- **Operação, entrada e saída.** Ajustar vocabulário e idf apenas no acervo indexado permitido para o ensaio. Aplicar a mesma transformação a documento e consulta produz vetores esparsos com pesos por termo.
- **Aplicação e dependências.** Controle lexical para experimentos semânticos. Exige tokenizador em português, vocabulário congelado e regra para termos inéditos.
- **Custo.** Com T ocorrências de termos e S pares distintos termo-documento, uma construção simples custa O(T) operações esperadas em mapas e O(S) espaço para a matriz. Uma nova consulta custa O(m) para contagem, além do ranqueamento.
- **Limitações e alternativas.** Representação por palavras perde ordem, negação e sentidos. Ajustar idf com enunciados de teste vaza informação. Alternativas incluem BM25, pesos binários e n-gramas de caracteres.
- **Avaliação e versão.** Lexicon 0.0.2 como controle. Variar um fator de cada vez entre TF bruto, TF log e suavização. Reportar MRR, proporção de consultas sem atributos conhecidos e tamanho da matriz.

### Cosine Similarity

- **Conceito e matemática.** cos(x,y)=(x·y)/(‖x‖₂‖y‖₂) para vetores com norma positiva. O valor em vetores reais pode ir de −1 a 1. Em TF-IDF com pesos não negativos fica entre 0 e 1. [Definição do scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html)
- **Operação, entrada e saída.** Recebe dois vetores no mesmo espaço. Prediz afinidade angular e permite ordenar candidatos. Para norma zero, a proposta é marcar falta de evidência e abster-se quando apropriado.
- **Aplicação e dependências.** Comparar TF-IDF e, em ensaio distinto, vetores latentes. Exige mesma versão do vocabulário ou do modelo, mesma dimensão e convenção de normalização.
- **Custo.** O(D) por par denso. Com índices esparsos ordenados, a interseção por dois cursores custa O(nnz(x)+nnz(y)), em que nnz conta elementos armazenados. Pré-calcular normas reduz trabalho por consulta.
- **Limitações e alternativas.** A qualidade acompanha a representação. Cosseno alto também ocorre entre frases contraditórias. Alternativas são produto interno com norma controlada, Jaccard e BM25.
- **Avaliação e versão.** Lexicon 0.0.2. Testar vetores colineares, ortogonais e vazios e distinguir acerto em sinônimos de erro em antônimos. Incluir latência sobre vetores esparsos e densos separadamente.

### N-grams

- **Conceito e matemática.** Fragmentos contíguos de ordem g de uma sequência com m unidades produzem max(0,m−g+1) janelas sem marcadores de borda. A sobreposição entre conjuntos A e B pode usar J=|A∩B|/|A∪B|, com regra para união vazia. [Guia de atributos de texto](https://scikit-learn.org/stable/modules/feature_extraction.html)
- **Operação, entrada e saída.** Segmentar caracteres ou palavras, deslizar uma janela e emitir contagens ou postings. A saída pode alimentar pré-seleção fuzzy ou um modelo vetorial. “sala” produz os trigramas “sal” e “ala”.
- **Aplicação e dependências.** Resgatar grafias próximas ou preservar pequena ordem local. Definir fronteiras, acentos, unidade e tratamento de palavras curtas.
- **Custo.** O(m) janelas para uma ordem fixa. Se cada janela é copiada, O(mg) trabalho e espaço de materialização no pior caso. O tamanho das listas do índice cresce com o número de pares distintos entre um n-grama e uma entrada.
- **Limitações e alternativas.** N-gramas pequenos colidem em palavras diferentes. Grandes ordens são esparsas. Alternativas são distância de edição direta, aliases ou termos no índice invertido.
- **Avaliação e versão.** Lexicon 0.0.2 como controle lexical de generalização. Medir recall do conjunto de candidatos antes do ranking, precisão por comprimento de consulta, crescimento do índice e colisões por ordem escolhida.

## Decisão e inferência

### Weighted Ranking

- **Conceito e matemática.** Computar S(c)=Σⱼwⱼfⱼ(c) para sinais orientados na mesma direção e escalas documentadas. Requisitos obrigatórios de elegibilidade restringem previamente o conjunto. A pontuação é uma preferência, sem interpretação probabilística automática.
- **Operação, entrada e saída.** Recebe candidatos elegíveis, atributos e pesos versionados. Produz ordem, decomposição por sinal, regra de desempate e versão da política. Um sinal ausente requer um tratamento distinto do valor zero observado.
- **Aplicação e dependências.** Incorporar compatibilidade de persona e pertinência de contexto a uma relevância lexical já medida. Precisa de dados de desenvolvimento para calibrar pesos, transformações e decisão de abstenção.
- **Custo.** O(CF) para F sinais já extraídos, mais O(C log C) para ordenação completa. Se calcular um sinal exigir consulta a um grafo, somar esse custo.
- **Limitações e alternativas.** Escalas incompatíveis distorcem o efeito dos pesos. Sinais correlacionados contam duas vezes o mesmo indício. Alternativas são precedência lexicográfica, uma regra explícita e classificação supervisionada.
- **Avaliação e versão.** Persona 0.0.3 para um sinal de perfil, Context 0.0.4 para fusão contextual. Comparar o ranking completo a cada ablação e verificar o desempate. Registrar inversões de pares ao variar um peso. Genesis deve reportar seus três braços isoladamente.

### Weighted Random Selection

- **Conceito e matemática.** Para pesos finitos não negativos e soma positiva, P(i)=wᵢ/Σⱼwⱼ. Uma variável uniforme seleciona um intervalo da soma acumulada. [Documentação do Python](https://docs.python.org/3/library/random.html)
- **Operação, entrada e saída.** Recebe alternativas igualmente admissíveis quanto aos fatos, pesos, ordem estável e gerador pseudoaleatório. Devolve uma escolha, seu peso e os dados de reprodução. Soma zero resulta em fallback determinístico explícito.
- **Aplicação e dependências.** Alternar realizações de uma mesma proposição. Exige equivalência factual anotada, política, semente e versões do gerador e do procedimento de amostragem.
- **Custo.** O(C) para construir acumulados e O(log C) por sorteio binário subsequente, com O(C) espaço. Uma passada para uma única escolha também custa O(C).
- **Limitações e alternativas.** Sorteios consecutivos podem repetir. Evitar repetição muda a distribuição e precisa de política própria. Alternativas são escolha determinística ou rodízio registrado.
- **Avaliação e versão.** Logos 0.0.6. Conferir reprodução com configuração idêntica, pesos nulos e distribuição empírica em muitas sementes pré-fixadas. Medir taxa de repetição e verificar fidelidade factual em todas as variantes.

### Decision Trees

- **Conceito e matemática.** Cada nó particiona exemplos por um atributo. Um critério é a redução de impureza I(pai)−Σᵢ(nᵢ/n)I(filhoᵢ), com entropia ou Gini. As folhas contêm a decisão ou frequências de classe. [Quinlan, 1986](https://mlanthology.org/mlj/1986/quinlan1986mlj-induction/) · [Guia do scikit-learn](https://scikit-learn.org/stable/modules/tree.html)
- **Operação, entrada e saída.** Aprender divisões em exemplos revisados com rótulos. Aplicar a uma consulta estruturada e devolver classe proposta e caminho de testes. Casos sem suporte podem pedir esclarecimento.
- **Aplicação e dependências.** Classificar intenções ou recomendar revisão de exemplos em Sophia. Precisa de taxonomia estável, matriz de atributos, rótulos auditados e política de profundidade.
- **Custo.** Predição O(h) por exemplo para profundidade h e testes constantes. Treino depende de pontos de corte e implementação. Para F atributos, A exemplos e ordenação inicial por atributo, o preparo pode custar O(FA log A) antes da busca de divisões.
- **Limitações e alternativas.** Árvores profundas memorizam grupos raros e pequenas mudanças podem alterar as primeiras divisões. Alternativas são tabela de regras, Naive Bayes e classe majoritária como controle.
- **Avaliação e versão.** Sophia 0.0.9. Medir macro-F1, matriz de confusão, profundidade, tamanho das folhas e generalização por origem das frases. Revisar caminhos que se apoiem em pistas editoriais alheias à intenção.

### Finite State Machines

- **Conceito e matemática.** Uma máquina mantém estado s em conjunto finito S e uma transição δ(s,e) dada uma observação e. Uma função de saída associa uma ação discursiva ao estado ou à transição.
- **Operação, entrada e saída.** Recebe estado da conversa e evento autorizado, consulta a transição, emite próximo estado interno e ação de diálogo. Exemplo proposto é “aguardando esclarecimento” seguido de uma resposta do interlocutor.
- **Aplicação e dependências.** Controlar sequência de turnos e tratamento de eventos imprevistos. Exige estados nomeados, política para evento ausente e identificador de sessão quando persistido.
- **Custo.** O(1) por transição indexada por (estado,evento) em tabela direta. Uma tabela densa usa O(|S|·|E|) células. Guardas ordenadas acrescentam o custo de avaliá-las.
- **Limitações e alternativas.** Cruzar tema, humor e fase do diálogo em um único estado provoca explosão combinatória. Alternativas são regras de contexto e árvore de comportamento, mantendo fatos ortogonais em campos separados.
- **Avaliação e versão.** Context 0.0.4 para estado fornecido na requisição. Mnemosyne 0.0.7 para continuidade conversacional sob política de memória. Medir cobertura de transições, estados inalcançáveis, recuperação de eventos inválidos e isolamento entre conversas.

### Bayesian Inference

- **Conceito e matemática.** Para hipóteses mutuamente exclusivas e exaustivas com P(e)>0, P(h|e)=P(e|h)P(h)/ΣⱼP(e|hⱼ)P(hⱼ). Naive Bayes fatora as verossimilhanças por atributo sob independência condicional dada a hipótese. [Guia de Naive Bayes](https://scikit-learn.org/stable/modules/naive_bayes.html)
- **Operação, entrada e saída.** Recebe hipóteses de intenção, evidências tipadas e parâmetros estimados. Atualiza a distribuição e registra os termos da atualização. Evidência ausente ou incompatível pede política explícita.
- **Aplicação e dependências.** Estudar reconhecimento de ambiguidade e valor de uma pergunta de esclarecimento. Exige classes rotuladas, probabilidades condicionais, suavização, avaliação de calibração e tratamento de classe desconhecida.
- **Custo.** Para H hipóteses e F atributos sob o modelo ingênuo, O(HF) por exemplo. A inferência em uma rede bayesiana geral pode crescer exponencialmente com sua largura de árvore.
- **Limitações e alternativas.** Repetir evidência correlacionada produz excesso de confiança. Mudanças nas frequências de intenção invalidam priors. Alternativas são árvore supervisionada e abstenção por margem calibrada.
- **Avaliação e versão.** Sophia 0.0.9, em laboratório. Medir Brier score, curva de confiabilidade, macro-F1 e erros em frases ambíguas. O desempenho será comparado a uma política por frequência. O funcionamento interno do Akinator não é premissa deste ensaio.

### Knowledge Graphs

- **Conceito e matemática.** Um grafo dirigido rotulado G=(V,E) registra arestas da forma (origem,relação,destino). Sentidos diferentes podem designar nós diferentes. Uma aresta deve admitir procedência e escopo. [W3C, RDF 1.1](https://www.w3.org/TR/rdf-concepts/) · [OpenWordNet-PT](https://aclanthology.org/C12-3044/)
- **Operação, entrada e saída.** A partir de sentidos candidatos ou entidades fornecidas, percorrer relações permitidas com direção e profundidade limitadas. Devolver caminhos com suas fontes. Herança e composição de relações precisam de regra explícita para autorizar uma inferência.
- **Aplicação e dependências.** Expansão lexical por sinônimos, desambiguação e explicação por caminho. Exige identificadores de sentidos, semântica de cada relação e política de fatos contraditórios.
- **Custo.** Uma busca em largura na região atingida custa O(Vᵣ+Eᵣ) e usa O(Vᵣ) memória de visita. Enumerar todos os caminhos possíveis pode custar muito mais. Índices por relação e profundidade limitada restringem a região.
- **Limitações e alternativas.** Lacunas, polissemia e composição indevida geram expansões erradas. Alternativas são tabelas de aliases revisadas e filtros de domínio em índice textual.
- **Avaliação e versão.** Lexicon 0.0.2. Medir precisão da expansão por sentido, cobertura de termos, MRR e fração de respostas cuja justificativa contém cada relação usada. Incluir nós homógrafos, ciclos e relações sem procedência.

## Controle e experiência

### Utility AI

- **Conceito e matemática.** Uma função U(a,s) atribui utilidade a um ato a em situação s. Um modelo simples soma curvas de resposta gⱼ aplicadas a atributos, U=Σⱼwⱼgⱼ(s,a). O conjunto de atos admissíveis é definido antes da maximização. [Mark e Dill, GDC](https://www.gdcvault.com/play/1012410/Improving-AI-Decision-Modeling-Through2d)
- **Operação, entrada e saída.** Recebe fatos autorizados, predisposições da persona e atos possíveis, como descrever ou pedir confirmação. Calcula utilidades e retorna o ato, os sinais determinantes e as exclusões por condição obrigatória.
- **Aplicação e dependências.** Escolher um comportamento discursivo ou uma reação expressiva. Distingue-se do ranking de frases pelo objeto da decisão. Exige curvas interpretáveis, pesos, limites e semântica dos atributos.
- **Custo.** O(AF) para A atos e F fatores com curvas de custo constante. Consultas externas a essa conta devem entrar no orçamento da etapa de obtenção de atributos.
- **Limitações e alternativas.** Curvas mal escalonadas dominam a escolha. Pequenas variações em estados próximos podem alternar a ação repetidamente. Alternativas são tabela de prioridades, FSM e ramo explícito de abstenção.
- **Avaliação e versão.** Context 0.0.4 para decisões de fala e Anima 0.0.8 para reações. Avaliar concordância com julgamentos humanos, estabilidade a perturbações e deriva da persona. Auditar pares nos quais desempates alteram a reação.

### Behavior Trees

- **Conceito e matemática.** Uma árvore combina condições e ações em nós de sequência ou seleção. A cada passo, um nó retorna sucesso, falha ou execução em curso. A composição define o fluxo lógico. [Colledanchise e Ögren](https://arxiv.org/abs/1709.00084)
- **Operação, entrada e saída.** O controlador consulta condições de contexto e visita filhos conforme as regras de propagação. Devolve estado de execução, ato discursivo e sequência de nós visitados. Uma folha pode sugerir “pedir o referente” antes de tentar descrever uma entidade.
- **Aplicação e dependências.** Coordenar alternativas quando atos exigem precondições distintas. Precisa de catálogo de folhas, memória de execução quando aplicável, limites de passos e semântica de reinício.
- **Custo.** Em uma travessia sem repetidores, O(B) visitas no pior caso para B nós. O custo real soma o trabalho das folhas. Com repetição ou tarefas persistentes, o total entre passos precisa de limite separado.
- **Limitações e alternativas.** Ordem dos ramos embute preferências. Folhas com efeitos colaterais dificultam reprodução. Alternativas são FSM para trajetos curtos e regras com prioridade explícita.
- **Avaliação e versão.** Anima 0.0.8, comparada a uma tabela simples. Medir ramos cobertos, passos até a escolha, casos de interrupção e coerência de reações. Inverter um ramo deve produzir uma mudança explicável nos casos pertinentes.

### GOAP

- **Conceito e matemática.** Goal-Oriented Action Planning descreve um estado inicial, um objetivo e ações com precondições, efeitos e custo. Um plano é uma sequência aplicável que satisfaz o objetivo. Pode-se buscar custo mínimo quando as hipóteses do algoritmo de busca permitem. [Orkin, GDC](https://gdcvault.com/play/1013459/Three-States-and-a-Plan)
- **Operação, entrada e saída.** Tratar apenas estados do discurso. Por exemplo, estabelecer o referente para depois descrever um atributo informado. Retornar sequência de atos, premissas, custo e motivo de parada por impossibilidade ou orçamento.
- **Aplicação e dependências.** Investigar encadeamento narrativo quando regras fixas perdem cobertura. Exige representação finita, objetivo observável, efeitos discursivos, custos não negativos e orçamento de expansão.
- **Custo.** Busca ingênua a profundidade d com fator de ramificação b pode visitar O(bᵈ) sequências e consumir memória da mesma ordem em largura. Heurísticas reduzem trabalho em certos casos, sem garantir ganho geral.
- **Limitações e alternativas.** Busca pode consumir o orçamento antes de achar plano. Precondições incompletas validam planos absurdos. Nenhuma transição interna autoriza alterar o estado de um sistema externo. Alternativas são FSM e roteiros de atos curados.
- **Avaliação e versão.** Awakening 0.1.0, exclusivamente como investigação opcional. Medir taxa de planos válidos, expansões, tempo, fidelidade aos fatos e comportamento sem solução. Adotar apenas com benefício sobre sequência escrita à mão.

### Case-Based Reasoning

- **Conceito e matemática.** O ciclo conhecido como 4R abrange recuperar, reutilizar, revisar e reter casos. Um caso descreve situação, decisão e resultado validado. A semelhança com um caso antigo é uma hipótese de utilidade da solução. [Aamodt e Plaza](https://www.iiia.csic.es/~enric/papers/Aamodt_1994_Case.pdf)
- **Operação, entrada e saída.** Recuperar um caso por atributos, confrontar diferenças, propor adaptação e submeter à revisão. O resultado pode ser um ato sugerido com identificador do precedente e condições de adaptação. Reter um caso exige aprovação e nova distribuição do conhecimento.
- **Aplicação e dependências.** Reutilizar resolução curada de ambiguidade conversacional. Exige histórico autorizado com origem, consentimento aplicável, solução revisada e mecanismo de descarte de casos incorretos.
- **Custo.** Varredura de N casos com F atributos simples custa O(NF) antes da adaptação. Um índice pode reduzir a busca. O custo da revisão humana e da adaptação deve ser contabilizado à parte.
- **Limitações e alternativas.** Semelhança de superfície transfere decisões para situações incompatíveis. Reforço automático de um erro contamina casos futuros. Alternativas são recuperação convencional de Talksets e regras gerais.
- **Avaliação e versão.** Sophia 0.0.9. Separar famílias de casos entre treino e teste. Medir adequação da adaptação, proporção rejeitada por revisores, perda por retirada do precedente e rastreabilidade até o caso autorizado.

## Composição e representação

### Formal Grammars

- **Conceito e matemática.** Uma gramática livre de contexto pode ser escrita G=(V,Σ,P,S), com não terminais, terminais, produções e símbolo inicial. Aplicações sucessivas de produções derivam uma cadeia. [Chomsky, 1956](https://experts.arizona.edu/en/publications/three-models-for-the-description-of-language/)
- **Operação, entrada e saída.** Receber uma estrutura de conteúdo autorizada e recursos linguísticos. Expandir categorias e verificar traços de concordância. Devolver a frase e sua árvore de derivação ou indicar que nenhuma realização satisfaz as condições.
- **Aplicação e dependências.** Realizar descrições com gênero, número e contrações de pt-BR. Exige gramática revisada, léxico flexionado e estratégia para produção sem alternativa válida.
- **Custo.** Com uma derivação já escolhida e produções limitadas, custo proporcional ao número de símbolos visitados e ao texto emitido. Explorar todas as derivações ambíguas pode crescer exponencialmente com a profundidade, e recursão sem condição pode impedir término.
- **Limitações e alternativas.** Gramática sintaticamente correta ainda pode produzir contradição factual. Traços adicionais ampliam a manutenção. Alternativas são templates com slots tipados e frases completas curadas.
- **Avaliação e versão.** Logos 0.0.6. Testar concordância, terminações em todas as categorias, cobertura de entradas e preservação de negação e quantificação. Registrar regras responsáveis por cada desvio.

### Markov Chains

- **Conceito e matemática.** Uma cadeia de ordem r aproxima P(xₜ|x₁…xₜ₋₁) por P(xₜ|xₜ₋ᵣ…xₜ₋₁). Uma estimativa por contagem normaliza, para cada contexto, as frequências dos próximos símbolos. [Shannon, 1948](https://web.mit.edu/6.441/spring05/reading/shannon1948.pdf)
- **Operação, entrada e saída.** A partir de texto autorizado, construir contagens de transição e depois amostrar a partir de um prefixo. Registrar tuplas de contexto, política para sequência inédita, semente e limite de comprimento.
- **Aplicação e dependências.** Linha de base de variação local em laboratório. Precisa de partição de treinamento com direitos adequados, símbolos de início/fim e política de parada. A memória conversacional do produto tem outro contrato.
- **Custo.** Com r fixo e mapas, O(T) inserções esperadas para T tokens. Memória proporcional ao número de transições observadas. Com distribuições acumuladas, uma amostra por token custa O(log A) para A sucessores possíveis.
- **Limitações e alternativas.** Perde dependências longas e pode repetir passagens da fonte ou inventar fatos. Elevar r aumenta esparsidade e reprodução literal. Alternativas são gramática e templates ancorados nos fatos.
- **Avaliação e versão.** Logos 0.0.6, isolada da geração operacional. Medir diversidade, maior trecho copiado, taxa de contradição e avaliação humana fora do treino. Perplexidade, se usada, só admite comparação com tokenização e conjunto iguais.

### Procedural Text Generation

- **Conceito e matemática.** Uma função de realização R(plano,léxico,contexto,escolhas) produz texto. Separar seleção de conteúdo, ordenação e realização permite testar fidelidade em cada passo. [Compton, Kybartas e Mateas, 2015](https://www.galaxykate.com/pdfs/ComptonKybartasMateas15-Tracery%20An%20Author-Focused%20Generative%20Text%20Tool.pdf)
- **Operação, entrada e saída.** Extrair proposições autorizadas, escolher um esquema compatível, preencher slots tipados e flexionar. Devolver texto e vínculo entre segmentos, fatos e regra de composição. Ausência de um slot exige variante autorizada mais simples ou abstenção.
- **Aplicação e dependências.** Descrever um ambiente fornecido, encadear frases e adaptar registro. Precisa de schemas de fatos, referências de entidade, léxico e templates revisados. Um renderizador como Jinja2 seria detalhe substituível.
- **Custo.** Para um template escolhido e percorrido uma vez, O(B+L) para B nós de composição e L caracteres emitidos, sob acesso constante aos slots. Escolher entre muitos planos adiciona o custo da busca.
- **Limitações e alternativas.** Frases individualmente corretas podem repetir informação ou ter referência ambígua. Um adjetivo acrescentado sem apoio já pode alterar os fatos. Alternativas são frases prontas, gramáticas formais e concatenação de controle.
- **Avaliação e versão.** Mythos 0.0.5 para descrição restrita e Logos 0.0.6 para composição. Contar proposições suportadas, ausentes e contraditas. Avaliadores cegos julgam fluência, referência e repetição com entradas idênticas.

### Semantic Search

- **Conceito e matemática.** Recuperar entradas por proximidade de sentido. Uma realização simbólica expande um sentido q por relações autorizadas com peso a(q,t) e calcula Σₜa(q,t)·relevância(t,d). O peso é uma hipótese explícita de utilidade da relação. [OpenWordNet-PT](https://aclanthology.org/C12-3044/)
- **Operação, entrada e saída.** Identificar sentidos possíveis, restringir idioma e domínio, expandir relações permitidas e pontuar documentos. Em caso de ambiguidade, devolver caminhos alternativos ou abster-se. Outra realização possível consulta vetores semânticos.
- **Aplicação e dependências.** Investigar paráfrases com pouca sobreposição lexical, por exemplo “encerrar a conversa” e “terminar o diálogo”. Exige léxico por sentido, procedência das relações e juízos humanos que distingam equivalência de mera associação.
- **Custo.** Para U expansões escolhidas, soma do custo de obtê-las e das listas de ocorrências percorridas, mais o ranking dos C candidatos. Um limite em U e na profundidade permite quantificar perdas de cobertura.
- **Limitações e alternativas.** “Banco” pode denotar assento ou instituição. Uma expansão ampla aceita antônimos relacionados ao mesmo tema. Alternativas são BM25 sem expansão, aliases escritos por curador e representação latente.
- **Avaliação e versão.** Lexicon 0.0.2, com braço simbólico offline como proposta inicial. Medir MRR e recall em paráfrases sem termos comuns, precisão por sentido e taxa de falsos aceites em contradições, comparando com Genesis congelado.

### Vector Embeddings

- **Conceito e matemática.** Uma transformação f(x)∈ℝᴰ situa entradas em um espaço com uma métrica definida. Uma alternativa clássica é a aproximação de baixa dimensão X≈UₖΣₖVₖᵀ por SVD da matriz termo-documento. Outra usa um codificador treinado de sentenças. [Deerwester et al., 1990](https://www.microsoft.com/en-us/research/publication/indexing-by-latent-semantic-analysis/) · [Reimers e Gurevych, 2019](https://aclanthology.org/D19-1410/)
- **Operação, entrada e saída.** Projetar consultas e entradas com o mesmo vocabulário e projeção ou o mesmo codificador. Devolver vetores e vizinhos por cosseno ou distância definida. FAISS pode indexar vetores já obtidos. [Documentação do Faiss](https://faiss.ai/index.html)
- **Aplicação e dependências.** Ensaio complementar para paráfrases difíceis. A versão clássica exige corpus autorizado e projeção reproduzível. Uma versão neural exige pesos e tokenizador identificados, direitos verificados, idioma adequado e execução local em CPU. Essa variante é opcional.
- **Custo.** Armazenar N vetores densos custa O(ND), cerca de 4ND bytes só para os valores em float32. Busca exata custa O(ND) por consulta, além da codificação. Aproximação troca memória, tempo de construção e recall. O custo de codificar varia com o modelo e o comprimento.
- **Limitações e alternativas.** Vizinhança vetorial é difícil de justificar e pode aproximar frases com fatos opostos. Mudanças no modelo exigem reindexação. Alternativas são expansão simbólica e TF-IDF/cosseno. Predições densas exigem evidência textual ou conceitual complementar para auditoria.
- **Avaliação e versão.** Projeção clássica em Lexicon 0.0.2 como opção de laboratório. Codificadores neurais e FAISS podem ser investigados em Awakening 0.1.0 se o braço simbólico deixar uma lacuna demonstrada. Comparar com busca exata, recall dos vizinhos, pertinência humana em pt-BR, custo total em CPU e reprodução sem rede. A instalação básica deve continuar utilizável sem esse ensaio.

## Como interpretar uma comparação

Uma unidade de teste associa uma consulta a zero, uma ou várias respostas admissíveis. A ordenação dos itens e a decisão de responder são avaliadas separadamente. Para a mesma consulta, um escore de edição 0,88 e um valor negativo de BM25 pertencem a escalas diferentes. Uma comparação válida examina a posição da resposta aceita e o erro da política de abstenção de cada método. Estimar uma escala comum é um experimento posterior, com parâmetros aprendidos em desenvolvimento.

No caso autoral “quem fechou a porta?”, a presença de um Talkset sobre portas pode levar o ranking lexical a um item temático. A decisão final ainda precisa de uma entrada que realmente responda à pergunta e de fatos suficientes para sustentar o enunciado. Em Genesis, um repertório sem alternativa apropriada deve permitir fallback. Em uma etapa posterior, pedir esclarecimento ou usar um fato externo depende do contrato da versão.

[Índice](INDEX.md) · [Agenda e protocolos](RESEARCH.md) · [Avaliação](EVALUATION.md) · [Especificação de Genesis](releases/0.0.1-GENESIS.md) · [Referências](REFERENCES.md)
