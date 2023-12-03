import tkinter as tk
from tkinter import messagebox
from income_expense_analyzer import analyze_expenses_and_income
from weekly_plan_generator import generate_weekly_plan

class FinancialTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tracker")


        # Initialize variables
        self.income_entries = []
        self.expense_entries = []

        # Create GUI elements
        self.create_widgets()

        # Initialize expense_entries as a dictionary
        self.expense_entries = {}

    def create_widgets(self):

        # Generate Plan button
        generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan", command=self.generate_plan)
        generate_plan_button.grid(row=2, column=1, padx=10, pady=10)

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
            self.income_entries.append(income_amount)

            # Display a message box with the added income amount
            print("Income Added", f"Income of {income_amount} has been added.")

            # Update the label with the added income amount
            self.income_display_label.config(text=f"Added income: {income_amount}")

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
                # Check if the category already has an expense recorded
                if category not in self.expense_entries:
                    # Add the expense to the dictionary
                    self.expense_entries[category] = expense_amount
                    messagebox.showinfo("Expense Added", f"{category} expense of {expense_amount} has been added.")
                else:
                    messagebox.showwarning("Duplicate Entry", f"Expense for {category} has already been recorded.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number for expense.")
        else:
            messagebox.showwarning("No Category Selected", "Please select an expense category.")

        # Clear the expense entry field for new input
        self.expense_entry.delete(0, tk.END)

    def generate_plan(self):
        # Call the external modules for analysis and plan generation
        analyze_expenses_and_income(self.income_entries, self.expense_entries)
        generate_weekly_plan(self.income_entries, self.expense_entries)


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialTracker(root)
    root.mainloop()
