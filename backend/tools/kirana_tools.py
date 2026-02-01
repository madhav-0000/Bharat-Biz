import sqlite3
from langchain.tools import tool

def get_db_connection():
    conn = sqlite3.connect('db/kirana.db')
    conn.row_factory = sqlite3.Row
    return conn

@tool
def update_udhaar(customer_name: str, amount: float):
    """Update or create an udhaar (credit) entry for a customer. 
    Use this when the user says things like 'Rahul ko 500 udhaar chada do'."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO udhaar_ledger (customer_name, amount_due)
        VALUES (?, ?)
        ON CONFLICT(id) DO UPDATE SET 
        amount_due = amount_due + ?, 
        last_updated = CURRENT_TIMESTAMP
    ''', (customer_name, amount, amount))
    conn.commit()
    conn.close()
    return f"Success: Added ₹{amount} to {customer_name}'s ledger."

@tool
def check_inventory(item_name: str):
    """Check stock level for a specific item. 
    Use this when user asks 'Doodh kitna bacha hai?'."""
    conn = get_db_connection()
    item = conn.execute('SELECT * FROM inventory WHERE item_name LIKE ?', (f'%{item_name}%',)).fetchone()
    conn.close()
    if item:
        return f"Stock for {item['item_name']}: {item['stock_quantity']} units."
    return f"Sorry, {item_name} is not in the system."