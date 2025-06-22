import SQL_functions

print("Hello to your Expenses Helper 1.0! ")

def show_info():
    print("""
            Choose operation:
            1 - Add expense to table
            2 - View all expenses
            3 - View total expenses
            4 - Delete expenses on ID
            0 - Exit
        """)

def main():
    while True:
        show_info()
        try:
            operation = int(input("Enter the operation number(0-4): "))
            if operation == 1:
                while True:
                    category = input("Enter category(Necessarily): ")
                    if category == "":
                        continue
                    else:
                        break
                amount = int(input("Enter amount: "))
                date = input("Enter date(Y-M-D): ")
                comment = input("Enter comment: ")
                SQL_functions.add_expense(category=category, amount=amount, date=date, comment=comment)

            elif operation == 2:
                date = input("Enter date(Y-M-D or nothing to see all): ")
                SQL_functions.view_expenses(date)

            elif operation == 3:
                date = input("Enter date(YYYY-MM or YYYY or nothing to see all): ")
                SQL_functions.total_expenses(date)

            elif operation == 4:
                expense_id = input("Enter expense id: ")
                SQL_functions.delete_expense_by_id(expense_id)

            elif operation == 0:
                print("Goodbye!")
                break
            else:
                print("Error. Please enter a number between 0 and 4")
        except ValueError:
            print("Error. Please enter a valid number (digits only).")




if __name__ == '__main__':
    main()
