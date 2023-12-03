import tkinter as tk
from tkinter import messagebox
from income_expense_analyzer import analyze_expenses_and_income
from weekly_plan_generator import generate_weekly_plan
from financial_education import display_financial_education

class FinancialTracker:
    def __init__(self, root, current_user):
        self.root = root
        self.root.title("Financial Tracker")
        self.current_user = current_user


        # Initialize variables
        self.income = 0.0
        self.expense_entries = {}

        # Create GUI elements
        self.show_form()


    def show_form(self):
        # Generate Plan button
        generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan", command=self.generate_plan)
        generate_plan_button.grid(row=3, column=1, padx=10, pady=10)

        # Financial Education (Use Case)
        education_button = tk.Button(self.root, text="Financial Educatinon", command=self.generate_financial_advice)
        education_button.grid(row=3, column=2, padx=10, pady=10)

        # added code
        # Income section
        income_label = tk.Label(self.root, text="Income:")
        income_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)


        # Income section
        self.income_entry = tk.Entry(self.root)
        self.income_entry.grid(row=0, column=1, padx=10, pady=10)

        add_income_button = tk.Button(self.root, text="Add Income", command=self.add_income)
        add_income_button.grid(row=0, column=2, padx=10, pady=10)

        # Label to display the added income
        self.income_display_label = tk.Label(self.root, text="No income added yet")
        self.income_display_label.grid(row=0, column=3, columnspan=2, padx=10, pady=10, sticky=tk.W)

        # Expense section
        expense_label = tk.Label(self.root, text="Expense:")
        expense_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        # Label to dynamically display added expenses
        self.expense_display_var = tk.StringVar()
        self.expense_display_label = tk.Label(self.root, textvariable=self.expense_display_var)
        self.expense_display_label.grid(row=2, column=1, sticky=tk.W)

        # Dropdown menu for expense categories
        self.expense_category = tk.StringVar(self.root)
        self.expense_category.set("Select Category")  # default value
        expense_categories = ["Food", "Essentials", "Shopping"]
        expense_dropdown = tk.OptionMenu(self.root, self.expense_category, *expense_categories)
        expense_dropdown.grid(row=1, column=2, padx=10, pady=10)

        self.expense_entry = tk.Entry(self.root)
        self.expense_entry.grid(row=1, column=1, padx=10, pady=10)

        add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        add_expense_button.grid(row=1, column=3, padx=10, pady=10)



    def add_income(self):
        # Get the income amount from the Entry widget
        income_amount = self.income_entry.get()

        # Check if the income amount is not empty and is a valid number
        try:
            income_amount = float(income_amount)

            # Add the income amount to the income_entries list
            self.current_user.income = income_amount

            # Update the label with the added income amount
            self.income_display_label.config(text=f"Added income: {income_amount}")

            # # Update the user's income in the database
            # self.update_user_income()

            # Clear the income entry field for new input
            self.income_entry.delete(0, tk.END)
        except ValueError:
            # Display an error message if the input is not a valid number
            messagebox.showerror("Invalid Input", "Please enter a valid number for income.")

    # def update_user_income(self):
    #     # Update the user's income in the database
    #     self.db_manager.cursor.execute('UPDATE users SET income=? WHERE username=?',
    #                                    (self.current_user.income, self.current_user.username))
    #     self.db_manager.conn.commit()

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



    def generate_financial_advice(self):
        display_financial_education(self.income)

# #
# if __name__ == "__main__":
#     root = tk.Tk()
#     app = FinancialTracker(root)
#     root.mainloop()


def deploy(current_user):
    root = tk.Tk()
    app = FinancialTracker(root, current_user)
    root.mainloop()




