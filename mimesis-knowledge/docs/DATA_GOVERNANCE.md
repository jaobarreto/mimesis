# Governança do conhecimento

**Decisão aprovada.** A origem e as transformações precisam ser rastreáveis, a curadoria é supervisionada e motor e conhecimento têm versões independentes. O estado `RELEASED` depende de uma publicação identificada. **Proposta operacional.** A responsabilidade acompanha a decisão tomada. Um responsável pode exercer mais de uma função em equipe pequena. Registrar quando uma revisão exigida como independente foi realizada por outra pessoa e quando essa verificação ainda está pendente.

## Autoridade e evidência

| Função | Decisão a registrar | Artefato de prestação de contas |
|---|---|---|
| Coordenação de dados | Reserva o lote, define finalidade e quem resolve colisões de trabalho | Identificador do lote, fontes/edições abrangidas, responsável e estado |
| Coletor ou autor | Declara procedência, conteúdo adquirido/produzido e condições conhecidas | Ficha de fonte, recibo do artefato, evidência de autoria e termos para o material próprio |
| Responsável por direitos e privacidade | Fundamenta operações permitidas, território, restrições, retenção e créditos | Decisão `rights_id` versionada por artefato, finalidade e versão da evidência |
| Engenheiro de dados | Responde por limites de extração, normalização, rastreamento e repetibilidade | Eventos de transformação e reconciliação por lote |
| Curador e adjudicador | Julgam precisão do conteúdo e resolvem divergências ligadas a rubricas | Parecer associado a registro e revisão, decisão de aceitação/rejeição e limitações |
| Mantenedor do benchmark | Controla partições, cegamento e exposição de consultas/gabaritos | Manifesto separado, registro de acesso e grupos de vazamento |
| Responsável pela release | Decide a composição, compatibilidade comprovada e publicação/retirada do pacote | Manifesto com `knowledge_version`, `schema_version`, `engine_compatibility`, hashes, avisos e decisões aplicáveis |

Sem evidência de direitos ou de revisão para a finalidade escolhida, o responsável pela release mantém o item fora da seleção. Em caso de conflito entre edições de uma obra, os fatos bibliográficos permanecem associados às respectivas edições. Só se generaliza um registro quando a curadoria documenta a correspondência. [Licenciamento](LICENSING.md) · [Metadados](METADATA_SPECIFICATION.md)

## Colaboração e histórico

1. Reservar tarefas por `source_id`, identificador do item, revisão e escopo de domínio. Duplicação de descoberta é conciliável por referência. Dois agentes que alteram a mesma revisão devem comparar evidências e propor a revisão subsequente antes da publicação.
2. Um evento registra estado anterior, novo estado, responsável, instante, razão e alvo. Os objetos originais e derivados são identificados por hash quando sua guarda for permitida. Uma correção gera nova revisão e aponta a que substitui. O histórico pode manter apenas metadados mínimos permitidos após retirada de conteúdo.
3. Uma divergência de classificação segue ao curador. Uma dúvida sobre o direito de executar uma operação segue ao responsável por direitos e suspende a operação afetada. Uma mudança de esquema ou rubrica é discutida junto aos consumidores, com avaliação dos registros atingidos e plano de migração e revalidação.
4. Guardar a última versão distribuível e um registro de versões retiradas. O caminho de retorno após falha operacional precisa verificar elegibilidade atual. Uma versão retirada por direitos não é candidata a rollback. [Pipeline](DATA_PIPELINE.md) · [Versionamento](VERSIONING.md)

## Acesso e proteção de pessoas

Classificar o destino de cada componente do lote. Texto autorizado para distribuição pública, material permitido apenas para processamento interno, comprovantes administrativos e conjuntos cegos de avaliação possuem necessidades de acesso diferentes. Em manifestações públicas de contribuição, usar a forma de crédito aceita e preservar a ligação interna ao autor conforme as condições de retenção. Proibir credenciais, URLs assinadas, contatos privados e excertos pessoais em commits ou relatórios distribuídos.

Diálogos com humanos e feedback da aplicação podem conter dados pessoais mesmo quando se apresentam como ficção. Antes de receber qualquer material desse tipo, delimitar finalidade, base aplicável, minimização, acesso, prazo de guarda e tratamento de solicitações. Evitar importar nomes, contatos ou logs de usuários para um Talkset. Um pseudônimo pode permitir reidentificação pelo contexto. Preferir exemplos autorais fictícios quando atendem à pergunta de pesquisa. A ANPD explica condições específicas para tratamento para fins acadêmicos e para estudos por órgãos de pesquisa. A qualificação do MIMESIS para uma hipótese legal específica permanece indeterminada. [Guia da ANPD](https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-tratamento-de-dados-pessoais-para-fins-academicos-e-para-a-realizacao-de-estudos-e-pesquisas)

## Contestação e retirada

1. Receber a identificação da edição, arquivo, registro ou release. Dar número ao caso e guardar a comunicação em área com acesso adequado.
2. Conferir o fundamento, o escopo do pedido e as obrigações próprias do material. Se houver exposição indevida plausível, bloquear novas distribuições e usos afetados durante a análise. Registrar a medida e seu alcance.
3. Percorrer `rights_id` e entradas/saídas das atividades até registros, modelos textuais, índices, exportações e benchmarks. Listar hashes, versões e destinos controlados. Um registro derivado de múltiplas fontes pode permanecer afetado mesmo após remover o arquivo original.
4. Decidir manutenção justificada, correção, restrição ou retirada. Recompor o manifesto, reconstruir o SQLite e confirmar ausência do texto atingido nos dados, nas tabelas auxiliares de busca e nos artefatos públicos de teste e documentação. Registrar créditos retificados ou novo fundamento quando aplicável.
5. Marcar releases e hashes afetados como retirados, atualizar canais de distribuição sob controle do projeto e emitir aviso de correção para consumidores. Informar limites de atuação sobre cópias offline anteriores. A tabela de rejeição ou o aviso só guarda o mínimo permitido e não precisa reproduzir o material contestado.

**Critério de ensaio.** Dada uma fonte de teste inventada com um trecho, um Talkset derivado e uma consulta de avaliação, o ensaio local de retirada deve enumerar os três descendentes, gerar seleção substituta e bloquear o pacote anterior. Este é um teste futuro, ainda sem execução ou resultados. [Qualidade](DATA_QUALITY.md)\n