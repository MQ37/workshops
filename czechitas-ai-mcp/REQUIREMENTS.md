# Requirements

Připrav si před workshopem. Všechny příkazy běží v terminálu.

## 1. Python 3.10+

Ověř, že máš Python:

```bash
python3 --version
```

**Silně doporučuju lokálně.** Cloud backup (Google Colab) jen v krajním případě.

- macOS / Linux — `brew install python` / `apt install python3`
- Windows — [python.org/downloads](https://www.python.org/downloads/) (zaškrtni *Add Python to PATH*)

Pak doinstaluj 2 Python knihovny (`pip` = Python balíčkovač):

```bash
pip install --user requests openrouter
```

## 2. OpenRouter API klíč

OpenRouter je jeden účet, stovky AI modelů.

1. Účet na [openrouter.ai](https://openrouter.ai) (Google/GitHub login)
2. Klíč na [openrouter.ai/keys](https://openrouter.ai/keys) — **ulož si ho, vidíš ho jen jednou**

Free tier obvykle stačí. **Doporučuju dobít $3–5** pro případ rate limitu během workshopu.

## 3. Editor

Cokoliv s Python podporou. Tip: [VS Code](https://code.visualstudio.com).
