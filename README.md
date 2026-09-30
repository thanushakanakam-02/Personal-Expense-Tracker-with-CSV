# Personal Expense Tracker with CSV

A beginner-friendly command-line Personal Expense Tracker developed in Python to record, manage, filter, and analyze daily expenses by category with persistent CSV storage.

---

## Table of Contents

- [Project Description](#project-description)
- [Objective](#objective)
- [Key Features](#key-features)
- [Technologies & Libraries Used](#technologies--libraries-used)
- [CSV File Structure](#csv-file-structure)
- [How the Program Works](#how-the-program-works)
- [How to Run the Project](#how-to-run-the-project)
- [Example Usage & Sample Output](#example-usage--sample-output)
  - [1. Main Menu](#1-main-menu)
  - [2. Adding an Expense](#2-adding-an-expense)
  - [3. Viewing All Expenses](#3-viewing-all-expenses)
  - [4. Filtering Expenses](#4-filtering-expenses)
  - [5. Category Summary](#5-category-summary)
  - [6. Input Validation Handling](#6-input-validation-handling)
- [Learning Outcomes](#learning-outcomes)
- [Project Structure](#project-structure)
- [Author & Submission Note](#author--submission-note)

---

## Project Description

Managing daily expenses is essential for personal financial health. The **Personal Expense Tracker with CSV** is a Python CLI (Command-Line Interface) tool designed to allow individuals to record their expenses on the go. Unlike temporary in-memory solutions, this project uses standard CSV file persistence so that all recorded expenses remain safely preserved between program executions.

The project is built specifically to demonstrate core Python fundamentals, clean functional architecture, robust input validation, and file handling without relying on bulky third-party libraries.

---

## Objective

The objective of this project is to:
- Build an interactive terminal application using Python's standard library.
- Implement structured data storage and retrieval using Python's built-in `csv` module.
- Provide data querying features (filtering by category or date).
- Compute statistical category-wise aggregations and totals dynamically.
- Enforce input validation and exception handling for user inputs (dates, numeric amounts, menu selections).
- Create a clean, submission-ready project for an online Python internship.

---

## Key Features

1. **Add Expense**:
   - Record date (`YYYY-MM-DD`), category, description, and amount.
   - Allows pressing `Enter` to automatically record today's date.
   - Validates that amount is a positive number (`> 0`).
   - Validates proper calendar date format.

2. **View All Expenses**:
   - Displays all stored expenses in an organized tabular format with column headers, aligned text, and total sum.
   - Formats currency neatly with the Indian Rupee symbol (`₹150.00`).
   - Handles empty records gracefully with a friendly message (`No expenses recorded yet.`).

3. **Filter Expenses**:
   - **Filter by Category**: Search expenses under a specific category (case-insensitive, e.g., `food`, `Food`, `FOOD`).
   - **Filter by Date**: Search all expenses recorded on a specific date (`YYYY-MM-DD`).

4. **Category-wise Summary**:
   - Calculates total spending grouped per category.
   - Computes overall grand total expenditure.
   - Displays dynamic calculations (no hardcoded outputs).

5. **Persistent CSV Storage**:
   - Stores data in `expenses.csv`.
   - Appends records without overwriting historical data.
   - Automatically initializes the CSV file with headers (`date,category,description,amount`) if missing or empty.

6. **Error & Exception Handling**:
   - Handles non-numeric inputs for amounts and menus.
   - Handles invalid calendar dates (e.g., February 30th, invalid month ranges).
   - Handles missing or empty CSV files gracefully without crashing.

---

## Technologies & Libraries Used

This project relies exclusively on **Python's standard library** (no external packages such as pandas or tabulate are required):

- **Python 3.8+**
- **`csv`**: Built-in module for reading from and writing to comma-separated values files.
- **`datetime`**: Built-in module for date parsing and calendar validation.
- **`os`**: Built-in module for checking file paths and sizes.
- **`sys`**: Built-in module for managing terminal character encoding (UTF-8 support for currency symbols).

---

## CSV File Structure

The project stores records in `expenses.csv` with the following column schema:

```csv
date,category,description,amount
2026-09-30,Food,Lunch,150.00
2026-09-30,Travel,Metro Card Recharge,200.00
2026-10-01,Education,Python Book,450.00
```

| Field Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `date` | `String` (`YYYY-MM-DD`) | Date when expense occurred | `2026-09-30` |
| `category` | `String` | Category title (e.g., Food, Travel) | `Food` |
| `description` | `String` | Brief note explaining expense | `Lunch` |
| `amount` | `Float` | Expense amount in Rupees | `150.00` |

---

## How the Program Works

1. **Initialization (`initialize_csv`)**: When the script starts, it verifies whether `expenses.csv` exists. If not, it creates it with the header row `date,category,description,amount`.
2. **Main Loop (`main`)**: A `while True` loop displays the interactive menu and waits for the user's choice (1 to 5).
3. **Adding Data (`add_expense`)**:
   - Prompts for date, category, description, and amount with validation loops.
   - Appends the validated data row to `expenses.csv`.
4. **Displaying Data (`view_expenses` / `display_expense_table`)**:
   - Reads records via `csv.DictReader`.
   - Formats each row into formatted columns with totals.
5. **Filtering Data (`filter_expenses`)**:
   - Prompts the user to select filtering by category or date.
   - Performs matching (case-insensitive for categories) and displays filtered rows.
6. **Aggregating Data (`category_summary`)**:
   - Iterates through the list of expenses, accumulating sums in a dictionary (`totals_by_category[cat] += amt`).
   - Displays category subtotals and the overall total.
7. **Exit**: Gracefully exits the loop with a farewell message.

---

## How to Run the Project

### Prerequisites
Make sure Python 3 is installed on your system. You can verify this by running:
```bash
python --version
```

### Steps to Run
1. Open your terminal or command prompt.
2. Navigate to the project directory:
   ```bash
   cd "Personal Expense Tracker"
   ```
3. Run the main Python script:
   ```bash
   python expense_tracker.py
   ```

---

## Example Usage & Sample Output

### 1. Main Menu
```text
========================================
       PERSONAL EXPENSE TRACKER         
========================================
1. Add Expense
2. View All Expenses
3. Filter Expenses
4. Category Summary
5. Exit
========================================
Enter your choice: 1
```

### 2. Adding an Expense
```text
----------------------------------------
           ADD NEW EXPENSE              
----------------------------------------
Enter Date (YYYY-MM-DD) [Press Enter for Today]: 2026-09-30
Enter Category (e.g., Food, Travel, Bills): Food
Enter Description (e.g., Lunch, Train ticket): Lunch
Enter Amount: 150

Expense added successfully!
Record: 2026-09-30 | Food | Lunch | ₹150.00
```

### 3. Viewing All Expenses
```text
----------------------------------------
           ALL EXPENSES                 
----------------------------------------
-------------------------------------------------------------------------------------
| #    | Date         | Category         | Description                  |         Amount |
-------------------------------------------------------------------------------------
| 1    | 2026-09-30   | Food             | Lunch                        |        ₹150.00 |
| 2    | 2026-09-30   | Travel           | Metro Ticket                 |         ₹50.00 |
| 3    | 2026-10-01   | Education        | Python Course Material       |        ₹500.00 |
-------------------------------------------------------------------------------------
| TOTAL                                                                 |        ₹700.00 |
-------------------------------------------------------------------------------------
```

### 4. Filtering Expenses

**Filter by Category:**
```text
----------------------------------------
           FILTER EXPENSES              
----------------------------------------
1. Filter by Category
2. Filter by Date
3. Back to Main Menu
----------------------------------------
Enter filter choice (1-3): 1
Enter Category to filter by: food

Filtered Results for Category: 'Food'
-------------------------------------------------------------------------------------
| #    | Date         | Category         | Description                  |         Amount |
-------------------------------------------------------------------------------------
| 1    | 2026-09-30   | Food             | Lunch                        |        ₹150.00 |
-------------------------------------------------------------------------------------
| TOTAL                                                                 |        ₹150.00 |
-------------------------------------------------------------------------------------
```

### 5. Category Summary
```text
----------------------------------------
           CATEGORY SUMMARY             
----------------------------------------

Education       : ₹500.00
Food            : ₹150.00
Travel          : ₹50.00
--------------------------------
Total           : ₹700.00
--------------------------------
```

### 6. Input Validation Handling
```text
Enter Amount: abc
Invalid amount! Please enter a numeric value (e.g., 150 or 250.75).
Enter Amount: -50
Amount must be greater than 0. Please enter a valid amount.
Enter Amount: 150
```

```text
Enter Date (YYYY-MM-DD) [Press Enter for Today]: 2026-02-30
Invalid date! Please enter a valid date in YYYY-MM-DD format (e.g., 2026-09-30).
```

---

## Learning Outcomes

By building this project, the following core Python concepts were practiced:
- **Modular Code Design**: Splitting code into single-responsibility functions (`initialize_csv`, `add_expense`, `view_expenses`, `filter_expenses`, `category_summary`).
- **File I/O and Persistence**: Handling CSV reading and writing safely with context managers (`with open(...) as file:`).
- **Data Collections**: Using lists of dictionaries to store and query tabular data, and using dictionaries for key-value frequency and sum aggregations.
- **Robust Exception Handling**: Utilizing `try-except` blocks for `ValueError`, `TypeError`, `OSError`, and `FileNotFoundError`.
- **User Interface Formatting**: Generating clean ASCII-based tables and formatted currency outputs without external packages.

---

## Project Structure

```text
Personal Expense Tracker/
│
├── expense_tracker.py   # Main CLI application code
├── expenses.csv         # Persistent CSV storage file
├── README.md            # Comprehensive documentation
└── .gitignore           # Git ignore file (keeps expenses.csv tracked)
```

---

## Author & Submission Note

Developed as part of the **Python Programming Online Internship**. Ready for submission, evaluation, and GitHub repository hosting.
