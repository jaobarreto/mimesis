# Taxonomia e política de classificação

**Decisão aprovada.** Cada registro pertence a um dos dez domínios da MKB. **Proposta arquitetural.** Descrever cada item em eixos independentes. O domínio responde quem mantém a afirmação. O subtipo responde que unidade ela representa. Os descritores registram propriedades observadas com uma autoridade e um vocabulário versionado.

| Eixo | Exemplos técnicos | Uso |
|---|---|---|
| `domain` | `MKB-LIT`, `MKB-LEX`, `MKB-SEM`, `MKB-DLG`, `MKB-NAR`, `MKB-CTX`, `MKB-PSY`, `MKB-BEH`, `MKB-REA`, `MKB-LRN` | Um por registro. Criar derivados quando houver afirmações de naturezas distintas. |
| Subtipo do payload | `fragment`, `lexical_entry`, `concept`, `talkset`, `template`, `signal`, `profile`, `behavior`, `rule`, `judgment` | Os perfis com alternativas usam `kind` para discriminar subtipos. O perfil mínimo de Talkset é reconhecível pelos seus membros. |
| Categoria literária | `dialogue`, `turn`, `environment`, `emotion_expression`, `gesture`, `sensation`, `action`, `reaction`, `conflict`, `transition`, `syntactic_structure`, `vocabulary`, `literary_construction` | Multivalorado e ancorado. Um mesmo período pode conter fala e gesto com intervalos diferentes. |
| Função comunicativa | `greeting`, `request_clarification`, `acknowledgment` | Rótulos candidatos a intenções revisadas. A recuperação lexical de uma frase não comprova sua intenção. |
| Relação de significado | `broader`, `related`, `antonym` | Vínculos tipados em SEM. A direção e as inferências permitidas dependem de cada relação. |
| Idioma e variedade | `language`, região, período de produção, registro de uso | Datar a origem ou indicar incerteza. Preservar a distinção entre pt-BR, pt-PT e formas históricas. |
| Certeza da anotação | `observed`, `inferred`, `uncertain` | Proposta de vocabulário editorial. A anotação incerta permanece disponível para adjudicação. |
| Estado no pipeline | `RAW`, `PROCESSED`, `CURATED`, `RELEASED`, `REJECTED` | Controla revisão e distribuição. Ordem de publicação e validade semântica são avaliadas separadamente. |

## Decisões de fronteira

- **LEX e SEM.** “Manga” pode ter uma entrada para uma forma e ligações a conceitos distintos. Um par de palavras parecidas na grafia pode justificar um teste de busca aproximada. Uma ligação de sentido exige evidência e tipo em SEM.
- **LIT, DLG e NAR.** A fala fictícia “Ainda há ruído no corredor?” tem posição na edição. Para virar Talkset, requer respostas elegíveis para todas as variantes. Para virar modelo, requer parâmetros tipados e avaliação de fidelidade. Preservar a derivação nos dois casos.
- **CTX, PSY e BEH.** Um campo de contexto declara se o interlocutor pediu esclarecimento. O perfil pode preferir frases curtas. Um comportamento relaciona o pedido e a preferência a uma maneira de responder. A ocorrência na sessão pertence ao integrador e à execução.
- **REA e LRN.** Uma justificativa aplicável a vários casos pode ser formalizada como regra. O desacordo de uma pessoa com uma aplicação específica gera um julgamento revisável e vinculado à evidência.

## Manutenção dos vocabulários

Uma proposta de termo deve trazer identificador estável em inglês, definição em pt-BR, exemplo positivo, contraexemplo, domínio responsável e relação com termos existentes. A equipe deve manter sinônimos de busca separados de equivalências conceituais. Mudança de rótulo preserva o identificador. Divisão de um conceito cria novos identificadores e um mapa de migração com os casos que exigem reclassificação manual. Alteração da semântica de uma relação exige rever tanto as arestas afetadas quanto seus consumidores.

Para hierarquias, propor uma direção canônica e testar ciclos na parte que deva ser acíclica. Usar um termo mais amplo somente quando o sentido mais estreito estiver efetivamente contido nele. “Estação” e “chuva” podem estar associadas sem formar uma hierarquia. A separação entre rótulos e relações tem como referência o modelo SKOS. O inventário MKB é uma proposta interna sem compromisso de correspondência integral com SKOS. [W3C SKOS Reference](https://www.w3.org/TR/skos-reference/)

**Questões pendentes.** Escolher inventários de classes gramaticais e variedades regionais após avaliar amostras autorizadas. A lista acima ilustra códigos iniciais. Cada expansão deve registrar motivação, conflitos de anotação e implicações para versões anteriores. A [curadoria](CURATION_GUIDELINES.md) orienta o tratamento de desacordos e o [dicionário](DATA_DICTIONARY.md) define as identidades.
