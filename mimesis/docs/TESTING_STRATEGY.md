# Estratégia cumulativa de testes

O contrato se verifica por comportamento observável na entrada pública. Um teste de rankings pode passar enquanto a aplicação inteira confunde erro de banco com desconhecimento. A especificação distingue cinco níveis que deverão acompanhar cada versão funcional.

| Nível | Preparação e estímulo | Oráculo e falha detectável |
|---|---|---|
| Unidade | Chaves com Unicode composto/decomposto, acentos, negação, espaços, cadeia vazia. | Normalização idempotente e alinhada ao perfil. A forma preservada mantém o original. |
| Contrato | Manifesto didático válido e variantes com versão ausente, hash divergente, ID repetido ou vínculo órfão. | Aceitar o par válido, recusar o defeituoso com causa, preservar edição ativa válida. |
| Integração | Compilar duas vezes um lote congelado, abrir SQLite, recuperar prompts, classificar e resolver direitos pelo ID. | Comparar digest lógico, contagens, ordem, resposta e motivo até a fonte. |
| Ponta a ponta | Instalação local limpa, rede indisponível, execução de CLI proposta com consulta conhecida, ambígua, desconhecida e entrada inválida. | Estados distintos no resultado, recursos medidos e trilha presente. |
| Regressão de pesquisa | Mesmos casos, grupos e manifesto, release anterior e candidata. | Reproduzir baselines, investigar diferenças pareadas e preservar invariantes factuais e de autoridade. |

**Casos metamórficos.** Trocar apenas maiúsculas mantém a saída no perfil proposto de Genesis. Inserir “não” pode mudar a admissibilidade e requer par julgado. Reordenar a inserção de prompts mantém o desempate. Acrescentar resposta julgada inadequada à consulta e depois recuperá-la com alta confiança constitui erro de precisão. Registrar mudanças esperadas junto aos casos.

**Falhas parciais e concorrência.** Simular interrupção após preencher metade da base temporária. Abrir nova sessão durante promoção e conferir que cada sessão observa uma edição completa. Repetir a compilação e validar que índices e contagens não duplicam. Após revogar uma edição por direitos, verificar que trocar para ela também falha no caminho de restauração.

**Isolamento das evidências.** Fixtures sintéticas autorais e pequenas testam invariantes funcionais e podem ser públicas quando autorizado. O conjunto reservado mede generalização e fica fora de exemplos, ajuste e CI pública. Uma falha descoberta no teste de pesquisa pode originar regressão sintética com histórico, enquanto a próxima medida confirmatória usa novo conjunto reservado.

**Saída de versão.** Guardar commits, digests, perfil, casos realmente executados, resultados e causas das exclusões. Verificar a instalação integral e os testes de todas as etapas anteriores. Em Research, a verificação presente abrange documentos, contratos e exemplos. [Avaliação](EVALUATION.md) · [Roadmap](ROADMAP.md)
