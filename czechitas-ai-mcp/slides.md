# APIs, agenti a SQL
## Jakub Kopecký, Engineer @ Apify
### Czechitas AI Workshop · 26.-27. 5. 2026

---

## Co nás čeká

**Den 1 - API + agenti**
1. Co je API - anatomie, metody, JSON, první call v Pythonu (Kuba)
2. LLM a coding agent - co to je, jak se liší od chatu (Kuba)
3. OpenCode hands-on - AGENTS.md, skills (Ilja)
4. Security a use cases - klíče, rizika, domácí úkol (Ilja)

**Den 2 - MCP + Evals**
1. Co je MCP ("USB-C pro AI") (Kuba)
2. Snowflake MCP hands-on (Tana)
3. **Report** z přirozeného jazyka ze Snowflake (Ilja)
4. SQL Quality Judge Evals - automatická evaluace Text-to-SQL (Kuba)

---

# Den 1 · API + agenti

---

## Co je internet?

Síť propojených počítačů.

🖥️ Tvůj počítač  ↔  🌐 Internet  ↔  🏢 Server

Tvůj browser, mobil, Snowflake server, ChatGPT - všechno běží jako počítače propojené sítí.

Kabely · Wi-Fi · satelity. Pod tím vším: miliardy zpráv letících mezi mašinami.

Tohle je playground, kde se odehraje celý workshop.

---

## Klient & Server

Na internetu existují **dvě role**:

🧑 **KLIENT** - kdo se ptá
   browser · mobilní apka · Python skript · AI agent

🏢 **SERVER** - kdo má data a logiku
   Snowflake · GitHub · OpenAI · czechitas.cz

Klient pošle **dotaz** → server vrátí **odpověď**.

99 % všeho, co se na internetu děje. I tenhle workshop.

---

## Co se stane, když klikneš na link

Klikneš na `https://czechitas.cz`:

1. 🖥️ Browser (**KLIENT**) pošle zprávu serveru
2. 🌐 Zpráva proletí Wi-Fi → router → ISP → kabely pod oceánem → datacentrum
3. 🏢 **SERVER** zprávu přečte → pošle zpět HTML
4. 🖥️ Browser HTML zobrazí

Trvá to ~100 ms. Děje se to **miliardkrát za sekundu**.

Aby si **KLIENT a SERVER** rozuměli, potřebují domluvený jazyk. → To je **API**.

---

## Co je API?

**API = prostředník mezi klientem a serverem.**

Klient nemluví se serverem přímo. Mluví s API - to ví, jak server používat a co s ním lze.

Ty → request → API → server
Server → response → API → ty

🍽️ Jako **číšník v restauraci**. Ty jen řekneš co chceš, on se postará o zbytek.

---

## Proč tě to zajímá?

Automatizace

Data, ke kterým se jinak nedostaneš

Všechno je API. Snowflake, GitHub, Slack, Mapy.cz

---

## Druhy API

Pod kapotou existuje víc protokolů:

| Typ | Použití | Stav |
|---|---|---|
| **REST / HTTP** | weby, mobilní apky, většina veřejných API | dnes ~90 % všeho |
| **SOAP** | starší enterprise systémy (banky, telco) | legacy, ale pořád běží |
| **GraphQL** | komplexní data, klient si vybírá co chce | roste (GitHub, Shopify) |
| **gRPC** | mikroslužby, vysoký výkon | interní, hojné v cloudu |
| **WebSocket** | live data, chat, real-time push | doplněk k HTTP |

V tomhle workshopu řešíme **HTTP/REST**.
Když se naučíš tohle, ostatní pochopíš za odpoledne.

---

## Co je HTTP?

**HyperText Transfer Protocol**

1991 · Tim Berners-Lee · CERN
Vznikl, aby si vědci mohli posílat dokumenty po síti.

Dnes na něm jede skoro všechno:
- Weby a mobilní apky
- API ke každé službě
- AI agenti a MCP servery

---

## HTTP vs HTTPS

**🔓 http://** - čte to každý router cestou. Browsery dnes označují jako "Not secure".

