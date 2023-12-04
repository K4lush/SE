import tkinter as tk
from tkinter import ttk

def calculate_weekly_budget(income, plan_percentages):
    weekly_budgets = {category: income * percentage / 4 for category, percentage in plan_percentages.items()}
    return weekly_budgets

def generate_weekly_plan(income):
    def on_plan_selection(plan):
        plan_percentages = spending_plans[plan]

        # Calculate weekly budgets
        weekly_budgets = calculate_weekly_budget(income, plan_percentages)

        # Calculate daily budgets
        daily_budgets = {category: budget / 7 for category, budget in weekly_budgets.items()}

        # Create a new window for displaying results
        result_window = tk.Toplevel(root)
        result_window.title("Spending Plan Results")
        result_window.geometry("250x250")  # Set a larger window size

        # Display weekly budgets
        weekly_text = "Weekly Spending Plan:\n"
        for category, budget in weekly_budgets.items():
            weekly_text += f"{category.capitalize()}: ${budget:.2f}\n"

        # Display daily budgets
        daily_text = "\nThis means each day you can spend:\n"
        for category, budget in daily_budgets.items():
            daily_text += f"{category.capitalize()}: ${budget:.2f}\n"

        # Create labels for weekly and daily budgets in the new window
        weekly_label = ttk.Label(result_window, text=weekly_text, justify=tk.LEFT, font=("Arial", 12))
        daily_label = ttk.Label(result_window, text=daily_text, justify=tk.LEFT, font=("Arial", 12))

        # Pack the labels in the new window
        weekly_label.pack(pady=10)
        daily_label.pack(pady=10)

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

    # Function to create buttons and set their command
    def create_plan_button(plan):
        ttk.Button(
            root,
            text=f"{plan}",
            command=lambda p=plan: on_plan_selection(p)
        ).pack(side=tk.LEFT, padx=10)

    # Create buttons for each spending plan
    for plan in spending_plans:
        create_plan_button(plan)

    # Run the Tkinter event loop
    root.mainloop()


