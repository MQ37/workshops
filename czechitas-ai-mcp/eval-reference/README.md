# SQL Quality Judge — reference implementation

A 3-level evaluation pipeline for a text-to-SQL agent:

- **Level 1** · string match
- **Level 2** · result match (run both SQLs against SQLite, compare data)
- **Level 3** · LLM-as-judge (score 0–10 + verdict + issues)

No MCP, no cloud DB. Local SQLite + LLM via OpenRouter.

---

## 🚀 Easiest way to run — Google Colab

Open [`sql_quality_judge.ipynb`](./sql_quality_judge.ipynb) in
[Google Colab](https://colab.research.google.com):

1. Upload the notebook (`File → Upload notebook`) or open it directly from
   GitHub.
2. Add `OPENROUTER_API_KEY` to Colab Secrets — click the 🔑 in the left
   sidebar, paste your key from [openrouter.ai/keys](https://openrouter.ai/keys).
3. Run all cells (`Runtime → Run all`).

The notebook is **interactive** — text input for ad-hoc questions, a
"Run eval" button with a live progress bar, side-by-side diffs when string
match fails, etc. All built with `ipywidgets`, no marimo dependency at
runtime.

---

## 💻 Run locally (CLI)

```bash
# 1. Dependencies (Python 3.10+)
pip install --user openrouter

# 2. API key
export OPENROUTER_API_KEY=sk-or-...

# 3. Build the SQLite DB with dummy data
python populate_db.py

# 4. Run the eval
python eval.py
```

Whole run takes ~45 seconds for 12 test cases.

### Expected output

```
⚖️  SQL Quality Judge — 12 test cases

[ 1/12] Kolik máme zákazníků celkem?
        L1 string ❌  L2 result ✅  L3 judge ✅ 10/10
[ 2/12] Kolik zákazníků je z Prahy?
        L1 string ❌  L2 result ✅  L3 judge ✅ 10/10
...

═══════════════════════════════════════════════
  Level 1 (string match):    0 / 12  (  0 %)
  Level 2 (result match):    9 / 12  ( 75 %)
  Level 3 (LLM as judge):   12 / 12  PASS · avg 9.5 / 10
═══════════════════════════════════════════════
```

**What it shows:**

- **L1 ≈ 0 %** — string match never works in real life. The agent always
  formats SQL slightly differently from the reference.
- **L2 ≈ 70–90 %** — functional equivalence catches most cases but misses
  some (extra columns in SELECT, different column order).
- **L3 ≈ 100 % PASS** — the LLM judge picks up semantic nuances and gives
  verbal feedback (*"missing ORDER BY for deterministic ordering"*,
  *"extra column product_id"*).

---

## 📁 Files

| File | Purpose |
|---|---|
| `schema.sql` | Definition of 4 tables (single source of truth) |
| `populate_db.py` | Creates `eshop.sqlite` — 10 customers · 10 products · 15 orders · 20 items |
| `agent.py` | `SQLAgent` — LLM + schema in system prompt → generates SQL |
| `judge.py` | `SQLJudge` — LLM as judge, returns `{score, verdict, issues}` |
| `test_cases.py` | 12 `(question, reference_sql)` tuples |
| `eval.py` | Runner: agent + 3 levels + summary table |
| `sql_quality_judge.ipynb` | Self-contained interactive Colab notebook (all of the above in one file) |
| `requirements.txt` | Just `openrouter>=0.9.1` |

The notebook and the `.py` files share the same prompts, schemas, model,
and test cases — they're functionally equivalent.

---

## ⚙️ Customization

- **Different model** — change `DEFAULT_MODEL` in `agent.py` / `judge.py`
  (or in the notebook cells). Browse models at <https://openrouter.ai/models>.
- **More test cases** — append to `test_cases.py` (or `TEST_CASES` in the
  notebook). Each reference SQL must run against `eshop.sqlite`.
- **Different dataset** — edit `populate_db.py`. Data is plain Python lists
  of tuples.

---

## 🗄️ E-shop schema

```
customers   (customer_id, name, email, city, country, signup_date)
products    (product_id, name, category, price, stock_qty)
orders      (order_id, customer_id, order_date, status, total_amount)
order_items (order_item_id, order_id, product_id, quantity, unit_price)
```

Full schema in [`schema.sql`](./schema.sql).

---

## ⚠️ Free tier note

Default model is `nvidia/nemotron-3-super-120b-a12b:free` via OpenRouter.
Free tier has a per-minute rate limit (~20 req/min) — the CLI eval has
retry logic with exponential backoff, but if you hit a daily quota you'll
need to wait or switch to a paid model. The notebook doesn't retry — re-run
the eval cell if it fails.

A few dollars of credit on OpenRouter avoids all of this.
