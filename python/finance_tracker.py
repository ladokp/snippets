import csv
import datetime
import os
from collections import defaultdict
import matplotlib.pyplot as plt

# File to store the expense data
DATA_FILE = "expenses.csv"

# Initialize data file with a header if it doesn't exist
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Date", "Category", "Amount"])

def add_expense(date, category, amount):
    """
    Add a new expense to the CSV file.

    Parameters:
        date (str): The date of the expense in 'YYYY-MM-DD' format.
        category (str): The category of the expense (e.g., Food, Transport, Rent).
        amount (float): The amount spent in euros.

    Raises:
        ValueError: If the date is not in the correct format or the amount is not a valid float.
    """
    with open(DATA_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, amount])
    print("Expense added successfully.")

def view_expenses():
    """
    Display all expenses from the CSV file.

    Reads and prints each expense entry in the format:
    Date: YYYY-MM-DD, Category: CategoryName, Amount: €Amount
    """
    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        print("\nRecorded Expenses:")
        for row in reader:
            print(f"Date: {row[0]}, Category: {row[1]}, Amount: €{row[2]}")

def summarize_expenses():
    """
    Summarize expenses by category and display the totals.

    Returns:
        dict: A dictionary with categories as keys and total amounts as values.
    """
    summary = defaultdict(float)
    with open(DATA_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            summary[row[1]] += float(row[2])
    
    print("\nExpense Summary by Category:")
    for category, amount in summary.items():
        print(f"{category}: €{amount:.2f}")
    
    return summary

def plot_expenses():
    """
    Generate a bar chart showing expenses by category.

    Uses matplotlib to create a simple bar chart visualizing the expense summary.
    """
    summary = summarize_expenses()
    categories = list(summary.keys())
    amounts = list(summary.values())

    plt.figure(figsize=(8, 5))
    plt.bar(categories, amounts)
    plt.xlabel("Category")
    plt.ylabel("Amount (€)")
    plt.title("Expenses by Category")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def main():
    """
    Main function providing a menu interface for the Personal Finance Tracker.

    Options:
        1. Add Expense
        2. View Expenses
        3. Summarize Expenses
        4. Plot Expenses
        5. Exit
    """
    while True:
        print("\nPersonal Finance Tracker")
        print("1. Add Expense")
        print("2. View Expenses")
        print("3. Summarize Expenses")
        print("4. Plot Expenses")
        print("5. Exit")

        choice = input("Choose an option (1-5): ")
        
        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): ")
            category = input("Enter category (e.g., Food, Transport, Rent): ")
            amount = input("Enter amount (€): ")
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d")
                add_expense(date, category, float(amount))
            except ValueError:
                print("Invalid date or amount. Please try again.")
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            summarize_expenses()
        elif choice == "4":
            plot_expenses()
        elif choice == "5":
            print("Exiting. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Entry point of the script
if __name__ == "__main__":
    main()