**🔒 https://** - šifrované TLS spojení. HTTP + zámek.

V praxi: vždycky https. http nikdy.
ChatGPT, banking, Snowflake - všechno https.

---

## Anatomie requestu

```
POST /api/v2/statements HTTP/1.1
Host: czechitas.snowflakecomputing.com    ← tvoje Snowflake URL
Authorization: Bearer eyJraWQ...          ← API klíč (JWT token)
Content-Type: application/json            ← posíláme JSON

{
"statement": "SELECT COUNT(*) FROM customers",
"warehouse": "MY_WH"
}                                         ← body (volitelné)
```


Tři části:
1. **Start line** - co chci a kde (`POST /v1/users`)
2. **Headers** - metadata (auth, content type, ...)
3. **Body** - data (jen u POST/PUT/PATCH; u GET nikdy)

---

## Co je JSON?

Ten `{...}` v body je **JSON** - textový formát pro data.
Vzdáleně příbuzný Python dictu.

```json
{
  "name": "Anna",
  "age": 28,
  "skills": ["Python", "SQL"],
  "active": true
}
```

- **Klíče** vždycky v uvozovkách
- **Hodnoty**: text, číslo, `true`/`false`, `null`, list, další dict
- Vnořování - list v dictu, dict v listu, jak chceš

API ho používají všude. V Pythonu `resp.json()` z něj udělá dict.

---

## URL - z čeho se skládá

```
https://api.example.com/v1/users?role=admin&limit=10
└─┬─┘   └──────┬──────┘└──┬───┘└────────┬────────┘
scheme    host          path     query string
```

- **scheme** - protokol, v praxi vždycky `https`
- **host** - doménové jméno serveru
- **path** - cesta k resource (`/v1/...` = verze API)
- **query** - parametry za `?` ve formátu `key=value&key=value`

V Pythonu `params={"role": "admin", "limit": 10}` to složí za tebe.

---

## HTTP metody

| Metoda | CRUD | Co dělá | Má body? | Příklad |
|---|---|---|---|---|
| `GET` | **R**ead | čte data | ne | Načti seznam uživatelů |
| `POST` | **C**reate | vytváří | ano | Zaregistruj uživatele |
| `PUT` | **U**pdate | nahradí celé | ano | Přepiš celý profil |
| `PATCH` | **U**pdate | upraví část | ano | Změň jen email |
| `DELETE` | **D**elete | smaže | ne | Zruš účet |

Mapuje se 1:1 na SQL CRUD - co už znáš ze Snowflake.

V praxi: 90 % requestů je `GET` + `POST`.

---

## Status kódy

První číslo říká kategorii:

| Rozsah | Význam | Časté kódy |
|---|---|---|
| `2xx` | ✅ OK | `200` OK · `201` Created · `204` No Content |
| `3xx` | ↪️ Přesměrování | `301` Moved · `304` Not Modified |
| `4xx` | ❌ Tvoje chyba | `400` Bad Request · `401` Unauthorized · `403` Forbidden · `404` Not Found · `429` Too Many Requests |
| `5xx` | 💥 Chyba serveru | `500` Internal Error · `502` Bad Gateway · `503` Unavailable |

**4xx oprav ty, 5xx napiš adminovi.**

---

## Status code historky

**🫖 418 · I'm a teapot**
Z roku 1998 - dubnový žert. Server: "Jsem konvice, nedělám kafe."
Cloudflare ho dnes používá na blokované requesty.

**🚦 429 · Too Many Requests**
"Zpomal!" Když píšeš smyčku bez `sleep()`.

**💥 503 · Service Unavailable**
"Jsme rozbití, zkus za chvíli." Black Friday classic.

---

## HTTP v akci

```
GET /v1/forecast?latitude=50.08&longitude=14.42&current=temperature_2m HTTP/1.1
Host: api.open-meteo.com
```

```
HTTP/1.1 200 OK
Content-Type: application/json

{
  "latitude": 50.08,
  "longitude": 14.42,
  "current": {
    "time": "2026-05-26T18:00",
    "temperature_2m": 18.3
  }
}
```

