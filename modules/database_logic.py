import sqlite3

"""Database for the household"""
db_file = "household_database.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS household (
    household_name TEXT PRIMARY KEY UNIQUE,
    net_income TEXT,
    total_expenses INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS household_member (
    household_member_name TEXT PRIMARY KEY,
    member_net_income TEXT,
    member_net_raw INTEGER,
    member_percent_share TEXT,
    member_share_total TEXT,
    member_percent_raw REAL,
    member_total_expenses INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS expense_entry (
    ID TEXT PRIMARY KEY,
    expense_name TEXT,
    expense_amount_raw INTEGER,
    expense_amount_formatted TEXT,
    household_name TEXT REFERENCES household_member(household_member_name)
)''')


def write_to_database(entry, table, column):
    """Writes a given entry to a specified table and column in the database, replacing existing entries."""
    try:
        cursor.execute(
            f"REPLACE INTO {table} ({column}) VALUES (?)", (entry,)
        )
        conn.commit()
        print("Entry inserted or updated successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting or updating data: {e}")


if __name__ == "__main__":
    """Example usage:"""
    entry = "New expense"
    table = "expense_entry"
    column = "expense_name"
    write_to_database(entry, table, column)
