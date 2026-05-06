from models import Transaction, CATEGORIES
from database import (init_db, add_transaction, get_all_transactions, get_by_category,
                      get_by_month, monthly_report, update_transaction, delete_transaction)
from datetime import date

def show_menu():
    print("1. Add transaction")
    print("2. View all transactions")
    print("3. Filter by category")
    print("4. Monthly report")
    print("5. Edit transaction")
    print("6. Delete transaction")
    print("7. Quit")
    return input("Choose (1-7): ")

def add_new():
    print("\nCategories:", ",".join(CATEGORIES))
    tx = Transaction(
        amount=float(input("Amount(GHS): ")),
        type=input("Type (income/expense): ").strip(),
        category=input("Category: ").strip(),
        description=input("Description: ").strip(),
        date=input(f"Date (DD-MM-YYYY)[{date.today()}]:") or str(date.today())
    )

    add_transaction(tx)
    print("Saved!")

def filter_cat():
    cat = input(f"Category ({','.join(CATEGORIES)}): ").strip()
    rows = get_by_category(cat)
    if not rows:
        print("No transactions found for that category. ")
        return
    for r in rows:
        print(f"{r['date']} | GHS {r['amount']:.2f} | {r['description']}")

def show_report():
    year = int(input("Year (YYYY): "))
    month = int(input("Month (1-12): "))
    income, expenses, breakdown = monthly_report(year, month)
    print(f"\n--- Report for {year}-{month:02d} ---")
    print(f"Total income: GHS{income:.2f}")
    print(f"Total expenses: GHS{expenses:.2f}")
    print(f"Balance: GHS{income - expenses:.2f}")
    print("\nSpending by category:")
    for row in breakdown:
        print(f"{row['category']}: GHS{row['total']:.2f}")

def view_all():
    """Display all transactions with IDs for editing/deleting."""
    rows = get_all_transactions()
    if not rows:
        print("No transactions found.")
        return
    print("\n--- All Transactions ---")
    print("ID | Date       | Type    | Amount   | Category    | Description")
    print("-" * 70)
    for r in rows:
        print(f"{r['id']:2d} | {r['date']} | {r['type']:7s} | GHS {r['amount']:7.2f} | {r['category']:11s} | {r['description']}")

def main():
    init_db()
    print("--- Finance Tracker ---")
    while True:
        choice = show_menu()
        if choice == "1":
            add_new()
        elif choice == "2":
            rows = get_all_transactions()
            for r in rows:
                print(f"{r['date']} | GHS {r['amount']:.2f} | {r['description']}")
        elif choice == "3":
            filter_cat()
        elif choice == "4":
            show_report()
        elif choice == "5":
            edit_tx()
        elif choice == "6":
            delete_tx()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")

def edit_tx():
    view_all() # show all so user can see the ids
    try:
        tx_id = int(input("Enter transaction id to edit: "))
        
        # Get and validate amount
        amount_str = input("New amount (GHS): ")
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError("Amount must be positive.")
        
        # Get and validate category
        category = input(f"New category ({','.join(CATEGORIES)}): ").strip()
        if category not in CATEGORIES:
            raise ValueError(f"Category must be one of: {', '.join(CATEGORIES)}.")
        
        # Get and validate type
        type_input = input("New type (income/expense): ").strip().lower()
        if type_input not in ("income", "expense"):
            raise ValueError("Type must be 'income' or 'expense'.")
        
        description = input("New description: ").strip()
        
        # Get and validate date
        date_in = input(f"New date (YYYY-MM-DD): ").strip()
        from datetime import datetime
        datetime.strptime(date_in, "%Y-%m-%d")  # Validate format
        
        update_transaction(tx_id, amount, type_input, category, description, date_in)
    except ValueError as e:
        print("Error:", e)

def delete_tx():
    view_all() # show all so user can see the ids
    try:
        tx_id = int(input("\nEnter transaction id to delete: "))
        confirm = input(f"Are you sure you want to delete transaction {tx_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            delete_transaction(tx_id)   
        else:            
            print("Deletion cancelled.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()