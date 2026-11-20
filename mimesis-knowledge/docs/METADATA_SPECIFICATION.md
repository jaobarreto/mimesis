# Contrato de metadados e linhagem

**Proposta de contrato para o piloto.** Os registros descrevem unidades intelectuais. Os artefatos identificam sequências de bytes. Outra edição do mesmo livro pode compartilhar a obra e ter bytes, direitos e paginação diferentes. A separação entre entidades, atividades e responsáveis segue a noção de procedência do W3C. [PROV-DM](https://www.w3.org/TR/prov-dm/)

| Campo do envelope | Tipo e obrigação | Regra de validação |
|---|---|---|
| `record_id` | string opaca, global e estável | Atribuir uma vez no registro de identidades. Renomear arquivo não muda a identidade. Não reciclar ID retirado. |
| `revision` | inteiro positivo | Par com `record_id` é único e imutável para o conteúdo e as referências. Correção gera revisão seguinte. |
| `domain` | enum | Um dos dez identificadores MKB. Ligações entre domínios referenciam IDs. |
| `schema_version` | string de três componentes | Validar envelope e payload com a versão exata indicada no manifesto. |
| `language` | string BCP 47 | Usar `pt-BR`, `pt-PT`, `pt` quando a região é incerta, ou `und` quando desconhecida. Época e variedade regional têm anotações separadas. [RFC 5646](https://www.rfc-editor.org/rfc/rfc5646) |
| `source_id`, `rights_id` | strings | Resolver cadastro da origem e decisão de direitos aplicável ao registro e aos derivados. Com várias origens, a linhagem cobre cada entrada e o parecer consolida todas as permissões. |
| `provenance` | objeto | `artifact_id` remete ao artefato de evidência, `locator` localiza o trecho e `activity_ids` ordena os eventos que o produziram. |
| `status` | enum | Estado no instantâneo de ciclo de vida. Promoções são eventos auditados. O manifesto de distribuição inclui apenas entradas RELEASED. |
| `payload` | objeto segundo domínio | Preservar forma original, referências e unidades dos campos. Projeções resumidas usadas nas páginas de domínio omitem o envelope por legibilidade. |

**Exemplo didático de registro processado.** Texto criado para ilustrar o contrato. Os identificadores abaixo pertencem apenas ao exemplo. Uma ingestão efetiva precisa dos cadastros referenciados e de seus comprovantes.

```json
{
  "record_id": "r-017",
  "revision": 1,
  "domain": "MKB-DLG",
  "schema_version": "0.1.0",
  "language": "pt-BR",
  "source_id": "s-004",
  "rights_id": "d-009",
  "provenance": {
    "artifact_id": "a-041",
    "locator": "line:1",
    "activity_ids": ["ev-003"]
  },
  "status": "PROCESSED",
  "payload": {
    "prompts": [{"prompt_id": "p-02", "text": "Podemos começar?"}],
    "responses": [{"response_id": "a-02", "text": "Podemos, sim."}]
  }
}
```

### Cadastros associados

| Entidade | Campos exigidos | Sentido |
|---|---|---|
| Fonte | `source_id`, `source_type`, `title`, `creator`, `source_locator`, `checked_at` | Identifica catálogo, edição, lote próprio ou contribuição. Em origem interna, localizar declaração arquivada. |
| Artefato | `artifact_id`, `source_id`, `media_type`, `byte_length`, `sha256`, `storage_locator`, `acquired_at`, `rights_id` | SHA-256 hexadecimal minúsculo de 64 dígitos sobre bytes exatos antes de extrair ou recodificar. Localizador estável e sem credenciais. |
| Direitos | `rights_id`, `evidence_locator`, `scope`, `jurisdiction`, `decision`, `reviewer_id`, `reviewed_at`, `obligations` | O escopo distingue acesso, cópia interna, extração, transformação e redistribuição. Anexar condições, titulares e prazo quando aplicáveis. |
| Atividade | `activity_id`, `input_ids`, `output_ids`, `operation`, `tool_version`, `config_digest`, `agent_id`, `occurred_at` | Apontar para entradas e saídas imutáveis. Em operação manual, identificar protocolo e revisão. |
| Evento de estado | `event_id`, `record_id`, `revision`, `from_state`, `to_state`, `reason`, `agent_id`, `occurred_at` | Manter histórico, inclusive rejeições. Em RAW o item rastreado pode ser um artefato antes de existir um registro semântico, caso em que usar `artifact_id` no lugar do par. |

Datas operacionais usam UTC em ISO 8601, com `Z`. A data literária pode ter precisão de ano ou período incerto, declarada como tal. Para texto extraído, o localizador pode apontar intervalo de pontos de código Unicode com início inclusivo e fim exclusivo na transcrição original identificada por hash. São admitidos localizadores específicos do formato, por exemplo página mais região em fac-símile, ou identificador TEI. Transformações que alterem comprimento registram um mapa para a representação anterior.

**Regras de integridade.** Uma liberação seleciona uma revisão por identidade e fecha as referências entre registros. O estado é projetado dos eventos até a publicação. Duas materializações do mesmo conteúdo em estados diferentes têm hashes de arquivo próprios. O recibo de cada publicação fixa o arquivo e seu estado histórico. Usar `und` quando o idioma for indeterminado e `pt` quando houver evidência de português, mas a região for incerta. Origem desconhecida, decisão de direitos ausente ou hash divergente impede a liberação.

[Formatos](DATA_FORMATS.md) · [Dicionário de dados](DATA_DICTIONARY.md) · [Versionamento](VERSIONING.md)
