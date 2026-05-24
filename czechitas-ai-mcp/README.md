# Czechitas · AI / MCP / Evals Workshop

> 🇨🇿 **Slide content is in Czech.** The code, file structure, and this README are in English.

A 2-day intro to APIs, AI agents, the Model Context Protocol (MCP), and
LLM evaluation — for the [Czechitas](https://czechitas.cz) community.

**26.–27. 5. 2026 · 18:00–20:00**

---

## 📚 What's covered

**Day 1 — APIs + agents**

1. What is an API — HTTP, JSON, methods, first call in Python
2. LLMs and coding agents — what they are, how they differ from chat
3. OpenCode hands-on — AGENTS.md, skills
4. Security and use cases — keys, risks, homework

**Day 2 — MCP + Evals**

1. What is MCP ("USB-C for AI")
2. Snowflake MCP hands-on
3. Report from natural language over Snowflake
4. **SQL Quality Judge** — automated evaluation of text-to-SQL agents

---

## 📁 Repository contents

| Path | What |
|---|---|
| [`slides.md`](./slides.md) | Source of truth — all slide content in Markdown |
| [`dist/index.html`](./dist/index.html) | Hand-rolled standalone HTML deck (dark theme, keyboard-driven) |
| [`REQUIREMENTS.md`](./REQUIREMENTS.md) | What attendees need to install before the workshop |
| [`eval-reference/`](./eval-reference/) | Working SQL Quality Judge implementation — see its [README](./eval-reference/README.md) |
| [`eval-reference/sql_quality_judge.ipynb`](./eval-reference/sql_quality_judge.ipynb) | Google-Colab-ready interactive notebook for the eval hands-on |

---

## ▶️ How to run

### Open the slide deck

Just open `dist/index.html` in any modern browser. No build step, no
dependencies. Keyboard navigation:

- `→` / `Space` / `Page Down` — next slide
- `←` / `Page Up` — previous slide
- `Home` / `End` — first / last slide
- `F` — toggle fullscreen
- `#42` in the URL — jump to slide 42

### Run the SQL Quality Judge eval

**Easiest** — open [`eval-reference/sql_quality_judge.ipynb`](./eval-reference/sql_quality_judge.ipynb)
in [Google Colab](https://colab.research.google.com). Add your
`OPENROUTER_API_KEY` to Colab Secrets (🔑 in the left sidebar) and run all
cells.

**Locally** — see [`eval-reference/README.md`](./eval-reference/README.md)
for a CLI-based workflow.

---

## 🧱 Stack notes

- **Slides**: hand-rolled HTML + CSS, no slide framework. Single
  self-contained file, dark "tactical" theme, inline SVG diagrams.
  Every slide is a `<section class="slide">` you can edit in any text editor.
- **Eval reference**: ~100 lines of Python, [OpenRouter](https://openrouter.ai)
  as the LLM gateway (one API key → 300+ models), SQLite for the dummy
  e-shop dataset, structured JSON output via `response_format: json_schema`.

