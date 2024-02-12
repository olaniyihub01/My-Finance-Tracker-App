import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import sqlite3

window = tk.Tk()
# App title
window.title("My Finance Tracker App")
window.geometry("450x450")
window.configure(bg="#ecf0f1", borderwidth="30")

# create GUI components
entry_description = ttk.Entry(window)
entry_amount = ttk.Entry()
combo_category = ttk.Combobox()
combo_category.grid(row=2, column=1, padx=5, pady=5)


# our sqlite3 database which saves the user expenses.
def create_table():
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
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO expenses (description, amount, category) VALUES (?, ?, ?)",
                   (description, amount, category))
    conn.commit()
    conn.close()


# connects to a SQLite database, retrieves expense data grouped by category,
# and displays it as pie chart using matplotlib.
def show_pie_chart():
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


def show_bar_chart():
    conn = sqlite3.connect("finance_tracker.db")
    cursor = conn.cursor()
    cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
    data = cursor.fetchall()
    conn.close()

    if data:
        categories, amounts = zip(*data)
        plt.bar(categories, amounts)
        plt.xlabel("Categories")
        plt.ylabel("Total Amount")
        plt.title("Expense Distribution (Bar Chart)")
        plt.show()
    else:
        print("No data to display.")


def save_expense():
    description = entry_description.get()
    amount = entry_amount.get()
    category = combo_category.get()

    if description and amount and category:
        add_expense(description, amount, category)
        entry_description.delete(0, tk.END)
        entry_amount.delete(0, tk.END)
        combo_category.set("")


# function  which sets up a GUI window with labels, entry fields,
# dropdown menu, and buttons for saving expenses and displaying them using pie or bar charts,
# then run the main function.
def main():
    create_table()

    ttk.Label(window, text="Description:", foreground="#2c3e50", borderwidth="30").grid(row=0, column=0, padx=5, pady=5)
    entry_description.grid(row=0, column=2, padx=5, pady=5)

    ttk.Label(window, text="Amount:", foreground="#2c3e50", borderwidth="30").grid(row=1, column=0, padx=5, pady=5)
    entry_amount.grid(row=1, column=2, padx=5, pady=5)

    ttk.Label(window, text="Category:", foreground="#2c3e50", borderwidth="30").grid(row=2, column=0, padx=5, pady=5)
    categories = ["Groceries", "Entertainment", "Utilities", "Clothing", "Others"]
    combo_category.config(values=categories)
    combo_category.grid(row=2, column=2, padx=5, pady=5)

    ttk.Button(window, text="Save Expense", command=save_expense).grid(row=11, column=2, columnspan=2, pady=10)
    ttk.Button(window, text="View Expenses With Pie Chart", command=show_pie_chart).grid(row=12, column=1, pady=5)
    ttk.Button(window, text="View Expenses With Bar Chart", command=show_bar_chart).grid(row=13, column=1, pady=5)

    window.mainloop()


main()