---

## Setup

Potřebuješ Python + jednu knihovnu:

```bash
pip install --user requests
```

`--user` = nainstaluje to do tvého home adresáře, ne do systému.

**Backup: Google Colab**

https://colab.research.google.com

Otevřeš v prohlížeči. `requests` je tam už předinstalovaný.
Žádný terminál, žádný setup. Skript spustíš tlačítkem ▶.

---

## Tvůj první API call

```python
import requests

resp = requests.get(
    "https://api.open-meteo.com/v1/forecast",
    params={
        "latitude":  50.08,  # Praha
        "longitude": 14.42,
        "current":   "temperature_2m,wind_speed_10m",  # teplota 2 metry nad zemí, rychlost větru 10 metrů nad zemí
    },
)

print(resp.json())
# {'current': {'temperature_2m': 18.3, 'wind_speed_10m': 12.4}, ...}
```

💡 Stejně funguje browser - dostaneš stejný JSON.
Browser pošle `GET` request, stejně jako `requests.get`.

https://api.open-meteo.com/v1/forecast?latitude=50.08&longitude=14.42&current=temperature_2m,wind_speed_10m

---

## Free APIs na hraní

Žádná registrace, žádný klíč. Zkus doma:

- 🌤️ **Počasí** - open-meteo.com
- 🐱 **Kočka** - thecatapi.com
- 🎴 **Karty** - deckofcardsapi.com
- 🌍 **Země** - restcountries.com

Začni s tím, co tě baví. Princip je všude stejný.

---

## Co hlídat

- Rate limiting - kolik requestů za minutu/hodinu (jinak dostaneš status code `429`)
- Timeout - `requests.get(..., timeout=10)`, nikdy bez něj
- Dokumentace - jaké endpointy, parametry, formát dat

---

## Agenti

---

## Co je LLM?

Pravděpodobnostní model natrénovaný na obřím množství textu (knihy, web, kód, ...) - rozumí jazyku a generuje text.

Známé LLM:
- **Claude** (Anthropic)
- **GPT-4 / GPT-5** (OpenAI)
- **Gemini** (Google)
- **Llama** (Meta, open-source)

**Mentální model:** LLM jako komprimovaný soubor.
~5 GB váhy (jako jeden film) → značná část toho, co lidstvo napsalo.

LLM sám o sobě jen mluví. Coding agent = LLM s rukama.

---

## Jak LLM mluví

LLM = **předpovídá další slovo**. Spočítá pravděpodobnost každého možného slova.

```
"Praha je hlavní město ____"

LLM spočítá pravděpodobnosti:
  "České"    87%
  "Česka"     8%
  "Evropy"    3%
  "krásné"    1%

→ vybere "České"
→ opakuje: "České republiky."
```

Slovo po slově. Loop končí, když LLM vybere **speciální značku konce** - to znamená "konec, hotovo".

---

## Co LLM neumí

- ❌ Nezná, co se stalo po datu trénování (cutoff cca 2024)
- ❌ Vymyslí si autora, URL, citaci - sebevědomě a špatně (**halucinace**)
- ❌ Špatně počítá pod tlakem (math errors)
- ❌ Nezná tvoje data, dokud mu je nedáš

Vždycky ověřuj zdroje. Hlavně URL a citace.

---

## Tokeny a kontext

1 token ≈ 4 znaky / 0.75 slova

```
"Praha"            = 1 token
"Czechitas"        = 3 tokeny
"😂"                = 1 token
```

**Context window** = kolik tokenů LLM "vidí" najednou:
- Claude Opus 4.7: **1 000 000** tokenů (~1 500 stran textu)
- GLM 5.1: **203 000** tokenů

Když ti agent zapomene, došlo místo v **context window** - ne output tokeny.

---

## Co je agent?

LLM sám neumí nic - jen mluvit.

**Agent = LLM + nástroje (tools).**

