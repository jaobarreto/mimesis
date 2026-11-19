# Fronteira de responsabilidade

| Pertence ao motor | Pertence ao sistema consumidor |
|---|---|
| Interpretar a entrada, recuperar registros, ordenar respostas, explicar uma escolha e sinalizar desconhecimento. | Identificar e autenticar usuários, solicitar a interação e decidir como exibi-la. |
| Representar a personalidade recebida, modular uma fala e, em versões futuras, manter memória conversacional com origem. | Criar personagens e mundos, gerir calendário, inventário, combate, campanhas, rolagens e demais regras de RPG. |
| Realizar linguisticamente um fato fornecido, por exemplo `door.state = closed`. | Decidir se a porta abre, persistir o estado e autorizar eventuais pedidos de alteração. |
| Devolver texto e referências a evidências. | Implementar frontend e backend de Limiar ou de qualquer outro produto. |

**Contrato de autoridade.** A entrada externa identifica sujeito, atributo, valor e origem. A ausência de valor significa desconhecimento. Uma pergunta, uma fala de personagem e uma lembrança alegada continuam distinguíveis de uma observação autorizada. O texto produzido não é um canal de escrita no sistema externo. Uma futura proposta de alteração precisaria de protocolo de autorização próprio e de confirmação externa para passar a ser considerada fato.

**Limite da primeira etapa.** Research entrega pesquisa, critérios e contratos. Genesis aplicará recuperação textual em domínio delimitado. Síntese livre de acontecimentos, entendimento geral da linguagem e treino autônomo por conversas excedem esse primeiro marco. Regras de Iron Valley ou de qualquer outro RPG ficam no consumidor.

**Teste de fronteira proposto.** Dois consumidores enviam a mesma coleção de fatos usando identificadores distintos de aplicação. A resposta deve depender dos valores expressivos autorizados. O teste falha se a escolha consulta uma tabela de regras do jogo ou grava estado no consumidor. [Arquitetura](ARCHITECTURE.md) · [Testes](TESTING_STRATEGY.md)
