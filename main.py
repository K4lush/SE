import tkinter as tk
from tkinter import messagebox

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
        income_amount = self.income_entry.get()
        if income_amount:
            self.income_entries.append(float(income_amount))
            self.income_entry.delete(0, tk.END)

    def add_expense(self):
        expense_amount = self.expense_entry.get()
        if expense_amount:
            self.expense_entries.append(float(expense_amount))
            self.expense_entry.delete(0, tk.END)

    def generate_plan(self):
        total_income = sum(self.income_entries)
        total_expense = sum(self.expense_entries)

        weekly_plan = total_income - total_expense
        advice = "Spend wisely and save for the future."

        messagebox.showinfo("Weekly Plan", f"Your weekly plan: {weekly_plan}\n\nAdvice: {advice}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FinancialTracker(root)
    root.mainloop()
