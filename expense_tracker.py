"""
Personal Expense Tracker with CSV
---------------------------------
A beginner-friendly command-line application to record, view, filter,
and analyze daily personal expenses with persistent CSV storage.
"""

import csv
import datetime
import os
import sys

# Ensure UTF-8 output encoding for Indian Rupee symbol (₹) across Windows/Unix terminals
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Constants
CSV_FILE = "expenses.csv"
CSV_HEADERS = ["date", "category", "description", "amount"]


def initialize_csv(file_name=CSV_FILE):
    """
    Ensures that the CSV file exists with the proper header row.
    If the file does not exist or is completely empty, it creates the file
    and writes the header row without overwriting existing records.
    """
    try:
        file_exists = os.path.exists(file_name)
        file_is_empty = file_exists and os.path.getsize(file_name) == 0

        if not file_exists or file_is_empty:
            with open(file_name, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                writer.writerow(CSV_HEADERS)
    except OSError as e:
        print(f"Error initializing CSV file: {e}")


def load_expenses(file_name=CSV_FILE):
    """
    Reads all expense records from the CSV file.
    Returns a list of dictionaries where each dict represents an expense:
    {'date': str, 'category': str, 'description': str, 'amount': float}
    """
    initialize_csv(file_name)
    expenses = []

    try:
        with open(file_name, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Basic check to skip empty or corrupted rows
                if not row or "date" not in row or "amount" not in row:
                    continue
                try:
                    amount = float(row["amount"])
                    expenses.append({
                        "date": row.get("date", "").strip(),
                        "category": row.get("category", "").strip().title(),
                        "description": row.get("description", "").strip(),
                        "amount": amount
                    })
                except (ValueError, TypeError):
                    # Skip rows where amount is invalid
                    continue
    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading expenses: {e}")
        return []

    return expenses


def format_currency(amount):
    """
    Formats a numeric amount with Indian Rupee symbol and 2 decimal places.
    Example: 150 -> ₹150.00
    """
    return f"₹{amount:.2f}"


def get_valid_date(prompt):
    """
    Prompts the user to enter a date in YYYY-MM-DD format.
    Validates calendar dates (e.g. handles leap years, month ranges).
    Allows pressing Enter to use today's date automatically.
    """
    while True:
        user_input = input(prompt).strip()
        if not user_input:
            today_str = datetime.date.today().strftime("%Y-%m-%d")
            print(f"Defaulting to today's date: {today_str}")
            return today_str

        try:
            valid_date = datetime.datetime.strptime(user_input, "%Y-%m-%d").date()
            return valid_date.strftime("%Y-%m-%d")
        except ValueError:
            print("Invalid date! Please enter a valid date in YYYY-MM-DD format (e.g., 2026-09-30).")


def get_valid_amount(prompt):
    """
    Prompts the user to enter a positive numeric amount.
    Validates that the input is a number and strictly greater than 0.
    """
    while True:
        user_input = input(prompt).strip()
        try:
            amount = float(user_input)
            if amount <= 0:
                print("Amount must be greater than 0. Please enter a valid amount.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid amount! Please enter a numeric value (e.g., 150 or 250.75).")


def display_expense_table(expenses):
    """
    Renders a clean, formatted table of expense records.
    """
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    col_widths = {
        "index": 4,
        "date": 12,
        "category": 16,
        "description": 28,
        "amount": 14
    }

    separator = "-" * (sum(col_widths.values()) + 13)
    print(separator)
    print(
        f"| {'#':<{col_widths['index']}} "
        f"| {'Date':<{col_widths['date']}} "
        f"| {'Category':<{col_widths['category']}} "
        f"| {'Description':<{col_widths['description']}} "
        f"| {'Amount':>{col_widths['amount']}} |"
    )
    print(separator)

    total = 0.0
    for i, exp in enumerate(expenses, start=1):
        desc = exp["description"]
        if len(desc) > col_widths["description"]:
            desc = desc[:col_widths["description"] - 3] + "..."

        cat = exp["category"]
        if len(cat) > col_widths["category"]:
            cat = cat[:col_widths["category"] - 3] + "..."

        amount_str = format_currency(exp["amount"])
        total += exp["amount"]

        print(
            f"| {i:<{col_widths['index']}} "
            f"| {exp['date']:<{col_widths['date']}} "
            f"| {cat:<{col_widths['category']}} "
            f"| {desc:<{col_widths['description']}} "
            f"| {amount_str:>{col_widths['amount']}} |"
        )

    print(separator)
    print(
        f"| {'TOTAL':<{col_widths['index'] + col_widths['date'] + col_widths['category'] + col_widths['description'] + 9}} "
        f"| {format_currency(total):>{col_widths['amount']}} |"
    )
    print(separator)


def add_expense(file_name=CSV_FILE):
    """
    Prompts the user for date, category, description, and amount,
    validates the inputs, and appends the new record to the CSV file.
    """
    print("\n----------------------------------------")
    print("           ADD NEW EXPENSE              ")
    print("----------------------------------------")

    date = get_valid_date("Enter Date (YYYY-MM-DD) [Press Enter for Today]: ")
    
    while True:
        category = input("Enter Category (e.g., Food, Travel, Bills): ").strip()
        if category:
            category = category.title()
            break
        print("Category cannot be empty. Please enter a category.")

    while True:
        description = input("Enter Description (e.g., Lunch, Train ticket): ").strip()
        if description:
            break
        print("Description cannot be empty. Please enter a description.")

    amount = get_valid_amount("Enter Amount: ")

    initialize_csv(file_name)

    try:
        with open(file_name, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([date, category, description, f"{amount:.2f}"])

        print("\nExpense added successfully!")
        print(f"Record: {date} | {category} | {description} | {format_currency(amount)}\n")
    except Exception as e:
        print(f"Error saving expense: {e}\n")


def view_expenses(file_name=CSV_FILE):
    """
    Loads all expenses from the CSV file and displays them in a clean table.
    """
    print("\n----------------------------------------")
    print("           ALL EXPENSES                 ")
    print("----------------------------------------")
    expenses = load_expenses(file_name)
    display_expense_table(expenses)


def filter_expenses(file_name=CSV_FILE):
    """
    Allows the user to filter recorded expenses by category or date.
    Filtering is case-insensitive.
    """
    expenses = load_expenses(file_name)
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    while True:
        print("\n----------------------------------------")
        print("           FILTER EXPENSES              ")
        print("----------------------------------------")
        print("1. Filter by Category")
        print("2. Filter by Date")
        print("3. Back to Main Menu")
        print("----------------------------------------")

        choice = input("Enter filter choice (1-3): ").strip()

        if choice == "1":
            target_category = input("Enter Category to filter by: ").strip()
            if not target_category:
                print("Category cannot be empty.")
                continue

            filtered = [
                exp for exp in expenses
                if exp["category"].lower() == target_category.lower()
            ]

            print(f"\nFiltered Results for Category: '{target_category.title()}'")
            if filtered:
                display_expense_table(filtered)
            else:
                print(f"No expenses found under category '{target_category}'.\n")
            break

        elif choice == "2":
            target_date = get_valid_date("Enter Date to filter by (YYYY-MM-DD): ")
            filtered = [
                exp for exp in expenses
                if exp["date"] == target_date
            ]

            print(f"\nFiltered Results for Date: {target_date}")
            if filtered:
                display_expense_table(filtered)
            else:
                print(f"No expenses found on date {target_date}.\n")
            break

        elif choice == "3":
            break
        else:
            print("Invalid choice! Please select 1, 2, or 3.")


def category_summary(file_name=CSV_FILE):
    """
    Calculates and displays a summary of expenses broken down by category,
    along with the overall total expenses.
    """
    print("\n----------------------------------------")
    print("           CATEGORY SUMMARY             ")
    print("----------------------------------------")

    expenses = load_expenses(file_name)
    if not expenses:
        print("\nNo expenses recorded yet.\n")
        return

    totals_by_category = {}
    total_spent = 0.0

    for exp in expenses:
        cat = exp["category"]
        amt = exp["amount"]
        totals_by_category[cat] = totals_by_category.get(cat, 0.0) + amt
        total_spent += amt

    # Display categories in alphabetical order
    max_cat_len = max(len(cat) for cat in totals_by_category.keys())
    cat_width = max(max_cat_len + 2, 16)

    print()
    for cat in sorted(totals_by_category.keys()):
        amt = totals_by_category[cat]
        print(f"{cat:<{cat_width}}: {format_currency(amt)}")

    print("-" * (cat_width + 16))
    print(f"{'Total':<{cat_width}}: {format_currency(total_spent)}")
    print("-" * (cat_width + 16))
    print()


def main():
    """
    Main application loop presenting the CLI menu.
    """
    initialize_csv()

    while True:
        print("========================================")
        print("       PERSONAL EXPENSE TRACKER         ")
        print("========================================")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Filter Expenses")
        print("4. Category Summary")
        print("5. Exit")
        print("========================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            filter_expenses()
        elif choice == "4":
            category_summary()
        elif choice == "5":
            print("\nThank you for using Personal Expense Tracker. Goodbye!\n")
            break
        else:
            print("\nInvalid choice! Please select an option between 1 and 5.\n")


if __name__ == "__main__":
    main()
