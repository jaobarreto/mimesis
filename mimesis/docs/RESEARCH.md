# Agenda de pesquisa do MIMESIS

**Pergunta central.** Até onde um motor executado localmente consegue recuperar ou compor uma resposta narrativa apropriada em pt-BR a partir de conhecimento curado, fatos fornecidos e decisões que um revisor consiga reconstruir? A primeira variável observável é a adequação de uma resposta recuperada. Continuidade do diálogo, personalidade e composição serão verificadas em versões posteriores, cada uma preservando a avaliação das anteriores.

O recorte desta etapa é documental. Não há corpus coletado, medições no notebook, comparação executada ou vencedor entre algoritmos a relatar por estes protocolos. O [roadmap](ROADMAP.md) contém a sequência oficial e os critérios de encerramento. O [catálogo](ALGORITHMS.md) especifica as 23 técnicas. A [bibliografia comentada](REFERENCES.md) delimita o que cada fonte pública sustenta.

## Natureza de cada afirmação

| Estatuto | Como ler neste documento |
|---|---|
| Decisão aprovada | Diretriz explícita do briefing, como operação inicial offline, sem LLM, API de IA ou GPU dedicada, separação do motor e dos dados, evolução cumulativa e aprendizado supervisionado. |
| Informação verificada | Comportamento ou método documentado em fonte identificada. A evidência pública pode se restringir à interface. |
| Proposta arquitetural | Maneira de satisfazer uma diretriz. Normalizadores, comparadores específicos, curvas, limiares e políticas de desempate precisam de revisão e evidência antes da adoção definitiva. |
| Hipótese experimental | Previsão com observação capaz de enfraquecê-la. Um resultado de outro projeto não constitui medição no MIMESIS. |
| Questão pendente | Escolha que ainda depende de dados, revisão humana, autorização ou capacidade computacional medida. |
| Limitação conhecida | Restrição já reconhecida da técnica, do método de avaliação ou da evidência disponível. Deve acompanhar qualquer conclusão que dela dependa. |

## O que as inspirações efetivamente permitem concluir

### SimSimi e a unidade de recuperação

