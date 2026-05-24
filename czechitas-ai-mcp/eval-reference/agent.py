"""
SQLAgent — generuje SQL z přirozeného jazyka pomocí LLM přes OpenRouter.

Žádné MCP, žádné DB tools. Agent vidí pouze schema vložené do system
promptu a vrátí strukturovaný JSON s SQL polem. Strict json_schema =
žádné markdown wrappery, žádný extra text.

Použití:
    from agent import SQLAgent
    sql = SQLAgent().generate("Kolik zákazníků je z Prahy?")

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

SYSTEM_PROMPT = f"""Jsi SQL agent pro SQLite e-shop databázi.

DATABÁZE SCHEMA:
{SCHEMA}

Pravidla:
- Vrať JSON s jediným polem "sql" obsahujícím čistý SQL query.
- SQLite syntax (pro datum: strftime, LIKE '2024%').
- Tabulky a sloupce použij přesně jak jsou ve schéma (lowercase).
"""

RESPONSE_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "sql_query",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {
                "sql": {"type": "string"},
            },
            "required": ["sql"],
            "additionalProperties": False,
        },
    },
}


class SQLAgent:
    """LLM + schema v system promptu = SQL generator."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._api_key = os.getenv("OPENROUTER_API_KEY")
        if not self._api_key:
            raise RuntimeError("OPENROUTER_API_KEY není nastaven.")

    def generate(self, question: str) -> str:
        for attempt in range(5):
            try:
                with OpenRouter(api_key=self._api_key) as client:
                    response = client.chat.send(
                        model=self.model,
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": question},
                        ],
                        response_format=RESPONSE_FORMAT,
                    )
                raw = response.choices[0].message.content.strip()
                return json.loads(raw)["sql"].strip()
            except TooManyRequestsResponseError:
                time.sleep(2 ** attempt)   # 1, 2, 4, 8, 16 s
        raise RuntimeError("OpenRouter free tier vyčerpán po 5 pokusech.")


if __name__ == "__main__":
    # Quick smoke test.
    sql = SQLAgent().generate("Kolik máme zákazníků?")
    print(sql)
