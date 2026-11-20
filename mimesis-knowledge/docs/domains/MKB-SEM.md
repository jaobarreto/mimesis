# MKB-SEM · Conhecimento semântico

**Proposta arquitetural.** Representar acepções explicitadas por definições e ligações tipadas. Uma aresta comunica uma afirmação revisada. Similaridade calculada por um algoritmo pode propor arestas para avaliação.

## 1. Finalidade

Dar ao motor acesso a relações de significado explicáveis para desambiguar consultas, recuperar vocabulário ou limitar expansões. “Banco” no sentido de assento admite relações diferentes de “banco” no sentido de instituição.

## 2. Escopo

Conceitos, acepções localizadas, rótulos preferidos e alternativos, relações hierárquicas, associativas e de oposição. O vocabulário de relações possui semântica própria. Fatos contingentes fornecidos por uma aplicação ficam no contexto.

## 3. Responsabilidades

Definir o sentido com uma glosa e um discriminador de uso, explicitar direção e alcance da relação e impedir expansões indevidas por polissemia. O domínio mantém justificativas editoriais de vínculos interlinguísticos.

## 4. Tipos de conhecimento

`concept` descreve uma acepção. `relation` codifica uma ligação tipada entre dois conceitos. Um vínculo de lexicalização conecta uma entrada LEX a uma acepção. Rótulos alternativos podem ter restrições de registro ou período.

## 5. Estrutura dos registros

Um conceito requer `kind`, `preferred_label` e `gloss`. Uma relação requer `subject_id`, `predicate`, `object_id` e `rationale`. Para `broader`, a leitura proposta é “o sujeito tem o objeto como conceito mais amplo”. Exemplo fictício de payload, cujos alvos representariam um banco de praça e um assento, respectivamente.

```json
{"kind":"relation","subject_id":"s14","predicate":"broader","object_id":"s27","rationale":"Na acepção descrita, o banco é um tipo de assento."}
```

## 6. Relações entre entidades

Uma entrada LEX pode lexicalizar vários conceitos e cada conceito pode ter vários rótulos. `related` e `antonym` recebem interpretação simétrica quando assim declarados no inventário local. A hierarquia admite mais de um conceito amplo. A transitividade só se aplica às operações explicitamente definidas. A distinção entre associação e hierarquia encontra precedente no SKOS. [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)

## 7. Metadados obrigatórios

Usar o [envelope comum](../METADATA_SPECIFICATION.md). Identificar idioma da glosa, inventário e versão dos predicados, fonte do sentido e justificativa ou evidência da ligação. Para alinhamentos externos, registrar a versão e o identificador externo de cada conceito considerado.

## 8. Fontes candidatas

Acepções próprias contrastadas em contexto, exemplos de LIT depois de revisão e OpenWordNet-PT sob avaliação por versão. Preservar a diferença entre glosa externa e glosa redigida pela equipe. Uma licença da estrutura de rede pode exigir análise distinta da licença do texto associado.

## 9. Importação

Mapear identificadores externos a candidatos locais por versão. Importar um tipo de relação de cada vez e documentar equivalência, inversão de direção ou ausência de correspondente. Reservar os casos duvidosos para adjudicação. O texto idêntico de dois rótulos não autoriza a fusão dos conceitos.

## 10. Processamento

Testar a glosa com um exemplo e um contraexemplo. Distinguir “mesma forma”, “mesmo sentido no contexto” e “associação temática”. Registrar separadamente as sugestões por coocorrência e os vínculos aceitos pelo curador.

## 11. Validação

Checar domínios dos dois alvos e regras de autorrelação, direção e ciclos por predicado. Rejeitar hierarquia em que um conceito se torna seu próprio ancestral, inclusive por caminho indireto. Uma cadeia de antônimos não implica equivalência entre as pontas.

## 12. Indexação

Índice lexical por rótulo/idioma e listas de adjacência por `(subject_id, predicate)` e `(object_id, predicate)`. Limitar profundidade e registrar o caminho de uma expansão. Pré-computação do fechamento hierárquico dependerá do custo observado.

## 13. Utilização pelo motor

Lexicon pode propor consulta expandida em um sentido escolhido e comparar com busca lexical simples. A explicação deve trazer o conceito escolhido, a relação e o impacto no ranking. Se a acepção não puder ser desambiguada, preservar candidatos concorrentes ou abster-se da expansão.

## 14. Versionamento

Nova glosa editorial sem alteração de sentido revisa o conceito. Divisão de acepção cria conceitos novos e exige reexaminar arestas e julgamentos afetados. Uma release fixa conceitos, relações e inventário em conjunto.

## 15. Limitações

Conceitos discretos simplificam gradações e metáforas. Relações associativas podem degradar a precisão quando percorridas sem restrição. Uma relação local de proximidade não garante substituição livre em qualquer frase.

## 16. Critérios de qualidade

Avaliar expansão em conjuntos com homógrafos, relações invertidas e associações irrelevantes. Registrar precisão das arestas em amostra adjudicada, cobertura de sentidos e efeito sobre MRR ou Recall@K do consumidor. Qualquer ganho é hipótese até comparação com a mesma partição congelada.
