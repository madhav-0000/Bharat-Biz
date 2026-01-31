
CREATE TABLE inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT NOT NULL,
    stock_quantity REAL DEFAULT 0,
    price REAL NOT NULL,
    gst_percent REAL DEFAULT 18.0 -- Default for many retail items
);

CREATE TABLE udhaar_ledger (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_name TEXT NOT NULL,
    amount_due REAL DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT,
    total_amount REAL,
    transaction_type TEXT CHECK(transaction_type IN ('CASH', 'UPI', 'UDHAAR')),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);