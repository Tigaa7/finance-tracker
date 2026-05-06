import   sqlite3

DB_PATH = "data/transactions.db"

def init_db():
    
    """Create a table if it doesnt exist yet"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
                 CREATE TABLE IF NOT EXISTS transactions(
                 id     INTEGER PRIMARY KEY AUTOINCREMENT,
                 amount real NOT NULL,
                 type TEXT NOT NULL CHECK(type IN('income', 'expense')),
                 category TEXT NOT NULL,
                 description TEXT, 
                 date TEXT NOT NULL,
                 created_at TEXT DEFAULT CURRENT_TIMESTAMP
                 )
                 
    """)
    conn.commit()
    conn.close()

def add_transaction(tx):
    """Save a Tranasaction object to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        INSERT INTO transactions
        (amount, type, category, description, date)
        VALUES (?, ?, ?, ?, ?)
        """, (tx.amount, tx.type, tx.category, tx.description, tx.date))
    conn.commit()
    conn.close()

def get_all_transactions():
    """Return all transactions, newest first."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM transactions ORDER BY date DESC"
    ).fetchall()
    conn.close()
    return rows

def get_by_category(category):
    """Return all transactions for one category"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row      
    rows = conn.execute(
        "SELECT * FROM transactions WHERE category = ? ORDER BY date DESC", (category,)
    ).fetchall()
    conn.close()
    return rows

def get_by_month(year, type):
    """Return all transactions for a given month and type (income or expense)"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        "SELECT * FROM transactions WHERE strftime('%Y-%m', date) = ? AND type = ? ORDER BY date DESC", (f"{year}-01", type)
    ).fetchall()
    conn.close()
    return rows

def monthly_report(year, month):
    """Return income, expenses and breakdown by category."""
    prefix = f"{year}-{month:02d}"
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    # Add up all income for the month
    income = conn.execute("""
        SELECT COALESCE(SUM(amount),0) as total
        FROM transactions
        WHERE date LIKE ? AND type = 'income' 
        """, (prefix + "%",)).fetchone()["total"]
    
    # Add up all expenses for the month
    expenses = conn.execute("""
        SELECT COALESCE(SUM(amount), 0) as total
        FROM transactions
        WHERE date LIKE ? AND type = 'expense'
        """, (prefix + "%",)).fetchone()["total"]
    
    # Break expenses down by category
    breakdown = conn.execute("""
        SELECT category, SUM(amount) as total
        FROM transactions
        WHERE date LIKE ? AND type = 'expense'
        GROUP BY category
        ORDER BY total DESC
        """, (prefix + "%",)).fetchall()
    
    conn.close()
    return income, expenses, breakdown

def update_transaction(tx_id, amount, type, category, description, date):
    """Update an existing transaction by its id"""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        UPDATE transactions
        SET amount = ?, type = ?, category = ?, description = ?, date = ?
        WHERE id = ?
        """, (amount, type, category, description, date, tx_id))
    conn.commit()
    conn.close()
    print(f"Transaction {tx_id} updated successfully.")

def delete_transaction(tx_id):
    """Delete a transaction by its id."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM transactions WHERE id = ?", (tx_id,))
    conn.commit()
    conn.close()
    print(f"Transaction {tx_id} deleted successfully.")