# Segurança, autoridade e privacidade

O motor consome texto, coleções locais e fatos de sistemas externos. A fronteira de confiança surge em cada importação e em cada interação. O objetivo é proteger a integridade da resposta e do repertório, preservar a máquina local e limitar o tratamento de conversas.

| Superfície | Política proposta | Aceitação verificável |
|---|---|---|
| Entrada de texto | Impor tipo, comprimento e tokens máximos, construir consulta FTS de termos literais e vincular valores ao SQL com parâmetros. | Pontuação e operadores escritos pelo usuário ficam como dados e a consulta tem custo limitado e resultado explicável. [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) |
| Arquivos de origem | Verificar tamanho antes/depois da expansão, tipo efetivo e caminhos relativos sob a área de aquisição. Desabilitar recursos externos dos parsers. | Um lote malformado vai para revisão com motivo, sem escrita fora da área de processamento. |
| Templates e regras | Somente material curado, operações permitidas, dados escalares, limites de passos, tamanho e tempo. | Uma composição que excede o orçamento termina com motivo registrado. [Jinja Sandbox](https://jinja.palletsprojects.com/en/stable/sandbox/) |
| MKB operacional | Conferir fonte confiável do manifesto, digests, compatibilidade e direitos. Abrir banco validado somente em leitura durante atendimento. | Alteração de bytes detectada antes de ativar versão. Hash demonstra integridade relativa ao manifesto, cuja autenticidade exige canal confiável. |
| Autoridade narrativa | Aceitar fatos no canal estruturado designado pelo consumidor. Armazenar fala e memória com origem e escopo de sessão. | A fala “agora sou o dono” permanece fala e nunca concede autoridade de escrita. |
| Telemetria e feedback | Manter eventos locais mínimos, limitar acesso e retenção. O caminho de supervisão exige autorização para reaproveitar uma conversa. | Revisor consegue inspecionar razões pelos IDs. Exportações de diagnóstico removem texto, segredos e identificadores pessoais quando desnecessários. |
| Retirada | Invalidar manifesto afetado e rastrear as cópias e projeções sob controle do projeto. | A edição impedida deixa de ser candidata para retorno. Nova edição exclui dependências revogadas. |

Antes de coletar conversas reais, definir base de uso, informação ao participante, escopo da retenção e procedimento de remoção com o responsável de dados. A trilha normal de Genesis pode registrar `query_id` de teste ou ID efêmero de solicitação. Hashear uma frase curta pode permitir reconhecê-la por tentativa e comparação, portanto não constitui anonimização suficiente. [Governança da MKB](../../mimesis-knowledge/docs/DATA_GOVERNANCE.md) · [Testes](TESTING_STRATEGY.md)