**Informação verificada.** No manual da SmallTalk API, um Talkset associa uma pergunta (qtext) a uma resposta (atext). A entrada do interlocutor (utext) orienta a busca por perguntas relacionadas. O AICR considera o conjunto de candidatos, parâmetros da requisição e outras condições ao escolher um Talkset. A resposta ao usuário provém desse par. O manual registra contribuições humanas ao repertório. Não fornece a fórmula do ranking, uma distribuição de pesos ou um contrato de moderação que se possa transpor para o motor. [SimSimi Workshop, seção de funcionamento](https://workshop.simsimi.com/en/document)

**Proposta para Genesis.** Procurar a consulta entre as perguntas do repertório e depois selecionar uma resposta elegível. Esse arranjo evita assumir que a resposta satisfatória precisa repetir as palavras da pergunta. Por exemplo, “Posso começar?” admite “Pode, estou ouvindo.” A segunda frase pode ter pouca sobreposição com a consulta. O modelo lógico do MIMESIS permite agrupar variantes quando cada resposta serve a cada pergunta do grupo. Um revisor deve dividir o registro se encontrar uma combinação inadequada. É uma decisão de modelagem própria, com identificadores que permitem remontar o par escolhido. [Contrato de Genesis](releases/0.0.1-GENESIS.md)

**Hipótese.** Um repertório pequeno com perguntas funcionais bem delimitadas pode obter alta precisão nas entradas que cobre. Duplicar perguntas sem controlar adequação e colisões pode aumentar as respostas incorretas. A observação que distingue os efeitos é uma curva de cobertura e falsas aceitações a cada incremento curado do repertório, usando o mesmo teste preservado. Um item ausente e uma falha de ranking precisam de códigos de diagnóstico distintos na análise.

### Valve e seleção por fatos

**Informação verificada.** Elan Ruskin descreve seleção de falas escritas usando fatos do mundo e correspondência com uma base de padrões. A apresentação é catalogada pela Valve no ano de 2012. A evidência pública fundamenta o uso de condições autorais em contexto. A expressão “fuzzy” ali empregada não identifica um comparador ortográfico a ser adotado em Genesis. [Apresentação de Ruskin na GDC](https://gdcvault.com/play/1015317/AI-driven-Dynamic-Dialog-through) · [Catálogo da Valve](https://www.valvesoftware.com/en/publications)

**Proposta para Context.** Separar requisitos de verdade de preferências estilísticas. No exemplo autoral “A janela continua aberta”, “aberta” exige o estado atual e “continua” pressupõe continuidade temporal. Se o contrato externo fornece apenas o estado atual, “A janela está aberta” pode ser elegível. Se o contrato fornece somente a cor, ambas as frases ficam sem apoio. A trilha registraria a condição ausente e a regra avaliada. Avaliar o caso com a janela aberta, fechada e com estado omitido mede efeitos diferentes do contexto.

### Akinator e perguntas de esclarecimento

**Informação verificada.** A descrição publicada pela Elokence afirma que o produto tenta identificar um personagem a partir de respostas a uma sequência de perguntas. Essa fonte descreve a experiência do jogador. A política de perguntas, a representação de conhecimento e os algoritmos proprietários ficam indeterminados. [Descrição da Elokence](https://apps.apple.com/us/app/akinator/id933135994)

**Hipótese independente.** Em uma conversa com dois referentes plausíveis, uma pergunta curta pode reduzir a chance de responder sobre o referente errado. Uma hipótese técnica futura seria escolher uma pergunta que diminua a entropia esperada entre interpretações. Isso requer probabilidades estimadas, custo de mais um turno e um controle simples, como a pergunta fixa “A qual deles você se refere?”. Medir acerto após esclarecimento, turnos adicionais e frequência de perguntas em casos já resolvidos. Essa hipótese não descreve o algoritmo da Elokence.

### Sistemas especialistas, simbolismo e raciocínio por casos

**Informação verificada.** McCarthy discute representação declarativa de informações e consequências. Os relatos de MYCIN documentam o uso e a explicação de regras em um sistema especialista. Aamodt e Plaza descrevem um ciclo de raciocínio por casos que passa por recuperação, reutilização, revisão e retenção. [McCarthy](https://www-formal.stanford.edu/jmc/mcc59.pdf) · [Buchanan e Shortliffe](https://impact.dbmi.columbia.edu/shortliffe/Buchanan-Shortliffe-1984/MYCIN%20Book.htm) · [Aamodt e Plaza](https://www.iiia.csic.es/~enric/papers/Aamodt_1994_Case.pdf)

**Proposta.** Representar uma regra com premissas tipadas, conclusão permitida, origem e escopo. Por exemplo, o fato externo “entidade A está no recinto B” pode licenciar uma referência a sua presença em B naquele instante. Só uma regra adicional, explicitamente aprovada para o domínio, autorizaria outra conclusão. A falta de uma premissa deixa a conclusão indeterminada. Um caso anterior pode servir de precedente com finalidade consultiva. A retenção em MKB-LRN exige revisão, controle de origem e nova versão. Um diálogo recém-recebido jamais publica conhecimento por conta própria.

### Recuperação conversacional e persona

**Informação verificada.** Zhang e colaboradores construíram uma tarefa de diálogo condicionado a informações de perfil. Gu e colaboradores estudaram seleção de respostas em função do diálogo e da persona com um método neural. As publicações fornecem desenhos de tarefa que distinguem relevância ao texto e adequação ao perfil. Os resultados dos autores pertencem a seus dados e configurações. [Zhang et al., ACL 2018](https://aclanthology.org/P18-1205/) · [Gu et al., EMNLP-IJCNLP 2019](https://aclanthology.org/D19-1193/)

**Proposta.** Preparar cenários pareados com os mesmos fatos e duas personas, por exemplo concisa e expansiva. Avaliadores em pt-BR devem julgar separadamente se a resposta preserva os fatos e se o estilo acompanha o perfil. Uma frase que inventa uma motivação para parecer mais expressiva falha na primeira pergunta. As descrições dos perfis e os textos de teste podem ser próprios. O aproveitamento de material de terceiros exige autorização da edição específica.

### Utility AI, autoria orientada por dados e composição

**Informação verificada.** Mark e Dill discutem modelos de escolha por utilidade. Compton, Kybartas e Mateas descrevem uma ferramenta de gramáticas voltada a autores. Chomsky fornece uma base formal para compreender classes de descrição linguística. As três referências tratam de planos diferentes de decisão. [Mark e Dill](https://www.gdcvault.com/play/1012410/Improving-AI-Decision-Modeling-Through2d) · [Compton, Kybartas e Mateas](https://www.galaxykate.com/pdfs/ComptonKybartasMateas15-Tracery%20An%20Author-Focused%20Generative%20Text%20Tool.pdf) · [Chomsky](https://experts.arizona.edu/en/publications/three-models-for-the-description-of-language/)

**Proposta.** Uma política de utilidade escolhe um ato discursivo elegível. Uma gramática ou um template realiza o conteúdo do ato. Regras, curvas, exemplos e léxico podem evoluir como dados versionados, com verificação dos contratos pelo consumidor. Mudar o peso que favorece concisão e mudar uma regra de concordância exigem testes diferentes. O primeiro deve alterar a escolha de estilo sob fatos idênticos. O segundo deve corrigir a forma sem alterar quais fatos aparecem. Uma regra geral de software ou uma linguagem de templates deve permanecer no repositório responsável por sua manutenção, conforme o [contrato de arquitetura](ARCHITECTURE.md).

## Primeiro ensaio comparativo proposto

**Hipóteses de Genesis.** Igualdade exata deverá oferecer um controle simples para chaves conhecidas. A busca fuzzy pode resgatar erros de digitação em troca de aceitar vizinhos de sentido distinto. BM25 pode favorecer termos informativos em consultas mais longas, mas pouco separa certas entradas curtas da coleção. Não há vencedor estabelecido. O objetivo é estimar essas trocas nas condições de uso, inclusive quando se deveria responder “não sei”.

| Braço isolado | Qual será a busca | O que examinar no erro |
|---|---|---|
| Exact | Igualdade pela chave produzida pelo perfil congelado. | Ausência de variante, colapso indevido de duas chaves ou incompatibilidade entre respostas com a mesma chave. |
| Fuzzy | Comparador ortográfico declarado, com referência exaustiva no repertório piloto. | Nome próprio, negação ou quantidade alterados por uma diferença curta. Verificar se o candidato já faltava antes do ranking. |
| BM25 | Índice dos mesmos prompts elegíveis. Tokenizador e versão do SQLite congelados. Guardar o valor nativo e sua orientação. | Termo dominante enganoso, ausência de tokens e empates associados ao comprimento. O FTS5 ordena as melhores correspondências pelos menores valores brutos. [Manual FTS5](https://www.sqlite.org/fts5.html) |

1. **Congelar população e julgamento.** Separar consultas de diagnóstico de igualdade literal, consultas novas por família e desconhecidos realistas. Reservar famílias de paráfrase, fonte/obra e sessão conforme aplicável. Uma duplicata literal intencional mede reconhecimento de chave conhecida e recebe relatório separado dos testes de generalização. Os itens de teste são inacessíveis ao ajuste de política.
2. **Construir a mesma situação para todos os braços.** Mesmo acervo autorizado, mesma definição de resposta elegível, mesmos rótulos, mesmo K e mesma máquina de referência. Preservar forma original e forma de busca. Documentar diferenças intrínsecas da tokenização FTS. Identificar snapshot, configuração, cópia do teste, versões e hashes.
3. **Calibrar a abstenção em desenvolvimento.** Separar entrada inválida, base indisponível, consulta desconhecida, ambiguidade e resposta recuperável. Predefinir custo de falso aceite e de falsa rejeição. Mínimos e margens podem diferir por método, pois suas escalas diferem. Congelar a política antes de abrir o teste.
4. **Executar e preservar a cadeia de decisão.** Executar três vezes a mesma coleção de consultas, uma passagem por método, inteiramente em CPU local e sem serviço externo. Para aferir latência, fazer também repetições em condições frias e quentes segundo o protocolo específico. Registrar candidatos, famílias, resposta selecionada, escore bruto, filtros, motivo da decisão, tempos e configuração.
5. **Separar as perguntas científicas.** O ranking encontrou a resposta admissível? A política respondeu quando convinha? O acervo tinha resposta? Publicar MRR e P@K/Recall@K entre respondíveis, matriz de abstenção em respondíveis, desconhecidos e ambíguos e cobertura do repertório julgada por humanos. Reportar denominadores, incerteza pareada por família e custo em recursos. [Protocolo de avaliação](EVALUATION.md) · [Protocolo de desempenho](PERFORMANCE.md)
6. **Decidir com as condições declaradas.** Comparar ganho nos erros ortográficos ao prejuízo em contradições, entre outros cortes. Se o ganho for inconclusivo ou o custo exceder o orçamento previamente acordado, preservar o controle e registrar nova pergunta. Um sistema híbrido é um experimento distinto, posterior ao relatório dos três braços.

### Casos diagnósticos autorais

| Consulta ou par | Situação construída | Julgamento necessário |
|---|---|---|
| “Podemos conversar?” / “  PODEMOS conversar?  ” | Mesmo pedido com caixa e espaços diferentes. | Reconhecer a mesma chave se o perfil aprovado assim definir. |
| “Você me ouve?” / “Você me oove?” | Um erro ortográfico em uma consulta conhecida. | Fuzzy pode recuperar o pedido. Verificar contra alternativas parecidas e registrar falso aceite se escolher outra fala. |
| “Eu **não** quero começar” / “Eu quero começar” | Frases próximas com polaridade incompatível. | Tratar como escolhas discursivas distintas. Uma única resposta de anuência para as duas falha o diagnóstico. |
| “O que significa banco?” | Consulta ambígua sem sentido indicado na entrada. | Pode caber esclarecimento curado. Se faltar uma resposta admissível no piloto, a referência é abstenção. |
| “Qual é o nome da pessoa na sala?” | A entrada externa não fornece nomes e a base piloto não oferece resposta apropriada. | Fallback de desconhecimento. Uma resposta com nome específico é indevida mesmo se obtiver alto escore lexical. |

Os exemplos acima ilustram julgamentos. A partição oficial precisa de itens inéditos, revisão independente e origem registrada. Uma política desenvolvida com os exemplos publicados só poderá usá-los como controles de regressão.

## Agenda cumulativa e observações decisivas

| Versão oficial | Pergunta experimental | Comparação que orienta a decisão |
|---|---|---|
| 0.0.0 Research | O protocolo permite a outro pesquisador reproduzir a comparação futura? | Revisar documentação, contratos, proveniência, reprodutibilidade e pendências. Coleta e piloto têm entregas próprias. |
| 0.0.1 Genesis | Um recuperador simples escolhe uma fala apropriada e se abstém diante do desconhecido? | Exact, fuzzy e BM25 isolados, no mesmo snapshot e em casos idênticos. |
| 0.0.2 Lexicon | Relações de sentido ajudam onde quase não há termos em comum? | Ativar e desativar expansão por sentido com controles de polissemia e negação. |
| 0.0.3 Persona | Trocar o perfil muda expressão preservando fatos e pertinência? | Trocas cegas de persona com os mesmos fatos, entradas e candidatos. |
| 0.0.4 Context | A escolha responde ao fato que mudou e admite a informação ausente? | Alterar um fato por vez, testar seu valor desconhecido e exigir rastro do requisito. |
| 0.0.5 Mythos | A descrição torna legível um ambiente fornecido? | Comparar cobertura dos fatos pedidos, omissões e acréscimos com uma realização mínima. |
| 0.0.6 Logos | Mais variedade mantém concordância, coesão e fidelidade? | Comparar frase pronta, template e gramática sob o mesmo plano de conteúdo. |
| 0.0.7 Mnemosyne | O antecedente correto continua acessível entre turnos? | Comparar diálogo com memória habilitada e controle sem memória. Testar sessões distintas e retomada após expiração. |
| 0.0.8 Anima | O estímulo modifica a reação expressiva de maneira consistente com a persona? | Fixar fatos, variar estímulo e duração, comparar política de reação a uma resposta estática. |
| 0.0.9 Sophia | Incorporar correções aprovadas melhora casos inéditos e preserva anteriores? | Medir antes e depois da edição curada, com famílias não vistas e possibilidade de reversão. |
| 0.1.0 Awakening | Capacidades integradas preservam as propriedades demonstradas isoladamente? | Diálogos de múltiplos turnos, ablação de cada capacidade e repetição de todos os testes acumulados. |
| 1.0.0 Mimesis | A evidência cobre as combinações que serão declaradas estáveis? | Instalação independente, matriz de versões compatíveis, reconstrução do índice e execução reprodutível dos cenários acordados. |

O roadmap exige versões cumulativas funcionais após Research. Os ensaios podem rejeitar uma técnica sem mudar o objetivo da versão. Um grafo sem contribuição demonstrada em Lexicon pode dar lugar a uma tabela de relações curadas, desde que a capacidade semântica e a compatibilidade sejam avaliadas.

## Pendências e limites de interpretação

| Questão pendente | Evidência e responsável funcional | Consequência |
|---|---|---|
| Em que situações uma fala é “apropriada” mesmo com outras respostas possíveis? | Curadoria de diálogo e QA devem rotular múltiplos IDs admissíveis, testar a rubrica e adjudicar desacordos preservando votos originais. | Comparar modelos somente onde há julgamentos interpretáveis. |
| Qual peso atribuir a uma resposta indevida frente à abstenção? | Pesquisa e responsáveis pelo uso devem declarar custos, cortes críticos, tolerâncias e orçamentos antes de abrir o teste. | A escolha do limiar e de um eventual vencedor depende desses valores. |
| Qual repertório inicial pode ser utilizado e distribuído? | Curadoria e governança devem conferir autorização, versão e metadados por fonte e edição, incluindo material próprio. | Enquanto faltarem direitos ou origem, o item permanece fora da release. |
| Como tratar abreviações, grafias históricas, regionalismos, acentos e negação? | Linguística deve criar pares positivos e negativos de desenvolvimento e medir colisões por perfil. | Uma modernização que desfaça oposição de sentido deve ser revista e o original preservado. |
| Qual tamanho de repertório e de índice cabe no equipamento? | Engenharia deve medir consultas frias e quentes, reconstrução e pico de memória no Dell Inspiron 15 3520, i5-1235U, 16 GB, SSD de 512 GB e Ubuntu. | Sem medições não há limite de escala ou tempo de resposta demonstrado. |
| Como explicar um candidato vetorial e verificar elegibilidade factual? | Pesquisa semântica deve confrontar busca densa ou latente com expansão simbólica e exigir trilha de evidência no candidato aceito. | Se não houver justificativa suficiente, a técnica continua restrita a laboratório. |
| As conclusões se transferem para outra aplicação, variedade ou repertório? | Avaliação deve repetir o ensaio com origem, distribuição linguística e vocabulário diferentes. | Frases importadas, mesmo em grande número, não demonstram compreensão nem generalização. |

O relatório futuro deve permitir localizar uma falha em pelo menos um estágio identificável, como lacuna do acervo, normalização, indexação, recuperação, ranking, abstenção, elegibilidade ou realização. Divergência persistente entre revisores também é um resultado e deve ser relatada. Uma decisão arquitetural baseada em ensaio deve remeter ao manifesto e à evidência do ensaio. [Registro de decisões](adr/README.md)

[Índice do motor](INDEX.md) · [Visão](VISION.md) · [Técnicas](ALGORITHMS.md) · [Referências](REFERENCES.md) · [Roadmap](ROADMAP.md)