Nástroj = funkce, kterou LLM může zavolat:
- 🌐 **Web** - vyhledávač, stažení stránky
- 🐍 **Kód** - Python runtime, spustit skript
- 📁 **Soubory** - file system, číst, psát
- 🗜️ **Data** - databáze, API, e-mail

Loop: LLM vybere nástroj → runtime ho spustí → výsledek se vrátí LLM → LLM pokračuje.

Tak se z mluvy stane akce.

---

## Co je coding agent?

Autocomplete → doplní řádek
Chat → odpoví na otázku
**Agent → udělá práci**

**Coding agent = LLM specializovaný na kód.**
- Trénovaný i na obřím množství kódu (GitHub, dokumentace)
- Speciální nástroje pro práci s projektem: `read`, `edit`, `bash`, `grep`, `glob`

Není to chatbot. Je to kolega, který tu práci doopravdy udělá.

---

## Co všechno vidí (a umí)

Agent má v pracovní složce přístup k:

- **Soubory** - čte, edituje, vytváří, maže
- **Terminál** - spustí jakýkoliv `bash` příkaz
- **Internet** - `curl`, `pip install`, stažení dat z URL
- **MCP servery** - připojené nástroje a datové zdroje (Snowflake, GitHub, ... zítra víc)

(Cokoliv) co umíš, umí i on. Ale má omezenou paměť a nemá duši - a tudíž vkus.
Stáhnout knihovnu, smazat složku, poslat HTTP request, dotázat se databáze...

---

## Jak to vypadá v praxi

```
You: Napiš mi skript co vytáhne data z Weather API,
      uloží to do CSV, a udělá z toho graf teplot
      za posledních 7 dní.

Agent:
  1. Píše Python skript
  2. Spouští ho
  3. Vidí chybu → opravuje
  4. Spouští znovu
  5. Hotovo. Tady máš graph.png
```

Loop: write → run → read output → fix

---

## Coding agent ⚡

Hands-on

---

# Den 2 · MCP + Evals

---

## Co je MCP?

Model Context Protocol

"USB-C pro AI"

Jeden standard. Připojíš agenta k:
- Databázi
- API
- Souborům
- GitHubu
- ...čemukoliv

Bez custom kódu pro každou integraci.

---

## Před MCP

```
Agent → custom kód → Snowflake
Agent → custom kód → GitHub
Agent → custom kód → Slack
Agent → custom kód → ...
```

N×M integrací. Každá jiná. Každou musíš psát.

---

## Po MCP

```
Agent → MCP ← Snowflake
       MCP ← GitHub
       MCP ← Slack
       MCP ← ...
```

1 protokol. N serverů. Agent se připojí ke všem stejně.

---

## Jak MCP funguje

```
┌────────┐     JSON-RPC      ┌─────────────┐
│ Agent  │ ←───────────────→ │ MCP Server   │
│ (host) │   tools/list      │ (Snowflake)  │
│        │   tools/call      │              │
└────────┘                   └─────────────┘
```

- Agent se zeptá: "Co umíš?" → server vrátí seznam tools
- Agent zavolá: "Spusť SQL query" → server provede, vrátí výsledek
- Transport: stdio (lokálně) nebo HTTP (vzdáleně)

Stejný pattern pro všechno.

---

## Co MCP nabízí (primitives)

MCP server může klientovi nabídnout **3 věci**:

| Primitive | Co to je | Kdo to spouští |
|---|---|---|
| **🔧 Tools** | funkce, které agent volá (`execute_query(...)`) | model |
| **📄 Resources** | data, která agent čte (tabulka, dokument) | app |
| **💬 Prompts** | připravené šablony příkazů (slash commands) | uživatel |

**Tools jsou nejčastější.** Většina MCP serverů dnes nabízí primárně je.

---

## Reálné MCP servery

Pár populárních z ekosystému 2026:

- 📊 **Snowflake** - SQL přes přirozený jazyk
- 🐙 **GitHub** - PRs, issues, code search
- 🕷️ **Apify** - tisíce scraperů na web data
- 🎭 **Playwright** - browser automation
- 💬 **Slack** - posílání zpráv, hledání
- 📁 **Filesystem** - lokální soubory

