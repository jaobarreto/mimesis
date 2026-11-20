# Coleta de dados e contribuições próprias

**Decisão aprovada.** Esta fase especifica o trabalho de coleta para agentes posteriores. São frentes paralelas a descoberta de materiais externos e a autoria deliberada em pt-BR. A unidade entregável de uma futura coleta é um lote identificável, com originais autorizados, evidência de procedência e direitos, contagem explicada e escopo delimitado. [Pipeline](DATA_PIPELINE.md) · [Registro de fontes](DATASET_REGISTRY.md)

## Preparar a tarefa

1. Registrar no acompanhamento do lote um responsável, `source_id` ou fila de descoberta, domínio pretendido, idioma/variedade procurados, unidade de amostragem, usos solicitados e limite de volume compatível com o SSD. Verificar se outro agente reservou o mesmo item externo ou a mesma contribuição. A descoberta pode terminar em uma ficha sem conteúdo.
2. Consultar a página do provedor e a ficha da edição, documentação dos arquivos, termos do canal de acesso e decisões anteriores. No acervo literário, identificar autoria, edição, colaboradores, tradução e revisão. No diálogo, distinguir coleta humana, interação com agente, geração sintética e origem indeterminada. Guardar URLs permanentes e evidência datada. [Licenciamento](LICENSING.md)
3. Conferir permissão para a ação imediata. Permissão de guarda local pode ser suficiente para um lote restrito, desde que o processamento, a saída do motor e a redistribuição sejam decididos nas etapas correspondentes. Se a guarda não está resolvida, manter somente a ficha e os metadados permitidos. Se a análise depender de acesso a dados pessoais, abrir a decisão de governança antes de receber os dados. [Governança](DATA_GOVERNANCE.md)
4. Planejar inspeção pequena por unidade editorial, idioma, gênero e qualidade de extração. Priorizar TXT UTF-8, XML/TEI, JSON ou JSONL, EPUB, HTML e CSV conforme a estrutura que se deseja preservar. Um texto TEI com falantes marcados pode ser preferível ao TXT. Usar PDF ou DOCX quando faltarem formatos melhores. Atribuir prioridade menor ao PDF digitalizado e justificar o custo de OCR e revisão. Registrar a razão da escolha. [Formatos](DATA_FORMATS.md)

## Aquisição futura por arquivo

| Momento | Ação do coletor | Evidência que outro agente consegue verificar |
|---|---|---|
| Antes de transferir | Fixar URL da ficha e URL de obtenção permitida, identificador do provedor, revisão e modo de acesso. Respeitar limites de acesso e interromper no volume planejado. | Identidade do item e decisão de direitos para a obtenção. Um identificador permanente ajuda caso a URL de entrega expire. |
| Durante a transferência | Usar área temporária, limitar expansão de arquivos compactados, observar tipo real e rejeitar arquivos incompletos. Preservar bytes antes de qualquer recodificação. | Data e hora UTC, tipo, tamanho e SHA-256 dos bytes finais. Um ETag não substitui o hash local. |
| Ao registrar o original | Guardar bytes uma vez no local autorizado. Manter nome externo como metadado e associar o artefato a `source_id`, `rights_id`, idioma, responsável e controle de acesso. | Registro administrativo do artefato e localizador interno resolvível. Um local de acesso restrito não vaza por URL com credencial em manifesto público. |
| Ao repetir ou retomar | Comparar item externo, revisão e hash. Mesmo conteúdo pode ser referenciado por mais de uma fonte. Se o hash mudou sob o mesmo nome, criar nova versão de artefato e abrir comparação. | Uma falha temporária permite nova tentativa sem substituir o original anterior nem duplicar um registro concluído. |
| Ao entregar | Informar quantidade descoberta, recebida, repetida, inacessível, pendente e rejeitada com denominadores explícitos. Indicar arquivos restritos e os dados que ficaram só em catálogo. | Manifesto e relatório de reconciliação. Só entradas efetivamente adquiridas podem constar como originais recebidos. |

Não iniciar transformações no único exemplar permitido. Registrar o SHA-256 e os detalhes das atividades no manifesto. O envelope de um registro linguístico usa `provenance` com `artifact_id`, `locator` e `activity_ids`. As atividades detalham ferramenta/versão, parâmetros, entradas, saídas, hashes, responsável e data. Exemplo de localizador adequado é a combinação de edição, página e trecho do TXT derivado. [Metadados](METADATA_SPECIFICATION.md)

## Dados próprios no mesmo ciclo

Uma contribuição original supervisionada exige evidência de autoria e dos termos aceitos. O autor recebe uma instrução de escrita com a finalidade e exemplos de situações inventadas. Entrega o texto de origem, declara autoria/coautoria e intervenções de terceiros, idioma/variedade e os usos autorizados. Vincular essa contribuição a um `source_id` do projeto e a um `rights_id`. Separar a identificação administrativa privada do crédito que o autor permita divulgar. Evitar conversas pessoais e fatos identificáveis de pessoas reais no repertório ficcional.

Para Talksets, pedir entradas realmente intercambiáveis, respostas que sirvam a cada entrada, uma entrada parecida que exija resposta diferente e um caso sem resposta conhecida. Para descrições, solicitar o fato estruturado que a frase deve realizar e conferir se ela acrescenta fatos. Para julgamentos de avaliação, manter o gabarito e o grupo de partição fora das fontes consumidas pelo motor. Um revisor decide adequação, atribui as evidências e envia para nova revisão quando necessário. [Curadoria](CURATION_GUIDELINES.md) · [Benchmarks](BENCHMARK_DATASETS.md)

## Aceite e exceções

Uma tentativa que falha antes da aquisição tem evento de coleta e motivo. Uma revisão já existente que falha na validação segue para `REJECTED` com a sua chave, etapa anterior e motivo permitido. Se a retenção de conteúdo for vedada, conservar o registro administrativo mínimo permitido, determinar a retirada compatível e documentar o alcance. A inclusão em Git depende de tamanho e permissão de distribuição. Materiais volumosos ou de guarda restrita ficam em armazenamento controlado com ponteiro seguro somente quando essa guarda for permitida. [Qualidade dos dados](DATA_QUALITY.md)

**Questões pendentes.** O primeiro lote deverá definir orçamento de disco/tempo medido, convenção institucional para crédito e contatos responsáveis por dúvidas de direitos. A coordenação pode abrir lotes próprios e pesquisas de catálogo em paralelo, sem esperar aprovação geral de um provedor externo. [Instruções permanentes](../AGENTS.md)\n