import sqlite3

"""Database for the household"""
db_file = "household_database.db"
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS household (
    household_ID INTEGER PRIMARY KEY,
    household_name TEXT,
    household_net_income TEXT,
    total_expenses INTEGER
)''')

cursor.execute('''CREATE TABLE IF NOT EXISTS household_member (
    household_member_ID INTEGER PRIMARY KEY,
    household_member_name TEXT,
    member_net_income TEXT,
    member_net_raw INTEGER,
    member_percent_share TEXT,
    member_share_total TEXT,
    member_percent_raw REAL,
    member_total_expenses INTEGER
)''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS expense_entry (
    unique_identifier TEXT PRIMARY KEY,
    ID INTEGER,
    expense_name TEXT,
    expense_amount_raw INTEGER,
    expense_amount_formatted TEXT,
    household_member_ID INTEGER REFERENCES household_member(household_member_ID)
);''')


def write_to_database(data, table, condition=None, replace_existing=True):
    """Writes a given dictionary of data to a specified table, updating existing entries based on the provided condition.

    Args:
        data (dict): A dictionary containing the column names and their corresponding values.
        table (str): The name of the table to insert or update.
        condition (str, optional): A condition to filter rows for updates. Defaults to None.
        replace_existing (bool, optional): Whether to replace the existing row if it exists. Defaults to True.
    """
    try:
        columns = ", ".join(data.keys())
        values = ", ".join(["?" for _ in data.values()])

        if condition:
            sql = f"UPDATE {table} SET {columns} = {values} WHERE {condition}"
        else:
            if replace_existing:
                sql = f"INSERT OR REPLACE INTO {
                    table} ({columns}) VALUES ({values})"
            else:
                sql = f"INSERT INTO {table} ({columns}) VALUES ({values})"

        if table == "expense_entry" and "household_member_ID" not in data:
            raise ValueError("Missing household_member_ID for expense entry")

        cursor.execute(sql, tuple(data.values()))
        conn.commit()
        # print("Entry inserted or updated successfully.")
    except sqlite3.Error as e:
        print(f"Error inserting or updating data: {e}")


def delete_expense(unique_identifier):
    sql = "DELETE FROM expense_entry WHERE unique_identifier = ?"
    cursor.execute(sql, (unique_identifier,))
    conn.commit()
    print("Expense deleted successfully.")


def fetch_from_database(table, columns="*", condition=None):
    """Fetches data from a specified table based on the given condition.

    Args:
    table (str): The name of the table to fetch data from.
    columns (str or list, optional): The columns to fetch. Defaults to "*".
    condition (str, optional): A condition to filter rows. Defaults to None.

    Returns:
    list: A list of tuples containing the fetched rows.
    """
    try:
        if isinstance(columns, list):
            columns = ", ".join(columns)

            sql = f"SELECT {columns} FROM {table}"
            if condition:
                sql += f" WHERE {condition}"

            cursor.execute(sql)
            rows = cursor.fetchall()
        return rows
    except sqlite3.Error as e:
        print(f"Error fetching data: {e}")
        return []


if __name__ == "__main__":
    """Example usage:"""
    entry = "New expense"
    table = "expense_entry"
    column = "expense_name"
    write_to_database(entry, table, column)
