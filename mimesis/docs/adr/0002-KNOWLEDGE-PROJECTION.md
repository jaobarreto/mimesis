# ADR 0002 · SQLite reproduzível a partir da MKB

**Estado** — decisão aprovada pelo briefing quanto ao SQLite operacional reconstruível. Perfil de construção, digest lógico e troca atômica são propostas de engenharia.

**Contexto.** O banco local precisa responder rapidamente, enquanto a curadoria exige originais rastreáveis, revisões e retirada de material. Um arquivo SQLite opaco como cópia principal ocultaria as transformações e dificultaria reconstruir uma edição autorizada.

**Decisão.** O manifesto da MKB seleciona revisões. O compilador do motor valida o conjunto e cria o índice operacional local. A edição e o perfil de compilação identificam o que foi servido. Alterações no atendimento seguem outra edição após revisão.

**Alternativas e consequências.** Ler JSONL integral a cada consulta reduz o preparo e aumenta trabalho repetido. Manter um serviço de banco dedicado entra em conflito com a operação inicial leve e offline. A projeção proposta precisa de espaço temporário, testes de integridade e uma política explícita de compatibilidade.

**Revisão.** Se compilar em CPU ou manter duas cópias ultrapassar o orçamento do notebook, medir alternativas de construção incremental contra a reconstrução integral, exigindo igualdade lógica e recuperação de interrupção. [Pipeline da MKB](../../../mimesis-knowledge/docs/DATA_PIPELINE.md)
