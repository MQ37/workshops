"""
SQLJudge — LLM-as-judge pro hodnocení vygenerovaného SQL.

Vidí otázku, generated SQL, reference SQL a (volitelně) raw výsledek.
Vrátí strukturovaný JSON: score + verdict + issues.

Použití:
    from judge import SQLJudge
    verdict = SQLJudge().evaluate(question, generated_sql, expected_sql)
    # → {"score": 7, "verdict": "PASS", "issues": ["chybí status filter"]}

Vyžaduje:
    pip install openrouter
    export OPENROUTER_API_KEY=sk-or-...
"""

import json
import os
import time
from pathlib import Path

from openrouter import OpenRouter
from openrouter.errors import TooManyRequestsResponseError

SCHEMA = (Path(__file__).parent / "schema.sql").read_text()
DEFAULT_MODEL = "nvidia/nemotron-3-super-120b-a12b:free"

JUDGE_PROMPT = f"""Posuď, jestli vygenerovaný SQL odpovídá na otázku.

DATABÁZE SCHEMA:
{SCHEMA}

OTÁZKA UŽIVATELE:
{{question}}

VYGENEROVANÝ SQL:
{{generated}}

REFERENČNÍ SQL (správné řešení):
{{expected}}

VÝSLEDEK GENERATED SQL:
{{result}}

Kritéria:
1. Sémantika — odpovídá to na otázku?
2. Edge cases — NULL handling, status filter, ORDER BY
3. Smysluplnost — žádné latentní bugy

Skórování: 10 = perfektní · 7-9 = funguje · 4-6 = částečně · 0-3 = špatně.
PASS pokud score >= 7.
"""

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "sql_judgment",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "score":   {"type": "integer", "minimum": 0, "maximum": 10},
                "verdict": {"type": "string", "enum": ["PASS", "FAIL"]},
                "issues":  {"type": "array", "items": {"type": "string"}},
            },
            "required": ["score", "verdict", "issues"],
            "additionalProperties": False,
        },
    },
}


class SQLJudge:
    """LLM jako hodnotící agent — nezná raw DB, pracuje jen s textem."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._api_key = os.getenv("OPENROUTER_API_KEY")
        if not self._api_key:
            raise RuntimeError("OPENROUTER_API_KEY není nastaven.")

    def evaluate(
        self,
        question: str,
        generated: str,
        expected: str,
        result: str = "",
    ) -> dict:
        prompt = JUDGE_PROMPT.format(
            question=question,
            generated=generated,
            expected=expected,
            result=str(result)[:500] or "(SQL nebyl spuštěn)",
        )
        raw = None
        for attempt in range(5):
            try:
                with OpenRouter(api_key=self._api_key) as client:
                    response = client.chat.send(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        response_format=RESPONSE_FORMAT,
                    )
                raw = response.choices[0].message.content.strip()
                break
            except TooManyRequestsResponseError:
                time.sleep(2 ** attempt)   # 1, 2, 4, 8, 16 s
        if raw is None:
            raise RuntimeError("OpenRouter free tier vyčerpán po 5 pokusech.")
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"score": 0, "verdict": "FAIL", "issues": [f"Nevalidní JSON: {raw[:100]}"]}


if __name__ == "__main__":
    # Quick smoke test.
    verdict = SQLJudge().evaluate(
        question="Kolik je zákazníků?",
        generated="SELECT COUNT(*) FROM customers",
        expected="SELECT COUNT(*) FROM customers",
    )
    print(verdict)
