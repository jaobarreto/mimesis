# Arquitetura do motor

**Decisões do briefing.** Duas unidades versionadas, execução local em CPU, conhecimento curado separado do motor, trilha explicável e fatos objetivos sob autoridade externa. **Proposta arquitetural.** Separar a compilação offline da MKB do caminho de uma interação. O limite permite reconstruir o índice ou trocar o recuperador sem mudar os julgamentos usados para comparar respostas.

```mermaid
flowchart LR
  C[Curadoria e direitos] --> M[Manifesto e registros liberados]
  M --> B[Compilação local e verificação]
  B --> I[(SQLite e FTS5)]
  U[Aplicação externa] --> Q[Entrada e fatos autorizados]
  Q --> N[Validação e normalização]
  N --> R[Recuperação]
  I --> R
  R --> E[Elegibilidade e classificação]
  Q --> E
  E --> S[Seleção ou fallback]
  S --> T[Resposta e trilha]
  T --> U
```

| Limite lógico | Entrada → saída | Invariante e falha |
|---|---|---|
| Carregamento | manifesto, conjunto de registros, configuração → índice validado | Confere compatibilidade, hashes, chaves e direitos. Falha preserva o índice anterior. |
| Linguagem | texto original + perfil → chave de busca e tokens | Original permanece disponível apenas no escopo autorizado. Mesmo perfil na compilação e na consulta. |
| Recuperação | chave + índice → IDs de prompts e escores por estratégia | Recuperar por idioma e versão. Coleção vazia ou incompatível é condição técnica distinguível. |
| Elegibilidade e classificação | candidatos + restrições → candidatos ordenados e motivos | Excluir idioma inadequado e condições conhecidas como falsas. Vínculo operacional órfão invalida a base. Campo obrigatório desconhecido também impede o candidato. |
| Seleção e composição | candidatos elegíveis + política → resposta, esclarecimento ou abstenção | Fixar desempate. Composição futura referencia o fato de origem de cada afirmação. |
| Observabilidade | IDs, versões, escores e motivos → eventos locais | Reproduzir a escolha em ambiente controlado. Minimizar captura de conteúdo sensível. |

### Uma interação que atravessa o limite

Imagine que a aplicação forneça `window.state = closed`. A pergunta “Como está a janela?” admite uma descrição do estado somente se a resposta estiver vinculada ao fato vigente. Um template futuro poderá flexionar o adjetivo. Se a janela deixa de constar do contexto, a saída admissível passa a ser um esclarecimento. Genesis pode usar repertório conversacional independente de estado. Talksets que pressupõem fatos do mundo ficam inelegíveis até que exista verificador para suas condições.

### Crescimento por capacidade

A organização futura separa `core` (orquestração e contratos), `language` (representações), `intent` e `semantic` (hipóteses de intenção e conceitos), `talkset` e `knowledge` (consultas ao repertório), `ranking` (comparação) e `reasoning` (inferência com premissas). `persona`, `context`, `emotion` e `memory` produzem restrições e sinais com duração definida. `narrative` planeja o conteúdo a partir de fatos e `composition` realiza a superfície textual. `learning` mantém propostas supervisionadas fora da consulta. Esses limites orientam dependências futuras. Os diretórios surgem junto ao primeiro uso testável.

Por proposta, a memória de uma sessão armazena eventos identificados, separados da MKB publicada. O contexto identifica a versão ou instante do fato. Uma nova observação da aplicação tem precedência sobre recordações anteriores. Um estado emocional simulado afeta expressão e expira por política. Inferências carregam premissas e podem ser retiradas quando elas caducam.

### Contrato entre repositórios

O compilador previsto no motor entende o esquema publicado na MKB. `talkset_id` referencia o `record_id` liberado. O manifesto fixa a revisão. O motor abre a cópia operacional em leitura. Uma atualização prepara, verifica e ativa um índice completo fora de consultas em curso. Os contratos de esquema e os detalhes operacionais estão na [engenharia da MKB](../../mimesis-knowledge/docs/ARCHITECTURE.md), no [versionamento](../../mimesis-knowledge/docs/VERSIONING.md) e na [especificação executável futura](releases/0.0.1-GENESIS.md).

**Limitações conhecidas.** Recuperação transfere a adequação do repertório para a saída. Textos parecidos podem inverter uma intenção por negação. Cobertura baixa ou contradição entre premissas exige abstenção. A arquitetura mantém disponíveis os sinais necessários para investigar cada classe de erro.
