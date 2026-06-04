import csv
from datetime import datetime
from decimal import Decimal, InvalidOperation
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data"
DATA_FILE = DATA_DIR / "expenses.csv"

FIELDNAMES = ["date", "category", "description", "amount"]


def ensure_data_file():
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    if not DATA_FILE.exists() or DATA_FILE.stat().st_size == 0:
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
            writer.writeheader()


def read_expenses():
    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)
    except (FileNotFoundError, OSError, csv.Error):
        return []


def save_expense(expense):
    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDNAMES)
        writer.writerow(expense)


def parse_date(date_text):
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return date_text
    except ValueError:
        return None


def parse_amount(amount_text):
    try:
        amount = Decimal(amount_text)

        if not amount.is_finite() or amount <= 0:
            return None

        return amount
    except InvalidOperation:
        return None


def format_expenses(expenses):
    if len(expenses) == 0:
        return "Expenses\nNo expenses recorded yet."

    lines = ["Expenses"]

    for expense in expenses:
        lines.append(
            f"{expense['date']} | {expense['category']} | "
            f"{expense['description']} | {Decimal(expense['amount']):.2f}"
        )

    return "\n".join(lines)


def calculate_totals(expenses):
    totals = {}

    for expense in expenses:
        category = expense["category"]
        amount = Decimal(expense["amount"])

        if category not in totals:
            totals[category] = Decimal("0.00")

        totals[category] += amount

    return totals


def format_totals(totals):
    if len(totals) == 0:
        return "Totals by Category\nNo expenses recorded yet."

    lines = ["Totals by Category"]

    for category, total in totals.items():
        lines.append(f"{category} - {total:.2f}")

    return "\n".join(lines)


def prompt_for_expense():
    while True:
        date_text = input("Enter date (YYYY-MM-DD): ").strip()
        parsed_date = parse_date(date_text)

        if parsed_date is None:
            print("Invalid date. Please use YYYY-MM-DD.")
            continue

        break

    while True:
        category = input("Enter category: ").strip().title()

        if not category:
            print("Category cannot be empty.")
            continue

        break

    while True:
        description = input("Enter description: ").strip().capitalize()

        if not description:
            print("Description cannot be empty.")
            continue

        break

    while True:
        amount_text = input("Enter amount: ").strip()
        amount = parse_amount(amount_text)

        if amount is None:
            print("Amount must be a positive number.")
            continue

        break

    return {
        "date": parsed_date,
        "category": category,
        "description": description,
        "amount": str(amount),
    }


def main():
    ensure_data_file()

    while True:
        print("Expense Tracker")
        print("1. Add expense")
        print("2. List expenses")
        print("3. Show totals by category")
        print("4. Exit")

        choice = input("Choose an option (1-4): ").strip()

        if choice == "1":
            new_expense = prompt_for_expense()
            save_expense(new_expense)
            print("Expense saved.")

        elif choice == "2":
            data = read_expenses()
            text = format_expenses(data)
            print(text)

        elif choice == "3":
            data = read_expenses()
            totals = calculate_totals(data)
            text = format_totals(totals)
            print(text)

        elif choice == "4":
            print("Goodbye.")
            break

        else:
            print("Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()
