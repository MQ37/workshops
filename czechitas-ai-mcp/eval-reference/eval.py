"""
eval.py — spustí kompletní SQL Quality Judge pipeline.

Pro každý test case:
  1. SQLAgent vygeneruje SQL z otázky (LLM call).
  2. Level 1: string match s referenčním SQL.
  3. Level 2: spustí oba SQL na SQLite a porovná výsledky.
  4. Level 3: LLM-as-judge posoudí kvalitu (LLM call).

Výstup: progress každého case + finální tabulka.

Spuštění:
    export OPENROUTER_API_KEY=sk-or-...
    python populate_db.py    # vytvoří eshop.sqlite (jednou)
    python eval.py
"""

import sqlite3
from pathlib import Path

from agent import SQLAgent
from judge import SQLJudge
from test_cases import TEST_CASES

DB_PATH = Path(__file__).parent / "eshop.sqlite"


def run_sql(sql: str, conn: sqlite3.Connection) -> list:
    """Spustí SQL a vrátí výsledek jako sortable list."""
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    # Seřadíme deterministicky — Level 2 nesmí selhat na ORDER mismatch.
    return sorted([tuple(r) for r in rows], key=str)


def string_match(generated: str, expected: str) -> bool:
    """Level 1: normalizovaný string match (case + whitespace insensitive)."""
    norm = lambda s: " ".join(s.lower().split())
    return norm(generated) == norm(expected)


def result_match(
    generated: str, expected: str, conn: sqlite3.Connection
) -> tuple[bool, str]:
    """Level 2: spustí oba SQL a porovná výsledky. Vrací (passed, raw_result)."""
    try:
        gen_result = run_sql(generated, conn)
        exp_result = run_sql(expected, conn)
        return gen_result == exp_result, str(gen_result)[:200]
    except Exception as e:
        return False, f"ERROR: {e}"


def _oneline(sql: str) -> str:
    """Složí víceřádkový SQL do jednoho řádku pro čitelný diff."""
    return " ".join(sql.split())


def main() -> None:
    if not DB_PATH.exists():
        raise SystemExit("Database not found. Spusť: python populate_db.py")

    agent = SQLAgent()
    judge = SQLJudge()
    conn = sqlite3.connect(DB_PATH)

    n = len(TEST_CASES)
    print(f"\n⚖️  SQL Quality Judge — {n} test cases\n")

    results = []
    for i, (question, expected_sql) in enumerate(TEST_CASES, 1):
        print(f"[{i:2d}/{n}] {question}")

        generated_sql = agent.generate(question)
        l1 = string_match(generated_sql, expected_sql)
        l2, gen_result = result_match(generated_sql, expected_sql, conn)
        l3 = judge.evaluate(question, generated_sql, expected_sql, gen_result)

        l1_icon = "✅" if l1 else "❌"
        l2_icon = "✅" if l2 else "❌"
        l3_icon = "✅" if l3.get("verdict") == "PASS" else "❌"
        print(
            f"        L1 string {l1_icon}  L2 result {l2_icon}  "
            f"L3 judge {l3_icon} {l3.get('score', 0)}/10"
        )
        if not l1:
            # Show why string match failed.
            print(f"            generated: {_oneline(generated_sql)}")
            print(f"            expected:  {_oneline(expected_sql)}")
        if not l2:
            # Show actual result diff.
            print(f"            got:    {gen_result[:120]}")
        for issue in l3.get("issues", []) or []:
            print(f"            └─ {issue}")

        results.append(
            {
                "question": question,
                "generated": generated_sql,
                "l1": l1,
                "l2": l2,
                "l3_score": l3.get("score", 0),
                "l3_verdict": l3.get("verdict", "FAIL"),
            }
        )

    conn.close()

    # Souhrn
    l1_pass = sum(r["l1"] for r in results)
    l2_pass = sum(r["l2"] for r in results)
    l3_pass = sum(r["l3_verdict"] == "PASS" for r in results)
    l3_avg = sum(r["l3_score"] for r in results) / n

    bar = "═" * 47
    print(f"\n{bar}")
    print(f"  Level 1 (string match):   {l1_pass:>2d} / {n}  ({l1_pass * 100 // n:>3d}%)")
    print(f"  Level 2 (result match):   {l2_pass:>2d} / {n}  ({l2_pass * 100 // n:>3d}%)")
    print(f"  Level 3 (LLM as judge):   {l3_pass:>2d} / {n}  PASS · avg {l3_avg:.1f}/10")
    print(bar)


if __name__ == "__main__":
    main()
