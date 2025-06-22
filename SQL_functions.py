import psycopg2
from datetime import datetime
from config import host, user, password, db_name

def with_connection(do_something):
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=db_name
        )
        with connection:
            with connection.cursor() as cursor:
                do_something(cursor)
    except Exception as _ex:
        print("[ERROR]", _ex)
    finally:
        if connection:
            connection.close()


def add_expense(category, amount, date=None, comment=None):
    if not date:
        date = datetime.today().strftime("%Y-%m-%d")

    def execute(cursor):
        cursor.execute("""
            INSERT INTO expenses (category, amount, date, comment)
            VALUES (%s, %s, %s, %s)
        """, (category, amount, date, comment))
        print("[INFO] Expense added.")

    with_connection(execute)


def view_expenses(date=None):
    def execute(cursor):
        if not date:
            cursor.execute("SELECT * FROM expenses ORDER BY expense_id;")
        else:
            cursor.execute("SELECT * FROM expenses WHERE date = %s", (date,))

        rows = cursor.fetchall()
        if not rows:
            print("[INFO] No expenses found.")
        else:
            print("\n All Expenses:")
            print("-" * 80)
            for row in rows:
                print(f"ID: {row[0]} | Category: {row[1]} | Amount: {row[2]} | Date: {row[3]} | Comment: {row[4]}")
            print("-" * 80)

    with_connection(execute)


def total_expenses(date=None):
    def execute(cursor):
        if not date:
            cursor.execute("SELECT SUM(amount) FROM expenses")
        else:
            cursor.execute("""
                SELECT SUM(amount)
                FROM expenses
                WHERE date::TEXT LIKE %s
            """, (f"{date}%",))  # ← теперь работает с типом date

        result = cursor.fetchone()[0]
        total = result if result else 0
        print(f"[INFO] Total expenses: {total}")

    with_connection(execute)


def delete_expense_by_id(expense_id):
    def execute(cursor):
        cursor.execute("""
        SELECT * FROM expenses WHERE expense_id = %s
        """, (expense_id,))

        row = cursor.fetchone()
        if not row:
            print(f"[INFO] No expense found with ID {expense_id}.")
            return

        cursor.execute("""
        DELETE FROM expenses WHERE expense_id = %s;
        """, (expense_id,))
        print(f"[INFO] Expense with ID {expense_id} was deleted successfully.")

    with_connection(execute)


