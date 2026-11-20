# Versões, compatibilidade e retirada

**Decisão do briefing.** Motor e MKB evoluem em repositórios independentes, com pares compatíveis explícitos. **Proposta.** `engine_version` identifica o produto instalável, `knowledge_version` identifica um instantâneo imutável do conhecimento e `schema_version` identifica o contrato de leitura. Versões de três componentes comunicam a evolução. A política de compatibilidade no período 0.x exige listar cada versão de motor ensaiada. [SemVer](https://semver.org/lang/pt-BR/)

| Situação | Consequência |
|---|---|
| Corrigir texto de uma fala | Nova revisão do registro e nova versão da MKB. Mesmo esquema se os campos conservarem o significado. Repetir testes de comportamento. |
| Mudar tipo, unidade, obrigatoriedade ou sentido de um campo | Novo contrato, migração explícita e novo ensaio de leitura. A proximidade numérica entre versões não concede compatibilidade. |
| Alterar só o algoritmo de busca | Nova versão do motor. Testar contra edições MKB alvo e respectivos esquemas, registrar o par e o perfil de índice. |
| Remover conteúdo | Identidade preservada em registro de retirada quando lícito. Gerar edição substituta e índice limpo, identificar derivados, comunicar revogação pelo canal de distribuição autorizado. |

**Manifesto de liberação proposto.** Exige `knowledge_version`, `schema_version`, `engine_compatibility` (lista fechada de versões, comparação exata), `artifacts` (caminho relativo, tamanho e SHA-256 por arquivo), `records` (seleção inequívoca de IDs/revisões ou referência a inventário com digest), `rights_summary`, `build_profile` e `created_at`. O perfil define campos, tokenizador, normalização e ordenação usados na compilação. O recibo de verificação do motor liga o digest do manifesto aos binários e resultados da matriz. Uma atestação posterior assinada ou identificada pode acrescentar evidência para outra combinação sem editar retroativamente o manifesto publicado. Para o leitor conservador, ampliar a lista aceita requer novo manifesto versionado.

| Matriz | MKB e esquema | Semântica |
|---|---|---|
| Research 0.0.0 | Nenhum pacote operacional publicado | Somente contratos documentais. |
| Genesis 0.0.1 | Primeira edição piloto e esquema a fixar | Alvo de teste. Exige compilação, casos sentinela, regressões e experimento antes da declaração. |
| Versão ausente da lista ou esquema desconhecido | Qualquer | Recusa explícita na abertura, com versões informadas. Preservar base ativa compatível e válida. |

Não usar nomes de branch ou `latest` como identidade de experimento. Registrar commits, versão de perfil e digests locais. Um artefato substituído sob a mesma versão quebra a reprodução. A operação correta é retirar a edição e publicar outra. [Pipeline](DATA_PIPELINE.md) · [Genesis](../../mimesis/docs/releases/0.0.1-GENESIS.md)
