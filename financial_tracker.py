import tkinter as tk
from tkinter import messagebox
from income_expense_analyzer import analyze_expenses_and_income
from weekly_plan_generator import generate_weekly_plan

print("hello")

class FinancialTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Tracker")

        # Initialize variables
        self.income_entries = []
        self.expense_entries = []

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Income section
        # ... (existing code)

        # Expense section
        # ... (existing code)

        # Generate Plan button
        generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan", command=self.generate_plan)
        generate_plan_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        # added code
        # Income section
        income_label = tk.Label(self.root, text="Income:")
        income_label.grid(row=0, column=0, padx=10, pady=10, sticky=tk.W)

        self.income_entry = tk.Entry(self.root)
        self.income_entry.grid(row=0, column=1, padx=10, pady=10)

        add_income_button = tk.Button(self.root, text="Add Income", command=self.add_income)
        add_income_button.grid(row=0, column=2, padx=10, pady=10)

        # Expense section
        expense_label = tk.Label(self.root, text="Expense:")
        expense_label.grid(row=1, column=0, padx=10, pady=10, sticky=tk.W)

        self.expense_entry = tk.Entry(self.root)
        self.expense_entry.grid(row=1, column=1, padx=10, pady=10)

        add_expense_button = tk.Button(self.root, text="Add Expense", command=self.add_expense)
        add_expense_button.grid(row=1, column=2, padx=10, pady=10)

        # Generate Plan button
        generate_plan_button = tk.Button(self.root, text="Generate Weekly Plan", command=self.generate_plan)
        generate_plan_button.grid(row=2, column=0, columnspan=3, padx=10, pady=10)
    def add_income(self):
        # ... (existing code)
        pass

    def add_expense(self):
        # ... (existing code)
        pass

    def generate_plan(self):
        # Call the external modules for analysis and plan generation
        analyze_expenses_and_income(self.income_entries, self.expense_entries)
        generate_weekly_plan(self.income_entries, self.expense_entries)


if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialTracker(root)
    root.mainloop()
