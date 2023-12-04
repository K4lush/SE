import tkinter as tk
from tkinter import ttk, messagebox
from income_expense_analyzer import analyze_expenses_and_income
from weekly_plan_generator import generate_weekly_plan
import sqlite3

class DatabaseHandler:
    def __init__(self, db_name="financial_data.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.conn.execute('''
            CREATE TABLE IF NOT EXISTS financial_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                income REAL NOT NULL
            )
        ''')
        self.conn.execute('''
                    CREATE TABLE IF NOT EXISTS expenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT NOT NULL,
                        category TEXT NOT NULL,
                        amount REAL NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES financial_data(user_id)
                    )
                ''')
        self.conn.commit()

    def get_expenses(self, user_id):
        self.cursor.execute("SELECT category, amount FROM expenses WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchall()
        print(result)
        return result


    def add_income(self, user_id, income_amount):
        self.cursor.execute('INSERT INTO financial_data (user_id, income) VALUES (?, ?) ', (user_id, income_amount))
        self.conn.commit()

    def add_expense(self, user_id, category, amount):
        self.cursor.execute('INSERT INTO expenses (user_id, category, amount) VALUES (?, ?, ?) ',
                            (user_id, category, amount))
        self.conn.commit()

    def get_income(self, user_id):
        self.cursor.execute("SELECT income FROM financial_data WHERE user_id = ?", (user_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None

class FinancialTracker:
    def __init__(self, root, user_id, db_handler):
        '''

        :param root: tkinter window
        :param usr: current user logged in!
        '''
        self.root = root
        self.root.title("Financial Tracker")
        self.user_id = user_id  # Store the user_id

        # Initialize variables
        self.income = 0.0
        # Initialize expense_entries as a dictionary
        self.expense_entries = {}

        self.db_handler = db_handler  # Move this line up

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        user_income = self.db_handler.get_income(self.user_id)

        if not user_income:
            # Generate Plan button
            generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan", command=self.generate_plan)
            generate_plan_button.grid(row=3, column=1, padx=10, pady=10)

            # Financial Education (Use Case)
            education_button = tk.Button(self.root, text="Financial Education", command=self.financial_education)
            education_button.grid(row=3, column=2, padx=10, pady=10)

            # Income section
            income_label = tk.Label(self.root, text="Income:")
            income_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

            self.income_entry = tk.Entry(self.root)
            self.income_entry.grid(row=0, column=1, padx=10, pady=10)

            add_income_button = tk.Button(self.root, text="Add Income", command=self.add_income)
            add_income_button.grid(row=0, column=2, padx=10, pady=10)

            # Label to display the added income
            self.income_display_label = tk.Label(self.root, text="No income added yet")
            self.income_display_label.grid(row=0, column=3, columnspan=2, padx=10, pady=10, sticky=tk.W)

            expense_label = tk.Label(self.root, text="Expense:")
            expense_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

            self.expense_display_var = tk.StringVar()
            self.expense_display_label = tk.Label(self.root, textvariable=self.expense_display_var)
            self.expense_display_label.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)

            # Dropdown menu for expense categories using Combobox
            expense_categories = ["Food", "Essentials", "Shopping"]
            self.expense_category = ttk.Combobox(self.root, values=expense_categories, state="readonly")
            self.expense_category.set("Select Category")  # default value
            self.expense_category.grid(row=1, column=2, padx=10, pady=10)

            self.expense_entry = tk.Entry(self.root)
            self.expense_entry.grid(row=1, column=1, padx=10, pady=10)

            add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
            add_expense_button.grid(row=1, column=3, padx=10, pady=10)

        else:

            # Fetch expense entries from the database
            expenses_from_db = self.db_handler.get_expenses(self.user_id)

            # Fetch income from the database
            income_from_db = self.db_handler.get_income(self.user_id)

            # Update the expense_entries dictionary
            for expense in expenses_from_db:
                category, amount = expense[0], expense[1]
                self.expense_entries[category] = amount

            # Generate Plan button
            generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan",
                                             command=self.generate_plan_logged(income_from_db, self.expense_entries))
            generate_plan_button.grid(row=3, column=1, padx=10, pady=10)

    def add_income(self):
        # Get the income amount from the Entry widget
        income_amount = self.income_entry.get()

        # Check if the income amount is not empty and is a valid number
        try:
            income_amount = float(income_amount)
            # Add the income amount to the income_entries list
            self.income = income_amount

            # Display a message box with the added income amount
            # print("Income Added", f"Income of {income_amount} has been added.")

            # Update the label with the added income amount
            self.income_display_label.config(text=f"Added income: {income_amount}")

            # Add income to the database
            # self.add_income_to_db(income_amount)
            self.db_handler.add_income(self.user_id, income_amount)

            # Clear the income entry field for new input
            self.income_entry.delete(0, tk.END)
        except ValueError:
            # Display an error message if the input is not a valid number
            messagebox.showerror("Invalid Input", "Please enter a valid number for income.")

    def add_expense(self):
        # Get the selected expense category and the expense amount
        category = self.expense_category.get()
        expense_amount = self.expense_entry.get()

        # Check if the category is selected and the amount is valid
        if category != "Select Category":
            try:
                expense_amount = float(expense_amount)

                # Check if adding the new expense will exceed the income
                if sum(self.expense_entries.values()) + expense_amount <= self.income:
                    # Check if the category already has an expense recorded
                    if category not in self.expense_entries:
                        # Add the expense to the dictionary
                        self.expense_entries[category] = expense_amount
                        # Update the expense display label
                        current_expense_text = self.expense_display_var.get()

                        # Add expense to the database
                        self.db_handler.add_expense(self.user_id, category, expense_amount)

                        new_expense_text = f"{current_expense_text}\n{category}: {expense_amount}"
                        self.expense_display_var.set(new_expense_text)
                        # messagebox.showinfo("Expense Added", f"{category} expense of {expense_amount} has been added.")
                    else:
                        messagebox.showwarning("Duplicate Entry", f"Expense for {category} has already been recorded.")
                else:
                    messagebox.showwarning("Exceeded Income",
                                           "Adding this expense will exceed the income. Please adjust.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for expense.")
        else:
            messagebox.showwarning("No Category Selected", "Please select an expense category.")

        # Clear the expense entry field for new input
        self.expense_entry.delete(0, tk.END)

    def generate_plan(self):
        # Call the external modules for analysis and plan generation
        analyze_expenses_and_income(self.income , self.expense_entries)
        generate_weekly_plan(self.expense_entries)

    def generate_plan_logged(self, income, expense_entries):
        # Call the external modules for analysis and plan generation
        analyze_expenses_and_income(income , expense_entries)
        generate_weekly_plan(self.expense_entries)

    def financial_education(self):
        pass

def deploy_main_app(user_id):
    # Create a DatabaseHandler instance
    db_handler = DatabaseHandler()

    root = tk.Tk()
    app = FinancialTracker(root, user_id, db_handler)
    root.mainloop()

