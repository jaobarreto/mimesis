# Referências comentadas

Esta bibliografia permite verificar afirmações específicas da [agenda científica](RESEARCH.md) e do [catálogo de técnicas](ALGORITHMS.md). Os artigos descrevem experimentos de seus autores, em seus idiomas e domínios. A aplicabilidade em pt-BR continua em avaliação. Consultar uma publicação, obter o código de um projeto e redistribuir um corpus são operações com direitos distintos. O registro de fontes de dados e a análise por edição ou distribuição pertencem ao repositório de conhecimento.

## Sistemas conversacionais e autoria

| Referência primária | O que sustenta | Limite de uso no MIMESIS |
|---|---|---|
| SimSimi Inc., manual do SimSimi Workshop, seção sobre o funcionamento da SmallTalk API. [Manual oficial](https://workshop.simsimi.com/en/document) | O texto do usuário orienta a procura de perguntas candidatas. Cada Talkset liga uma pergunta a uma resposta. Parâmetros e outras condições participam da escolha. | A página consultada apresenta o corpo do manual em coreano. Ela permite descrever o fluxo público. Métrica de distância, índices, pesos e limiares internos permanecem indeterminados. |
| Elan Ruskin, GDC 2012, apresentação da Valve sobre diálogo dinâmico. [Apresentação e resumo da GDC](https://gdcvault.com/play/1015317/AI-driven-Dynamic-Dialog-through) · [Catálogo da Valve, entrada de 2012](https://www.valvesoftware.com/en/publications) | Usa fatos do mundo para selecionar falas escritas a partir de uma base de padrões. A Valve cataloga a apresentação como *Rule Databases for Contextual Dialog and Game Logic*. | A expressão “fuzzy pattern matching” na apresentação descreve correspondência contextual. Atribuir distância de edição sobre texto à Valve exigiria evidência adicional. |
| Elokence, descrição de Akinator publicada pela desenvolvedora. [Ficha na App Store](https://apps.apple.com/us/app/akinator/id933135994) | O jogador pensa em um personagem, responde a perguntas e o sistema tenta identificá-lo. | A interface inspira um experimento sobre quando perguntar. Essa descrição comercial não documenta Bayes, árvores ou política de escolha da próxima pergunta. |
| Saizheng Zhang et al., ACL 2018, estudo de agentes de diálogo condicionados a perfis. [Artigo e metadados](https://aclanthology.org/P18-1205/) | Estuda o condicionamento por perfil e a predição da próxima fala em conversas. | A avaliação com perfis oferece uma pergunta experimental para Persona. Adotar dados, redes ou conclusões quantitativas do estudo requer decisões próprias. |
| Jia-Chen Gu, Zhen-Hua Ling, Xiaodan Zhu e Quan Liu, EMNLP-IJCNLP 2019, seleção de respostas personalizadas. [Artigo](https://aclanthology.org/D19-1193/) | Formula a seleção entre respostas candidatas em função de contexto e personalidade e testa uma arquitetura neural. | O desenho da tarefa se transfere como comparação. Resultados, modelos e distribuições dos dados não constituem uma linha de base medida em nosso ambiente. |

## Recuperação, grafia e representação vetorial

| Referência primária | Atribuição e aplicação |
|---|---|
| Christopher D. Manning, Prabhakar Raghavan e Hinrich Schütze, *Introduction to Information Retrieval*, Cambridge, 2008. [Edição da editora](https://www.cambridge.org/highereducation/books/introduction-to-information-retrieval/669D108D20F556C5C30957D63B5AB65C) | Os capítulos 3, 6 e 8 dão o vocabulário para tolerância ortográfica, pesos de termos, cosseno e avaliação da recuperação. Comparar respostas requer nossos próprios julgamentos de relevância. |
| Stephen Robertson e Hugo Zaragoza, *The Probabilistic Relevance Framework: BM25 and Beyond*, 2009. [Publicação e DOI](https://doi.org/10.1561/1500000019) | Fundamenta ponderação por frequência, saturação e normalização de comprimento. Há variantes de BM25. O artigo e o manual do backend respondem a perguntas distintas. |
| Equipe SQLite, *FTS5 Extension*, seções 4.3.1 e 5.1.1. [Manual do FTS5](https://www.sqlite.org/fts5.html) | Especifica tokenização, opções para diacríticos e orientação crescente da ordenação de bm25(). O manual fixa k1 e b nessa função. A compilação e a configuração deverão ser registradas durante o experimento. |
| Unicode Consortium, UAX #15. [Unicode Normalization Forms](https://www.unicode.org/reports/tr15/) | Define equivalência canônica e formas como NFC. A remoção de diacríticos, a redução de caixa e a modernização de grafia são escolhas distintas da política linguística. |
| Projeto RapidFuzz, documentação do módulo fuzz. [Definições dos comparadores](https://rapidfuzz.github.io/RapidFuzz/Usage/fuzz.html) | Especifica que fuzz.ratio usa similaridade Indel normalizada. O nome exato da função controla o significado de um resultado fuzzy. |
| Projeto scikit-learn, documentação de representação textual e cosseno. [Extração de atributos](https://scikit-learn.org/stable/modules/feature_extraction.html) · [Definição de cosine_similarity](https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html) | Explicita tokenização, n-gramas, pesos, suavização e operações vetoriais da biblioteca. Opções devem ser fixadas para comparar configurações. |
| Projeto RE2, especificação de comportamento do mecanismo de expressões regulares. [Documentação dos autores](https://github.com/google/re2) | Mostra como um subconjunto de padrões pode garantir tempo linear no comprimento da entrada para uma expressão fixa. Outros mecanismos têm características diferentes. |
| Scott Deerwester et al., *Indexing by Latent Semantic Analysis*, 1990. [Publicação dos autores](https://www.microsoft.com/en-us/research/publication/indexing-by-latent-semantic-analysis/) | Investiga redução de dimensão da matriz termo-documento e associação latente. Fundamenta uma alternativa clássica à representação neural. |
| Nils Reimers e Iryna Gurevych, EMNLP-IJCNLP 2019. [Sentence-BERT](https://aclanthology.org/D19-1410/) | Estuda representações de sentenças para comparação por similaridade. É referência para um possível braço experimental local, dependente da adequação do modelo ao idioma. |
| Equipe Faiss, documentação do projeto. [Descrição e métodos de pesquisa](https://faiss.ai/index.html) | Distingue representação vetorial e busca de vizinhos por distância ou produto interno. Um índice aproximado exige comparação com busca exata. |
| Valeria de Paiva, Alexandre Rademaker e Gerard de Melo, COLING 2012. [OpenWordNet-PT](https://aclanthology.org/C12-3044/) | Descreve um recurso léxico-semântico para português. O artigo dá suporte à abordagem por sentidos. Uso dos dados exige verificar a versão, a proveniência e os termos da distribuição pertinente. |

## Regras, escolha e planejamento

| Referência primária | Atribuição e aplicação |
|---|---|
| John McCarthy, *Programs with Common Sense*, 1959. [Texto do autor](https://www-formal.stanford.edu/jmc/mcc59.pdf) | Trata a representação declarativa de premissas e consequências como parte do projeto de um sistema simbólico. |
| Bruce G. Buchanan e Edward H. Shortliffe, organizadores, *Rule-Based Expert Systems*, 1984. [Livro do projeto MYCIN](https://impact.dbmi.columbia.edu/shortliffe/Buchanan-Shortliffe-1984/MYCIN%20Book.htm) | Documenta representação por regras, avaliação e explicação em um sistema especialista. Regras narrativas precisarão de validação específica do domínio textual. |
| Agnar Aamodt e Enric Plaza, *Case-Based Reasoning: Foundational Issues, Methodological Variations, and System Approaches*, 1994. [Artigo disponibilizado por coautor](https://www.iiia.csic.es/~enric/papers/Aamodt_1994_Case.pdf) | Descreve recuperação, reutilização, revisão e retenção. A retenção proposta para MIMESIS passaria por revisão humana e nova distribuição. |
| Richard Cyganiak, David Wood e Markus Lanthaler, editores, W3C Recommendation, 2014. [RDF 1.1 Concepts and Abstract Syntax](https://www.w3.org/TR/rdf-concepts/) | Formaliza grafos de triplas sujeito–predicado–objeto. Ilustra um modelo possível de relações dirigidas. A escolha de RDF como serialização permanece aberta. |
| J. R. Quinlan, *Induction of Decision Trees*, 1986. [Registro e artigo](https://mlanthology.org/mlj/1986/quinlan1986mlj-induction/) | Fundamenta indução de árvores a partir de exemplos e ganho de informação. A implementação CART do scikit-learn dispõe de seus próprios critérios e limites. [Guia do scikit-learn](https://scikit-learn.org/stable/modules/tree.html) |
| Projeto scikit-learn, guia de Naive Bayes. [Documentação dos autores](https://scikit-learn.org/stable/modules/naive_bayes.html) | Explicita independência condicional das evidências dada a classe para o modelo ingênuo. Interpretação de probabilidades requer avaliação de calibração. |
| Dave Mark e Kevin Dill, GDC 2010. [Improving AI Decision Modeling Through Utility Theory](https://www.gdcvault.com/play/1012410/Improving-AI-Decision-Modeling-Through2d) | Baseia a investigação de curvas que convertem atributos em preferências entre comportamentos. Os pesos propostos para o motor são matéria de experimento. |
| Michele Colledanchise e Petter Ögren, *Behavior Trees in Robotics and AI: An Introduction*. [Versão dos autores](https://arxiv.org/abs/1709.00084) | Estuda execução hierárquica e reativa com estados de retorno e composição de comportamentos. |
| Jeff Orkin, GDC 2006. [Three States and a Plan](https://gdcvault.com/play/1013459/Three-States-and-a-Plan) | Relato primário de planejamento orientado a objetivos em um sistema interativo. O paralelo admissível aqui é ordenar atos discursivos sob restrições. |
| Python Software Foundation, documentação de random. [Amostragem e reprodução](https://docs.python.org/3/library/random.html) | Explicita seleção com pesos relativos, semente e limites de compatibilidade entre versões. Permite formular um teste de reprodução de variedades textuais. |

## Linguagem e geração

| Referência primária | Atribuição e aplicação |
|---|---|
| Noam Chomsky, *Three Models for the Description of Language*, 1956. [Registro acadêmico e DOI](https://experts.arizona.edu/en/publications/three-models-for-the-description-of-language/) | Compara classes de descrição formal da linguagem. Uma gramática de domínio restrito é uma proposta de engenharia para Logos. |
| Claude Shannon, *A Mathematical Theory of Communication*, 1948. [Artigo original em cópia acadêmica](https://web.mit.edu/6.441/spring05/reading/shannon1948.pdf) | Usa fontes estocásticas e aproximações sucessivas da língua. Serve de fundamento para testar a dependência local de uma cadeia de Markov. |
| Kate Compton, Ben Kybartas e Michael Mateas, *Tracery: An Author-Focused Generative Text Tool*, 2015. [Artigo dos autores](https://www.galaxykate.com/pdfs/ComptonKybartasMateas15-Tracery%20An%20Author-Focused%20Generative%20Text%20Tool.pdf) | Mostra gramáticas acessíveis a autores para variação de texto. O controle de concordância e de fidelidade factual em pt-BR é um problema de engenharia próprio do MIMESIS. |

## Como usar uma referência em uma decisão

A ficha de um experimento deve apontar a seção ou versão relevante, a afirmação que ela sustenta, a mudança ensaiada e o resultado obtido localmente. Uma licença de artigo cobre um objeto diferente dos pesos, dos dados, de uma edição ou de trechos que se deseje distribuir. Para insumos, a fonte de verdade é o registro por item da MKB. Uma revisão pode substituir um link indisponível por uma cópia do autor ou do editor, preservando autoria, título, ano e DOI quando houver.

[Índice do motor](INDEX.md) · [Pesquisa](RESEARCH.md) · [Técnicas](ALGORITHMS.md) · [Avaliação](EVALUATION.md)
