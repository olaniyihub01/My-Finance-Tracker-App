import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

root = tk.Tk()
root.title("Mypersonal Finance Tracker")
root.geometry("700x550")
root.configure(bg="black", borderwidth="30")

# trying to solve an error
entry_description = tk.Entry()  # Add root here
entry_amount = tk.Entry()       # Add root here
combo_category = ttk.Combobox()  # Add root here
combo_category.grid(row=2, column=1)

# this was the solution to previous error
def create_table():
    # Create SQLite database and expenses table if not exists
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            amount REAL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()


def add_expense(description, amount, category):
    # Add expense to the database
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)",
                   (description, amount, category))
    conn.commit()
    conn.close()


def show_chart():
    # Generate and display a pie chart based on expense categories
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if data:
        categories, amounts = zip(*data)
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title("Expense Distribution")
        plt.show()
    else:
        print("No data to display.")


def save_expense():
    # Retrieve user input and save expense
    global entry_description, entry_amount, combo_category  # Add global here

    description = entry_description.get()
    amount = entry_amount.get()
    category = combo_category.get()

    if description and amount and category:
        add_expense(description, amount, category)
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        combo_category.set("")


def main():
    global entry_description, entry_amount, combo_category
    create_table()

    tk.Label(root, text="WELCOME", font=("Bold", 30), bg="brown")

    # Entry widgets
    tk.Label(root, text="Description:").grid(row=1, column=0)
    entry_description.grid(row=1, column=1)

    tk.Label(root, text="Amount:").grid(row=3, column=0)
    entry_amount.grid(row=3, column=1)

    tk.Label(root, text="Category:").grid(row=6, column=0)
    categories = ["Groceries", "Entertainment", "Utilities", "Other"]
    combo_category.config(values=categories)
    combo_category.grid(row=6, column=1)

    # Button to save expense
    tk.Button(root, text="Save Expense", command=save_expense).grid(row=9, column=0, columnspan=2, pady=10)

    # Button to show expense distribution chart
    tk.Button(root, text="Show Expense Chart", command=show_chart).grid(row=12, column=0, columnspan=2)

    root.mainloop()

main()

