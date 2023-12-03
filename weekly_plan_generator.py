import tkinter as tk
from tkinter import ttk
import calendar

def generate_weekly_plan(expense_values):
    # Hardcoded values for each day
    daily_expenses = {
        "Food": [0, 0.25, 0.15, 0, 0.2, 0, 0.4],  # Monday to Sunday
        "Essentials": [0.1, 0.2, 0.15, 0.2, 0.1, 0.1, 0.1],
        "Shopping": [0.2, 0.1, 0.2, 0.1, 0.1, 0.2, 0.1]
    }

    # Advice messages for each day
    advice_messages = {
        0: 'Relax and recharge! This is your day where you should gather your finances and analyze what spending you have to do for the week.',    # Sunday
        1: 'Start of the week! Start your week with your weekly shop for groceries.',     # Monday
        2: 'Restock some essentials today.',          # Tuesday
        3: 'No specific advice for today.',         # Wednesday
        4: 'Almost there! Plan for some shopping today.',          # Thursday
        5: 'Treat yourself today! You made it to the end of the week.',  # Friday
        6: 'Enjoy the weekend! Plan for weekend activities and expenses.'      # Saturday
    }

    # Create the main window
    root = tk.Tk()
    root.title("Weekly Expense Plan")

    # Set a themed style
    style = ttk.Style(root)
    style.theme_use("clam")

    # Create a calendar-like grid for the week
    days_of_week = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

    result_texts = [""] * 7
    result_text_widgets = [tk.Text(root, height=8, width=25, wrap=tk.WORD) for _ in range(7)]

    for i, day in enumerate(days_of_week):
        tk.Label(root, text=day, relief=tk.GROOVE, width=25, font=('Helvetica', 10, 'bold')).grid(row=1, column=i, padx=5, pady=5)
        result_text_widgets[i].grid(row=2, column=i, padx=5, pady=5)
        result_text_widgets[i].configure(state=tk.DISABLED, font=('Helvetica', 9))  # Disable user interaction with the text widget

    # Display the result in a readable format
    for i, day in enumerate(daily_expenses["Food"]):
        result_texts[i] = f"{day}:\n"
        for category, expenses in expense_values.items():
            expense = daily_expenses[category][i] * expenses
            result_texts[i] += f"{category.capitalize()}: {expense:.2f}\n"

        result_texts[i] += f"\nAdvice - {advice_messages[i]}\n\n"
        result_text_widgets[i].configure(state=tk.NORMAL)  # Enable user interaction with the text widget
        result_text_widgets[i].delete(1.0, tk.END)
        result_text_widgets[i].insert(tk.END, result_texts[i])
        result_text_widgets[i].configure(state=tk.DISABLED)  # Disable user interaction with the text widget

    # Start the Tkinter event loop
    root.mainloop()

