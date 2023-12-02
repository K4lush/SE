from tkinter import messagebox

def generate_weekly_plan(income_entries, expense_entries):
    total_income = sum(income_entries)
    total_expense = sum(expense_entries)

    weekly_plan = total_income - total_expense
    advice = "Spend wisely and save for the future."

    messagebox.showinfo("Weekly Plan", f"Your weekly plan: {weekly_plan}\n\nAdvice: {advice}")
