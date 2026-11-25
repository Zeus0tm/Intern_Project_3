import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

CSV_FILE = Path(__file__).with_name("expenses.csv")
FIELDS = ["date", "category", "description", "amount"]


def ensure_csv_exists():
    """Create the CSV file with a header if it does not exist."""
    if not CSV_FILE.exists():
        with CSV_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()


def read_expenses():
    """Read valid expense records from the CSV file."""
    ensure_csv_exists()
    expenses = []

    with CSV_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                expense_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
                amount = Decimal(row["amount"])
                if amount <= 0 or not amount.is_finite():
                    continue
                category = row["category"].strip()
                description = row["description"].strip()
                if not category:
                    continue
                expenses.append({
                    "date": expense_date.isoformat(),
                    "category": category,
                    "description": description,
                    "amount": amount,
                })
            except (ValueError, InvalidOperation, KeyError, TypeError):
                # Ignore malformed rows instead of crashing the application.
                continue

    return expenses


def get_valid_date():
    while True:
        value = input("Date (YYYY-MM-DD): ").strip()
        try:
            return datetime.strptime(value, "%Y-%m-%d").date().isoformat()
        except ValueError:
            print("Invalid date. Example of a valid date: 2026-11-25")


def get_valid_amount():
    while True:
        value = input("Amount (positive number): ").strip()
        try:
            amount = Decimal(value)
            if amount.is_finite() and amount > 0:
                return amount.quantize(Decimal("0.01"))
        except InvalidOperation:
            pass
        print("Invalid amount. Enter a number greater than zero.")


def add_expense():
    print("\n--- Add Expense ---")
    expense_date = get_valid_date()

    while True:
        category = input("Category: ").strip()
        if category:
            break
        print("Category cannot be empty.")

    description = input("Description: ").strip()
    amount = get_valid_amount()

    ensure_csv_exists()
    with CSV_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)
        writer.writerow({
            "date": expense_date,
            "category": category,
            "description": description,
            "amount": f"{amount:.2f}",
        })

    print("Expense saved successfully.")


def display_expenses(expenses):
    if not expenses:
        print("No expenses found.")
        return

    print("\nDate       | Category       | Description              | Amount")
    print("-" * 70)
    for item in sorted(expenses, key=lambda x: x["date"]):
        print(
            f'{item["date"]:<10} | {item["category"]:<14} | '
            f'{item["description"][:24]:<24} | {item["amount"]:>10.2f}'
        )


def view_expenses():
    print("\n--- All Expenses ---")
    display_expenses(read_expenses())


def filter_expenses():
    print("\n--- Filter Expenses ---")
    print("1. Filter by category")
    print("2. Filter by date")
    choice = input("Choose filter (1-2): ").strip()

    expenses = read_expenses()

    if choice == "1":
        category = input("Enter category: ").strip().casefold()
        matches = [e for e in expenses if e["category"].casefold() == category]
    elif choice == "2":
        date_value = get_valid_date()
        matches = [e for e in expenses if e["date"] == date_value]
    else:
        print("Invalid filter choice.")
        return

    display_expenses(matches)


def category_summary():
    print("\n--- Category Summary ---")
    expenses = read_expenses()

    if not expenses:
        print("No expenses available for summary.")
        return

    totals = {}
    for item in expenses:
        category = item["category"]
        totals[category] = totals.get(category, Decimal("0.00")) + item["amount"]

    for category, total in sorted(totals.items(), key=lambda pair: pair[1], reverse=True):
        print(f"{category:<20} {total:>10.2f}")

    grand_total = sum(totals.values(), Decimal("0.00"))
    print("-" * 32)
    print(f"{'TOTAL':<20} {grand_total:>10.2f}")


def main():
    ensure_csv_exists()

    while True:
        print("\n==============================")
        print("       EXPENSE TRACKER")
        print("==============================")
        print("1. Add expense")
        print("2. View all expenses")
        print("3. Filter expenses")
        print("4. Category summary")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("Your expenses are saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-5.")


if __name__ == "__main__":
    main()