Ekosystém má přes **17 000 serverů**. Najdeš na `smithery.ai` · `mcp.so` · `pulsemcp.com`.

---

## Local vs remote

Dva způsoby, jak se klient (agent) připojí k MCP serveru:

**🖥️ STDIO** - lokální proces
- Spouští se jako subprocess
- Komunikace přes `stdin` / `stdout`
- `npx`, `python`, binárka

**🌐 HTTP** - vzdálený endpoint (URL)
- Sdílený, škálovatelný
- Auth přes OAuth
- `mcp.apify.com`

Pro začátek: **stdio**. Když potřebuješ sdílení nebo škálu: **HTTP**.

---

## Postav si vlastní MCP server

30 řádků Pythonu. Stačí.

```python
from mcp.server.fastmcp import FastMCP

app = FastMCP("my-tools")

@app.tool()
def add(a: int, b: int) -> int:
    """Sečte dvě čísla."""
    return a + b

@app.tool()
def get_weather(city: str) -> str:
    """Vrátí počasí pro město."""
    return fetch_weather(city)

app.run()
```

Docstring popisuje, co tool dělá - LLM si ho přečte a rozhodne, kdy ho použít.

**Tvoje API se stane MCP serverem v jednom odpoledni.**

---

## Snowflake MCP ⚡

Hands-on

---

## Evals ⚖️

Důvěřuj, ale ověřuj.

---

## Jak se testuje software

**Bez testů:** spustíš a hledáš co nefunguje ručně.
**S testy:** spustíš `pytest`, automaticky se to ověří.

**Tři úrovně testů:**

- 🧱 **Unit** — testuje jednu funkci. Rychlé. Píšeš jich hodně.
- 🔗 **Integration** — testuje že komponenty mluví spolu. Středně rychlé.
- 🌐 **End-to-end** — testuje celou aplikaci jako uživatel. Pomalé.

Začneme s **unit testy**.

---

## Unit test — příklad

```python
# Funkce, kterou testuješ:
def cena_s_dph(cena: float, sazba: float = 0.21) -> float:
    return cena * (1 + sazba)

# Test:
def test_cena_s_dph():
    assert cena_s_dph(100) == 121
    assert cena_s_dph(100, 0.10) == 110
    assert cena_s_dph(0) == 0

# Spustíš:
$ pytest
test_cena_s_dph PASSED ✅
```

Stejný vstup → stejný výstup. **Deterministicky.**

---

## Integration & E2E — výhled

🔗 **Integration** — testuje že komponenty fungují spolu (např. funkce + databáze):

```python
def test_zaloz_objednavku():
    order_id = vytvor_objednavku(db, customer_id=1)
    assert db.find_order(order_id) is not None
```

🌐 **End-to-end** — testuje aplikaci jako uživatel (browser):

```python
def test_objednavka():
    page.goto("/eshop")
    page.click("Objednat")
    assert "/dekujeme" in page.url
```

Princip stejný jako unit test — `assert` na očekávaný výsledek. Jen testuješ víc kódu najednou.

---

## Jak ale testovat AI?

```python
# Unit test:
assert secti(2, 3) == 5     # vždycky 5 ✓

# AI agent:
agent.dotaz("Kolik mám zákazníků?")
→ "Máte 10 zákazníků."           # pondělí
→ "10 zákazníků máte v DB."     # úterý
→ "Celkem 10 customers."         # středa
```

Stejná otázka. **Tři různé odpovědi. Všechny správně.**

Jak napíšeš `assert`?

→ Potřebuješ jiný nástroj. **To je eval.**

---

## Co je eval?

**Eval = automatický test kvality AI výstupu.**

- Místo **PASS / FAIL** → skóre (0–10) nebo PASS / FAIL
- Místo *„kód funguje“* → *„agent dělá dobrou práci“*

Měříš jak dobré to je, ne jen jestli to nepadá.

---

## Test vs Eval

