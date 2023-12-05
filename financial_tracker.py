import tkinter as tk
from tkinter import ttk, messagebox
from income_expense_analyzer import analyze_expenses_and_income
from weekly_plan_generator import generate_weekly_plan
from financial_education import display_financial_education
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
        # Check if the user already has an entry in financial_data
        self.cursor.execute("SELECT * FROM financial_data WHERE user_id = ?", (user_id,))
        existing_entry = self.cursor.fetchone()

        if existing_entry:
            # Update the existing entry
            self.cursor.execute('UPDATE financial_data SET income = ? WHERE user_id = ?', (income_amount, user_id))
        else:
            # Insert a new entry
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
            self.display_main_menu_no_income()
        else:
            self.display_main_menu_logged()


    def display_main_menu_no_income(self):
        user_income = self.db_handler.get_income(self.user_id)

        if not user_income:
            # Generate Plan button
            generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan", command=self.generate_plan)
            generate_plan_button.grid(row=3, column=1, padx=10, pady=10)

            reset_expenses_button = tk.Button(self.root, text="Reset Expenses", command=self.reset_expenses)
            reset_expenses_button.grid(row=3, column=1, padx=10, pady=10)

            # Financial Education (Use Case)
            education_button = tk.Button(self.root, text="Financial Education", command=self.financial_education)
            education_button.grid(row=3, column=2, padx=10, pady=10)

            # Income section
            income_label = tk.Label(self.root, text="Monthly Income:")
            income_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

            self.income_entry = tk.Entry(self.root)
            self.income_entry.grid(row=0, column=1, padx=10, pady=10)

            add_income_button = tk.Button(self.root, text="Add Income", command=self.add_income)
            add_income_button.grid(row=0, column=2, padx=10, pady=10)

            # Label to display the added income
            self.income_display_label = tk.Label(self.root, text="No income added yet")
            self.income_display_label.grid(row=0, column=3, columnspan=2, padx=10, pady=10, sticky=tk.W)

            expense_label = tk.Label(self.root, text="Expense (Monthly Basis):")
            expense_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

            self.expense_display_var = tk.StringVar()
            self.expense_display_label = tk.Label(self.root, textvariable=self.expense_display_var)
            self.expense_display_label.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky=tk.W)

            # Dropdown menu for expense categories using Combobox
            expense_categories = ["Grocery", "Shopping", "Transportation", "Takeaways", "Night-outs"]
            self.expense_category = ttk.Combobox(self.root, values=expense_categories, state="readonly")
            self.expense_category.set("Select Category")  # default value
            self.expense_category.grid(row=1, column=2, padx=10, pady=10)

            self.expense_entry = tk.Entry(self.root)
            self.expense_entry.grid(row=1, column=1, padx=10, pady=10)

            add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
            add_expense_button.grid(row=1, column=3, padx=10, pady=10)


    def display_main_menu_logged(self):
         # Fetch expense entries from the database
         expenses_from_db = self.db_handler.get_expenses(self.user_id)

         # Fetch income from the database
         income_from_db = self.db_handler.get_income(self.user_id)

         # Update the expense_entries dictionary
         for expense in expenses_from_db:
             category, amount = expense[0], expense[1]
             self.expense_entries[category] = amount

         # Display income
         income_label = tk.Label(self.root, text=f"Income: {income_from_db}")
         income_label.grid(row=1, column=0, padx=1, pady=1, sticky=tk.W)

         # Display username
         income_label = tk.Label(self.root, text=f"Welcome back! {self.user_id}", font=('Helvetica', 20, 'bold'))
         income_label.grid(row=0, column=0, padx=3, pady=3, sticky=tk.W)

         # Edit Income button
         edit_income_button = tk.Button(self.root, text="Edit Income", command=self.edit_income)
         edit_income_button.grid(row=1, column=1, padx=10, pady=10, sticky=tk.W)

         # Display total expenses
         total_expenses = sum(self.expense_entries.values())
         expenses_label = tk.Label(self.root, text=f"This Months Expenses: {total_expenses}")
         expenses_label.grid(row=2, column=0, padx=1, pady=1, sticky=tk.W)

         # Edit Expenses button
         edit_expenses_button = tk.Button(self.root, text="Edit Expenses", command=self.edit_expenses)
         edit_expenses_button.grid(row=2, column=1, padx=10, pady=10, sticky=tk.W)

         # Generate Plan button
         generate_plan_button = tk.Button(self.root, text="Re-Analyse",
                                          command=lambda: self.generate_plan_logged(income_from_db,
                                                                                    self.expense_entries))
         generate_plan_button.grid(row=3, column=0, padx=10, pady=10)

         # Financial Education (Use Case)
         education_button = tk.Button(self.root, text="Financial Education", command=lambda: self.financial_education)
         education_button.grid(row=3, column=2, padx=10, pady=10)

    # Add the following method to the FinancialTracker class
    def edit_expenses(self):
        # Create a Toplevel window for editing expenses
        edit_expenses_window = tk.Toplevel(self.root)
        edit_expenses_window.title("Edit Expenses")

        # Label and entry for selecting expense category
        category_label = tk.Label(edit_expenses_window, text="Select Category:")
        category_label.grid(row=0, column=0, padx=10, pady=10)

        # Dropdown menu for expense categories using Combobox
        expense_categories = list(self.expense_entries.keys())
        category_var = tk.StringVar(value=expense_categories[0] if expense_categories else "")
        category_combobox = ttk.Combobox(edit_expenses_window, values=expense_categories, textvariable=category_var,
                                         state="readonly")
        category_combobox.grid(row=0, column=1, padx=10, pady=10)

        # Label and entry for entering new expense amount
        new_amount_label = tk.Label(edit_expenses_window, text="New Amount:")
        new_amount_label.grid(row=1, column=0, padx=10, pady=10)

        new_amount_entry = tk.Entry(edit_expenses_window)
        new_amount_entry.grid(row=1, column=1, padx=10, pady=10)

        # Initialize expense_display_var
        self.expense_display_var = tk.StringVar()

        # Button to update expense
        update_expense_button = tk.Button(edit_expenses_window, text="Update Expense",
                                          command=lambda: self.update_expense(category_combobox.get(),
                                                                              new_amount_entry.get(),
                                                                              edit_expenses_window))
        update_expense_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    # Add the following method to the FinancialTracker class
    def reset_expenses(self):
        # Clear the expense_entries dictionary
        self.expense_entries = {}

        # Clear the expense display label
        self.expense_display_var.set("")

        # Update the expense display label to show that expenses have been reset
        self.expense_display_label.config(text="Expenses have been reset.")

        # Clear expenses in the database
        self.db_handler.clear_expenses(self.user_id)

    # Add the following method to the FinancialTracker class
    def update_expense(self, category, new_amount, edit_expenses_window):
        try:
            new_amount = float(new_amount)

            # Calculate total expenses with the new expense
            total_expenses = sum(self.expense_entries.values()) + new_amount

            # Check if total expenses are less than or equal to income
            if total_expenses <= self.income:
                # Update expense in the dictionary
                self.expense_entries[category] = new_amount
                # Update the expense display label
                self.update_expense_display()
                # Update expense in the database
                self.db_handler.add_expense(self.user_id, category, new_amount)
                # Close the edit expenses window
                edit_expenses_window.destroy()
            else:
                messagebox.showerror("Invalid Input", "Expenses cannot be more than income.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for the new expense amount.")

    # Add the following method to the FinancialTracker class
    def update_expense_display(self):
        expense_text = ""
        for category, amount in self.expense_entries.items():
            expense_text += f"{category}: {amount:.2f}\n"
        self.expense_display_var.set(expense_text)

    def edit_income(self):
        # Create a Toplevel window for editing income
        edit_income_window = tk.Toplevel(self.root)
        edit_income_window.title("Edit Income")

        # Label and entry for new income
        new_income_label = tk.Label(edit_income_window, text="New Income:")
        new_income_label.grid(row=0, column=0, padx=10, pady=10)

        new_income_entry = tk.Entry(edit_income_window)
        new_income_entry.grid(row=0, column=1, padx=10, pady=10)

        # Button to update income
        update_income_button = tk.Button(edit_income_window, text="Update Income",
                                         command=lambda: self.update_income(new_income_entry.get(), edit_income_window))
        update_income_button.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Add the following method to the FinancialTracker class
    def update_income(self, new_income, edit_income_window):
        try:
            new_income = float(new_income)

            if 0 <= new_income <= 10000:  # Check if the new income is within the limit
                # Calculate total expenses
                total_expenses = sum(self.expense_entries.values())

                # Check if new income is greater than or equal to total expenses
                if new_income >= total_expenses:
                    # Update income in the database
                    self.db_handler.add_income(self.user_id, new_income)
                    # Close the edit income window
                    edit_income_window.destroy()
                    # Refresh the main window to display the updated income
                    self.root.destroy()
                    deploy_main_app(self.user_id)
                else:
                    messagebox.showerror("Invalid Input", "Income should be greater than or equal to total expenses.")
            else:
                messagebox.showwarning("Exceeded Limit", "Income cannot exceed $10,000.")
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number for income.")

    # Add the following method to the FinancialTracker class
    def add_income(self):
        # Get the income amount from the Entry widget
        income_amount = self.income_entry.get()

        # Check if the income amount is not empty and is a valid number
        try:
            income_amount = float(income_amount)

            # Add the income amount to the income_entries list
            if 0 <= income_amount <= 10000:  # Check if the income is within the limit
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
            else:
                messagebox.showwarning("Exceeded Limit", "Income cannot exceed $10,000.")
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
    def generate_plan2(self):
        generate_weekly_plan(self.expense_entries)

    def generate_plan_logged(self, income, expense_entries):
        # Call the external modules for analysis and plan generation
        analyze_expenses_and_income(income , expense_entries)

    def financial_education(self):
        display_financial_education()


def deploy_main_app(user_id):
    # Create a DatabaseHandler instance
    db_handler = DatabaseHandler()

    root = tk.Tk()
    app = FinancialTracker(root, user_id, db_handler)
    root.mainloop()

