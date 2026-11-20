# Plano do piloto MKB-DLG · Research 0.0.0

**Objetivo.** Demonstrar que uma resposta em português brasileiro pode ser rastreada até uma revisão autorizada e que o repertório pode ser avaliado com consultas independentes. A decisão de prontidão encerra Research e dá início à implementação de Genesis.

## Diagnóstico de 19 de novembro de 2026

- [x] Conferir os dois checkouts. O motor em `eb24988` contém 24 arquivos versionados. A MKB local contém 30 documentos e ainda não tem commit. O inventário encontrado cobre os contratos. Uma edição piloto liberada continua pendente.
- [x] Seguir uma fala pelo contrato. No exemplo didático, `a-02` pertence a `r-017`, revisão 1. A referência aponta para o artefato `a-041`, linha 1, a atividade `ev-003`, a origem `s-004` e o parecer `d-009`. O estado `PROCESSED` torna a revisão inelegível para o repertório servido. Esta conferência documental identifica o primeiro caso de rejeição a testar com dados reais. [Metadados](../../../../mimesis-knowledge/docs/METADATA_SPECIFICATION.md)
- [x] Conferir o alcance das decisões. O ADR 0001 atribui a curadoria à MKB e os fatos externos à aplicação consumidora. O ADR 0002 define o índice SQLite reconstruível a partir das revisões selecionadas no manifesto. O ADR 0003 propõe uma comparação e mantém em aberto a escolha do recuperador. [ADRs](../../adr/README.md)

## Execução e evidência de saída

| Etapa | Responsável e trabalho | Evidência para concluir |
|---|---|---|
| 1. Selecionar o lote | Na MKB, o responsável pela edição delimita o recorte pt-BR e reserva origem, edição, revisão e domínio. Em paralelo, autoria prepara falas autocontidas e direitos verifica um componente externo candidato para os usos pretendidos. | Ficha de cada origem com responsável, operações autorizadas e evidência. Material com permissão pendente fica fora da seleção. [Coleta](../../../../mimesis-knowledge/docs/DATA_COLLECTION_GUIDELINES.md) |
| 2. Curar Talksets | A equipe da MKB preserva original, hash e localizador. Dois revisores verificam todas as combinações de prompt e resposta e registram divergências para adjudicação. | Matriz de pares revisada. Verificar especialmente negação, mudança de interrogativo, dependência de contexto, IDs duplicados e textos vazios. Rastrear uma resposta real até o parecer e registrar as exclusões. [MKB-DLG](../../../../mimesis-knowledge/docs/domains/MKB-DLG.md) |
| 3. Isolar a avaliação | A equipe de avaliação agrupa origens e paráfrases antes de dividir os dados. Prepara consultas conhecidas, desconhecidas e ambíguas, verifica colisões com prompts e separa julgamentos do repertório. | Manifesto de avaliação com digests, partições por grupo, auditoria de sobreposição e julgamentos adjudicados. Colisões intencionais de igualdade entram no diagnóstico separado. [Benchmark](../../../../mimesis-knowledge/docs/BENCHMARK_DATASETS.md) |
| 4. Decidir a prontidão | O responsável pela edição verifica as revisões selecionadas e os direitos de distribuição. Motor e MKB conferem juntos identidade, esquema e rastreabilidade com dados reais. | Manifesto do piloto, relatório das verificações e decisão registrada de avançar ou corrigir pendências. Compatibilidade funcional exige teste posterior com o motor instalado. [Research](../../releases/0.0.0-RESEARCH.md) |

- [x] Abrir o [lote dlg-pilot-001](../../../../mimesis-knowledge/docs/pilots/dlg-pilot-001.md), preparar dois exemplos sintéticos de oficina e triar um componente externo. A coleta da primeira contribuição humana e o parecer de direitos permanecem pendentes.

## Primeiro trabalho de Genesis após a decisão

Consumir o manifesto liberado e reconstruir a projeção local duas vezes. Verificar igualdade lógica, rejeição de revisões inelegíveis e erro técnico para base incompatível. Em seguida, ligar a mesma política à consulta local e ao executor. Comparar igualdade, Levenshtein e BM25 separadamente sobre o mesmo instantâneo, preservando o ranking anterior à abstenção. Fixar custos de erro, limites de recursos e tolerâncias antes de abrir o teste reservado. A decisão sobre o ADR 0003 exige resultados pareados e medidas no notebook alvo. [Especificação de Genesis](../../releases/0.0.1-GENESIS.md)

## Execução prática de Research em 19 de novembro de 2026

- [x] Preparar Python, uv, os importadores locais e a projeção SQLite/FTS5 experimental. A integração entre os repositórios foi exercitada com pacote temporário de teste. [Operação da MKB](../../../../mimesis-knowledge/RESEARCH.md) · [Compilador de Research](../../RESEARCH_COMPILER.md)
- [x] Processar 50 Talksets sintéticos em dez intenções, incluindo a contribuição recebida como candidata. Os bytes e a linha de origem são rastreáveis. A matriz contém 400 pares pendentes de julgamento. [Inventário](../../../../mimesis-knowledge/pilot/README.md)
- [x] Auditar 33 consultas exploratórias e isolar os três diagnósticos conhecidos. A autoria e os julgamentos compartilhados impedem declarar o teste confirmatório congelado. [Protocolo do lote](../../../../mimesis-knowledge/pilot/benchmark/README.md)
- [ ] Obter pareceres humanos independentes, resolver as divergências e comprovar as permissões de incorporação e redistribuição das revisões selecionadas.
- [ ] Reunir consultas independentes, adjudicar sua relevância e congelar os grupos, os custos de erro e os limites de recursos antes do teste reservado.
- [ ] Compilar uma edição autorizada em duas construções limpas, registrar a compatibilidade e decidir a prontidão para Genesis.
