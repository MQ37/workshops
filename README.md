# Workshops

Materials from technical workshops I run — slides, demos, hands-on notebooks.

Each workshop lives in its own directory with its own README, requirements, and
runnable code. Most slides are HTML decks you can open straight in a browser.

---

## 📚 Workshops

### [`czechitas-ai-mcp/`](./czechitas-ai-mcp/)

> 🇨🇿 **Slides, code comments, print messages, and LLM prompts are in Czech** (audience is Czech). Function / variable names follow Python conventions in English.

A 2-day intro to **APIs, AI agents, MCP, and evals** for the Czechitas community.
Covers HTTP/REST basics, what LLMs actually are, how coding agents work, the
Model Context Protocol ecosystem, and a hands-on **SQL Quality Judge** —
a 3-level evaluation pipeline for text-to-SQL agents (string match · result
match · LLM-as-judge).

| Where | What |
|---|---|
| [`slides.md`](./czechitas-ai-mcp/slides.md) | Source of truth — all slide content in Markdown |
| [`dist/index.html`](./czechitas-ai-mcp/dist/index.html) | Hand-crafted standalone HTML deck (dark theme, keyboard-driven) |
| [`REQUIREMENTS.md`](./czechitas-ai-mcp/REQUIREMENTS.md) | What attendees need to install before the workshop |
| [`eval-reference/`](./czechitas-ai-mcp/eval-reference/) | Working reference implementation: SQL agent + LLM-as-judge + 3 metrics, all in ~100 lines of Python |
| [`eval-reference/sql_quality_judge.ipynb`](./czechitas-ai-mcp/eval-reference/sql_quality_judge.ipynb) | Google-Colab-ready interactive notebook for the eval hands-on |

**Running the deck.** Open `czechitas-ai-mcp/dist/index.html` in any modern
browser. Arrow keys / Space / Page Up / Page Down / F (fullscreen) for navigation.

**Running the eval reference.** Either:
- Open the notebook directly in [Google Colab](https://colab.research.google.com) — needs an `OPENROUTER_API_KEY` secret
- Or run locally — see [`eval-reference/README.md`](./czechitas-ai-mcp/eval-reference/README.md)

---

## 🛠️ Tech notes

- **Slides** are hand-rolled HTML + CSS, no slide framework. Single self-contained
  file, dark "tactical" theme, inline SVG diagrams. Designed to be hackable —
  every slide is a `<section class="slide">` you can edit in any text editor.
- **Eval reference** uses [OpenRouter](https://openrouter.ai) as the LLM gateway
  (one API key → access to 300+ models) and SQLite for the dummy e-shop dataset.
  Default model is a free tier with `nemotron-3-super-120b` as fallback.
- **No build step.** Everything in this repo runs as-is.

