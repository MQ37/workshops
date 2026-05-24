"""
populate_db.py — vytvoří SQLite databázi e-shopu s dummy daty pro evals.

Spuštění:
    python populate_db.py

Vytvoří soubor eshop.sqlite vedle skriptu. Existující přepíše.

Schema (4 tabulky, ≤ 20 řádků každá):
    customers     — 10 zákazníků (Praha, Brno, Ostrava, Plzeň, Bratislava, Vienna)
    products      — 10 produktů (Electronics, Books, Clothing, Home)
    orders        — 15 objednávek 2024 (completed / cancelled / pending)
    order_items   — 20 položek (váží orders × products)

Sanity: SUM(order_items.qty * unit_price) == SUM(orders.total_amount)
"""

import sqlite3
from pathlib import Path

HERE = Path(__file__).parent
DB_PATH = HERE / "eshop.sqlite"
SCHEMA_PATH = HERE / "schema.sql"

CUSTOMERS = [
    # (customer_id, name, email, city, country, signup_date)
    (1,  "Anna Nováková",       "anna.novakova@email.cz",  "Praha",      "CZ", "2024-01-15"),
    (2,  "Petr Svoboda",        "petr.svoboda@email.com",  "Brno",       "CZ", "2024-02-20"),
    (3,  "Markéta Procházková", "mp@mail.cz",              "Ostrava",    "CZ", "2024-03-10"),
    (4,  "Tomáš Dvořák",        "tomas.d@gmail.com",       "Praha",      "CZ", "2024-04-05"),
    (5,  "Eva Černá",           "eva.cerna@email.cz",      "Plzeň",      "CZ", "2024-05-12"),
    (6,  "Jan Horák",           "jan.horak@example.com",   "Bratislava", "SK", "2024-06-18"),
    (7,  "Hana Veselá",         "h.vesela@mail.cz",        "Praha",      "CZ", "2024-07-22"),
    (8,  "Michael Krejčí",      "mkrejci@gmail.com",       "Vienna",     "AT", "2024-08-30"),
    (9,  "Lucie Marešová",      "lucie.maresova@email.cz", "Brno",       "CZ", "2024-09-14"),
    (10, "David Pokorný",       "d.pokorny@example.com",   "Praha",      "CZ", "2024-10-08"),
]

PRODUCTS = [
    # (product_id, name, category, price, stock_qty)
    (1,  "Laptop Lenovo X1",       "Electronics", 32000.00, 5),
    (2,  "Kniha 1984",             "Books",         350.00, 50),
    (3,  "Tričko bílé",            "Clothing",      450.00, 30),
    (4,  "Hrnek modrý",            "Home",          250.00, 100),
    (5,  "Sluchátka Sony WH-1000", "Electronics",  3500.00, 15),
    (6,  "Kniha Hobit",            "Books",         420.00, 25),
    (7,  "Mikina šedá",            "Clothing",     1200.00, 20),
    (8,  "Polštář dekorační",      "Home",          800.00, 40),
    (9,  "Tablet Samsung Tab A",   "Electronics",  8500.00, 8),
    (10, "Kniha Solaris",          "Books",         380.00, 30),
]

ORDERS = [
    # (order_id, customer_id, order_date, status, total_amount)
    (1,  1,  "2024-03-01", "completed", 32000.00),
    (2,  2,  "2024-03-15", "completed",  1200.00),
    (3,  3,  "2024-04-02", "completed",   700.00),
    (4,  1,  "2024-04-20", "completed",  8500.00),
    (5,  4,  "2024-05-10", "cancelled",   420.00),
    (6,  5,  "2024-05-25", "completed",  3750.00),
    (7,  2,  "2024-06-12", "completed",  3500.00),
    (8,  6,  "2024-06-30", "completed",  1250.00),
    (9,  7,  "2024-07-15", "completed",   800.00),
    (10, 8,  "2024-08-05", "completed",  8500.00),
    (11, 3,  "2024-08-22", "pending",     350.00),
    (12, 9,  "2024-09-10", "completed",  1580.00),
    (13, 1,  "2024-09-28", "completed",   920.00),
    (14, 10, "2024-10-15", "completed", 32000.00),
    (15, 5,  "2024-11-03", "pending",    3950.00),
]

ORDER_ITEMS = [
    # (order_item_id, order_id, product_id, quantity, unit_price)
    (1,   1,  1, 1, 32000.00),  # Anna:    Laptop
    (2,   2,  7, 1,  1200.00),  # Petr:    Mikina
    (3,   3,  2, 2,   350.00),  # Markéta: 2× Kniha 1984
    (4,   4,  9, 1,  8500.00),  # Anna:    Tablet
    (5,   5,  6, 1,   420.00),  # Tomáš:   Hobit (cancelled)
    (6,   6,  5, 1,  3500.00),  # Eva:     Sluchátka
    (7,   6,  4, 1,   250.00),  # Eva:     Hrnek
    (8,   7,  5, 1,  3500.00),  # Petr:    Sluchátka
    (9,   8,  3, 1,   450.00),  # Jan:     Tričko
    (10,  8,  8, 1,   800.00),  # Jan:     Polštář
    (11,  9,  8, 1,   800.00),  # Hana:    Polštář
    (12, 10,  9, 1,  8500.00),  # Michael: Tablet
    (13, 11,  2, 1,   350.00),  # Markéta: Kniha 1984 (pending)
    (14, 12,  7, 1,  1200.00),  # Lucie:   Mikina
    (15, 12, 10, 1,   380.00),  # Lucie:   Solaris
    (16, 13,  4, 2,   250.00),  # Anna:    2× Hrnek
    (17, 13,  6, 1,   420.00),  # Anna:    Hobit
    (18, 14,  1, 1, 32000.00),  # David:   Laptop
    (19, 15,  5, 1,  3500.00),  # Eva:     Sluchátka (pending)
    (20, 15,  3, 1,   450.00),  # Eva:     Tričko (pending)
]


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()
        print(f"  ✗ removed existing {DB_PATH.name}")

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cur = conn.cursor()

    cur.executescript(SCHEMA_PATH.read_text())
    print("  ✓ created 4 tables (from schema.sql)")

    cur.executemany("INSERT INTO customers   VALUES (?, ?, ?, ?, ?, ?)", CUSTOMERS)
    cur.executemany("INSERT INTO products    VALUES (?, ?, ?, ?, ?)",    PRODUCTS)
    cur.executemany("INSERT INTO orders      VALUES (?, ?, ?, ?, ?)",    ORDERS)
    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)",    ORDER_ITEMS)
    conn.commit()

    print(f"  ✓ inserted: {len(CUSTOMERS)} customers · "
          f"{len(PRODUCTS)} products · {len(ORDERS)} orders · "
          f"{len(ORDER_ITEMS)} order_items")

    # sanity: order_items totals match order totals
    items_total  = cur.execute("SELECT SUM(quantity * unit_price) FROM order_items").fetchone()[0]
    orders_total = cur.execute("SELECT SUM(total_amount) FROM orders").fetchone()[0]
    if abs(items_total - orders_total) > 0.01:
        raise SystemExit(f"  ✗ totals mismatch: items={items_total} vs orders={orders_total}")
    print(f"  ✓ totals match: {items_total:,.2f} Kč")

    conn.close()
    print(f"\n✅ database ready: {DB_PATH}")


if __name__ == "__main__":
    main()
