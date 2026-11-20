"""Falas sintéticas exclusivas do ensaio técnico."""

from research_compiler.contract import canonical, sha

EDITION = "synthetic-core-v1"
ROWS = (
    ("parcel", ("Eu posso embrulhar a caixa para você?",), ("Pode embrulhar, por favor.",)),
    (
        "window",
        ("Posso fechar a janela?", "Tudo bem se eu fechar a janela?"),
        ("Pode fechar a janela.", "Sim, pode fechar."),
    ),
    (
        "window-open",
        ("Por favor, não feche a janela.",),
        ("Tudo bem, vou deixar a janela aberta.",),
    ),
    (
        "break",
        ("Podemos fazer uma pausa breve?", "Que tal um breve intervalo?"),
        ("Claro, podemos fazer uma pausa.",),
    ),
    ("room-light", ("A luz está pronta?",), ("A iluminação da sala está pronta.",)),
    ("stage-light", ("A luz está pronta?",), ("A iluminação do palco está pronta.",)),
)


def records(rows=ROWS):
    artifact = sha(canonical(rows))
    return {
        key: {
            "revision": 1,
            "language": "pt-BR",
            "source_id": EDITION,
            "rights_id": "fixture-development-only",
            "provenance": {
                "artifact_id": artifact,
                "locator": f"fixture:{key}",
                "activity_ids": ["authored-synthetic-fixture"],
            },
            "payload": {
                "prompts": [
                    {"prompt_id": f"{key}-p{i}", "text": text} for i, text in enumerate(prompts, 1)
                ],
                "responses": [
                    {"response_id": f"{key}-r{i}", "text": text}
                    for i, text in enumerate(responses, 1)
                ],
            },
        }
        for key, prompts, responses in rows
    }
