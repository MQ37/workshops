"""
test_cases.py — testovací sada pro SQL Quality Judge.

Každý case: (question, reference_sql).
- question        — v češtině, jak by se zeptal datový analytik
- reference_sql   — správné řešení, ručně napsané a ověřené proti eshop.sqlite

Cases pokrývají: COUNT, SUM, AVG, GROUP BY, JOIN, WHERE, ORDER BY + LIMIT,
date filtering, LEFT JOIN.
"""

TEST_CASES: list[tuple[str, str]] = [
    (
        "Kolik máme zákazníků celkem?",
        "SELECT COUNT(*) FROM customers",
    ),
    (
        "Kolik zákazníků je z Prahy?",
        "SELECT COUNT(*) FROM customers WHERE city = 'Praha'",
    ),
    (
        "Top 3 produkty podle prodaných kusů",
        """SELECT p.name, SUM(oi.quantity) AS qty
           FROM order_items oi JOIN products p ON oi.product_id = p.product_id
           GROUP BY p.product_id ORDER BY qty DESC LIMIT 3""",
    ),
    (
        "Celkové tržby v 2024 (jen dokončené objednávky)",
        """SELECT SUM(total_amount) FROM orders
           WHERE status = 'completed' AND order_date LIKE '2024%'""",
    ),
    (
        "Která kategorie produktů má nejvyšší průměrnou cenu?",
        """SELECT category, AVG(price) AS avg_price
           FROM products GROUP BY category
           ORDER BY avg_price DESC LIMIT 1""",
    ),
    (
        "Který zákazník udělal nejvíc objednávek?",
        """SELECT c.name, COUNT(*) AS n
           FROM orders o JOIN customers c ON o.customer_id = c.customer_id
           GROUP BY o.customer_id ORDER BY n DESC LIMIT 1""",
    ),
    (
        "Počet objednávek podle statusu",
        "SELECT status, COUNT(*) FROM orders GROUP BY status ORDER BY status",
    ),
    (
        "Produkty skladem méně než 20 kusů",
        "SELECT name, stock_qty FROM products WHERE stock_qty < 20 ORDER BY stock_qty",
    ),
    (
        "Která objednávka má nejvyšší hodnotu?",
        "SELECT order_id, total_amount FROM orders ORDER BY total_amount DESC LIMIT 1",
    ),
    (
        "Kolik kusů knih se prodalo celkem?",
        """SELECT SUM(oi.quantity)
           FROM order_items oi JOIN products p ON oi.product_id = p.product_id
           WHERE p.category = 'Books'""",
    ),
    (
        "Zákazníci, kteří nikdy nic neobjednali",
        """SELECT c.name FROM customers c
           LEFT JOIN orders o ON c.customer_id = o.customer_id
           WHERE o.order_id IS NULL""",
    ),
    (
        "Měsíční tržby v 2024 (jen completed)",
        """SELECT strftime('%Y-%m', order_date) AS month, SUM(total_amount) AS revenue
           FROM orders WHERE status = 'completed' AND order_date LIKE '2024%'
           GROUP BY month ORDER BY month""",
    ),
]
