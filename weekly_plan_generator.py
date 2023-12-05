import tkinter as tk
from tkinter import ttk

def calculate_weekly_budget(income, plan_percentages):
    weekly_budgets = {category: income * percentage / 4 for category, percentage in plan_percentages.items()}
    return weekly_budgets

def calculate_savings(income, spending_percentage):
    return income * (1 - spending_percentage)

def generate_weekly_plan(income):
    def on_plan_selection(plan):

        for widget in root.winfo_children():
            if isinstance(widget, ttk.Frame):
                widget.destroy()


        plan_percentages = spending_plans[plan]

        # Calculate the total spending percentage for the plan
        total_spending_percentage = sum(plan_percentages.values())

        # Calculate the savings percentage
        savings_percentage = 1 - total_spending_percentage

        # Calculate weekly budgets
        weekly_budgets = calculate_weekly_budget(income, plan_percentages)

        # Calculate daily budgets
        daily_budgets = {category: budget / 7 for category, budget in weekly_budgets.items()}

        # Calculate savings
        savings = calculate_savings(income, total_spending_percentage)

        # Update the existing window for displaying results
        result_frame = ttk.Frame(root)
        result_frame.pack(pady=10)

        # Display weekly budgets
        weekly_label = ttk.Label(result_frame, text="Your Weekly Spending Plan:", font=("Arial", 14, 'bold'))
        weekly_label.pack(padx=10, pady=10)
        for category, budget in weekly_budgets.items():
            budget_label = ttk.Label(result_frame, text=f"{category.capitalize()}: ${budget:.2f}", font=("Arial", 12))
            budget_label.pack(padx=10)

        # Display daily budgets
        daily_label = ttk.Label(result_frame, text="\nYour Daily Spending:", font=("Arial", 14, 'bold'))
        daily_label.pack(padx=10, pady=10)
        for category, budget in daily_budgets.items():
            budget_label = ttk.Label(result_frame, text=f"{category.capitalize()}: ${budget:.2f}", font=("Arial", 12))
            budget_label.pack(padx=10)

        # Display savings
        savings_label = ttk.Label(result_frame, text=f"\nYou are saving: ${savings:.2f} weekly",
                                  font=("Arial", 14, 'bold'))
        savings_label.pack(padx=10, pady=10)

        # # Create labels for weekly, daily budgets, and savings in the existing window
        # weekly_label = ttk.Label(result_frame, text=weekly_text, justify=tk.LEFT, font=("Arial", 12))
        # daily_label = ttk.Label(result_frame, text=daily_text, justify=tk.LEFT, font=("Arial", 12))
        # savings_label = ttk.Label(result_frame, text=savings_text, justify=tk.LEFT, font=("Arial", 12))

        # Pack the labels in the existing window
        weekly_label.pack(padx= 10, pady=10)
        daily_label.pack(padx= 10, pady=10)
        savings_label.pack(padx= 10, pady=10)

    # Define spending plans with fixed percentages for each category
    spending_plans = {
        'Budget Friendly Plan': {'Grocery': 0.3, 'Shopping': 0.1, 'Transportation': 0.2, 'Takeaways': 0.05, 'Night-outs': 0.05},
        'Normal Plan': {'Grocery': 0.2, 'Shopping': 0.2, 'Transportation': 0.2, 'Takeaways': 0.1, 'Night-outs': 0.1},
        'Excessive Plan': {'Grocery': 0.2, 'Shopping': 0.2, 'Transportation': 0.1, 'Takeaways': 0.2, 'Night-outs': 0.2}
    }

    # Create the main window
    root = tk.Tk()
    root.title("Weekly Spending Plan")

    ttk.Label(root, text="Choose a Spending Plan:").pack(pady=10)

    # Create buttons for each spending plan
    for plan in spending_plans:
        ttk.Button(
            root,
            text=f"{plan}",
            command=lambda p=plan: on_plan_selection(p)
        ).pack(pady=5)

    # Run the Tkinter event loop
    root.mainloop()
