-- E-shop database schema (SQLite).
-- Single source of truth: loaded by populate_db.py to create tables
-- and by agent.py to include in the LLM system prompt.

CREATE TABLE customers (
    customer_id   INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    email         TEXT NOT NULL,
    city          TEXT,
    country       TEXT,       -- 'CZ', 'SK', 'AT'
    signup_date   TEXT        -- 'YYYY-MM-DD'
);

CREATE TABLE products (
    product_id    INTEGER PRIMARY KEY,
    name          TEXT NOT NULL,
    category      TEXT,       -- 'Electronics', 'Books', 'Clothing', 'Home'
    price         REAL,       -- v Kč
    stock_qty     INTEGER
);

CREATE TABLE orders (
    order_id      INTEGER PRIMARY KEY,
    customer_id   INTEGER NOT NULL,
    order_date    TEXT,       -- 'YYYY-MM-DD'
    status        TEXT,       -- 'completed', 'pending', 'cancelled'
    total_amount  REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

CREATE TABLE order_items (
    order_item_id INTEGER PRIMARY KEY,
    order_id      INTEGER NOT NULL,
    product_id    INTEGER NOT NULL,
    quantity      INTEGER NOT NULL,
    unit_price    REAL,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
