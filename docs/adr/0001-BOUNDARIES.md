# ADR 0001 · Fronteiras e autoridade

**Estado** — decisão aprovada pelo briefing de Research, seções 2, 4 e 6.

**Contexto.** O ciclo de revisão de um texto e de sua permissão de uso pode ocorrer muitas vezes sem alterar o recuperador. Uma aplicação narrativa externa já possui regras e fatos próprios.

**Decisão.** Manter exatamente dois repositórios independentes. O motor contém algoritmos, contratos de interação e experimentos. A MKB contém fontes, processos, curadoria, manifestos e direitos. No atendimento, os fatos da aplicação chegam com origem. A aplicação controla qualquer alteração autorizada dos próprios fatos.

**Alternativas e consequências.** Um monorrepositório simplificaria commits atômicos entre código e corpus, mas acoplaria seus ciclos de distribuição. Incorporar regras de jogo ao motor reduziria o trabalho do primeiro integrador ao custo de prender as próximas aplicações a esse domínio. Os dois repositórios exigem uma matriz de compatibilidade e revisão conjunta das mudanças de esquema.

**Revisão.** Uma nova integração que precise escrever estado deve apresentar protocolo de autorização do consumidor e tratamento de conflitos antes de estender o contrato. [Escopo](../SCOPE.md) · [Versionamento da MKB](../../../mimesis-knowledge/docs/VERSIONING.md)