|  | Unit test | Eval |
|---|---|---|
| **Cíl** | správnost | kvalita |
| **Výstup** | PASS / FAIL | skóre |
| **Determinismus** | stejný vstup = stejný výstup | různý výstup každý run |
| **Rychlost** | milisekundy | sekundy (LLM call) |
| **Cena** | zdarma | $0.001 – $0.10 / call |
| **Co testuje** | funkci | model + prompt + data |

Test ti řekne: *"kód funguje."*
Eval ti řekne: *"agent dělá dobrou práci."*

---

## Z čeho se eval skládá

- 🗂️ **Test dataset** — sada vstupů s očekávanou odpovědí (otázka → reference SQL)
- 🤖 **Generator** — tvůj agent / LLM (otázka → vygenerovaný SQL)
- 📏 **Metrika** — jak měřit shodu (string · result · LLM judge)
- 📊 **Agregace** — souhrn napříč případy (% pass · průměrné skóre)

100 otázek + agent + metrika → **"87 % správně"**.

---

## Proč to stavět?

| Metrika | Bez evaluace | S evaluací |
|---|---|---|
| Víš jak dobrý je výstup? | Ne | Ano |
| Můžeš iterovat? | Metodou pokus-omyl | Data-driven |
| Bezpečnost | "Snad to nic nerozbije" | Chytneš to předem |

Evaly ti řeknou pravdu o tvém agentovi — žádný jiný způsob to neudělá.

---

## SQL Quality Judge

Problém: AI generuje SQL. Je správné?

Data tým používá Cortex / ChatGPT na SQL.
Jak ověříš, že výstup je OK?

Manuálně? Neškáluje.
Nedělat nic? Risk.

→ **Postavíme automatického grader.**

---

## Level 1 · String match

Otázka: *"Kolik zákazníků je z Prahy?"*

```python
generated = "SELECT COUNT(*) FROM customers WHERE city = 'Praha'"
expected  = "SELECT COUNT(*) FROM customers WHERE city = 'Praha'"

assert generated == expected
```

✅ Chytí: identické query

❌ Mine: `... WHERE city='praha'...` (lowercase, jiné mezery)
❌ Mine: `SELECT COUNT(customer_id) FROM customers WHERE ...` (jiný COUNT, sedí)
❌ Mine: přeházené podmínky

K ničemu v reálu.

---

## Level 2 · Result match

Spustíme oba SQL a porovnáme výstup.

```python
generated_result = run_sql(generated_sql)
expected_result  = run_sql(expected_sql)
# např. [(4,)]   — 4 zákazníci z Prahy

assert generated_result == expected_result
```

✅ Chytí: query vracející stejná data ve stejných sloupcích
✅ Odolné: formátování, aliasy, pořadí řádků

❌ Mine: extra sloupec navíc v SELECT nebo jiné pořadí sloupců
❌ Mine: latentní bug — query vrátí správný výsledek náhodou (např. `SELECT * FROM products LIMIT 5`)

---

## Level 3 · LLM as judge

```python
judge = SQLJudge()
verdict = judge.evaluate(question, generated, expected, result)

# → {"score": 8, "verdict": "PASS",
#     "issues": ["chybí ORDER BY", "extra sloupec product_id"]}
```

✅ Chytí sémantiku, code smells, edge cases - chápe otázku
⚠️ Nedeterministický, pomalejší, dražší

---

## SQL Quality Judge ⚡

Hands-on

---

## Co jsme se naučili

**Den 1**
- 🌐 **API** - HTTP, request/response, JSON
- 🐍 První API call v Pythonu
- 🧠 **LLM** = jazyk · **agent** = ruce
- 📄 `AGENTS.md` - kontext pro agenta
- 🔐 Secrets, approve/deny, bezpečnost

**Den 2**
- 🔌 **MCP** propojí agenta s daty
- 📊 Přirozený jazyk → SQL přes Snowflake
- ⚖️ **Evaly** - automatická kontrola kvality

**API → Agent → MCP → Evals.** Loop se uzavírá.

---

## 🔗

[linkedin.com/in/doas-jakub-kopecky](https://www.linkedin.com/in/doas-jakub-kopecky/)

---


