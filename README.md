# Python Expense Tracker

A menu-driven command-line expense tracker. It stores expenses in a CSV file so records remain available after the program closes.

## Features

- Add expenses with a date, category, description, and amount.
- View all saved expenses.
- Filter expenses by category or date.
- Display totals grouped by category and a grand total.
- Validate dates (`YYYY-MM-DD`) and positive numeric amounts.
- Create `expenses.csv` automatically if it does not exist.
- Use Python's built-in `csv` module; no third-party packages are required.

## Files

- `expense_tracker.py` — application source code.
- `expenses.csv` — sample data with 12 fictional expense records. When running the app, this is the file that will be updated.
- `README.md` — project instructions.

## Requirements

- Python 3.8 or newer

## Run

Keep `expense_tracker.py` and `expenses.csv` in the same folder, then run:

```bash
python expense_tracker.py
```

If `expenses.csv` is missing, the program creates it with the correct header.

## CSV format

The file uses these columns:

```text
date,category,description,amount
```

Dates use ISO format (`YYYY-MM-DD`) and amounts are stored as decimal text in the CSV, then converted to `Decimal` for accurate totals.

## Example category summary

With the included sample data, the program calculates totals for Food, Transport, Education, Bills, and Entertainment, plus a grand total.

## Problem fixed

A common Windows CSV issue is extra blank lines when writing rows. I fixed this by opening CSV files with `newline=""` and using `csv.DictWriter`. I also validate dates and positive amounts before saving, so invalid input is not added to the file.

## Sample data notice

All entries in `expenses.csv` are fictional practice data. They do not contain real bank or payment information.
