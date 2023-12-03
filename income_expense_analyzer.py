import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def analyze_expenses_and_income(income, expense_entries):
    '''
    Analyzes the user's monthly income and expenses, categorizing expenses and calculating savings.
    Then displays the analysis in a Tkinter window.

    :param income: The monthly income of the user as a float.
    :param expense_entries: A dictionary consisting of different categories where each value is the amount that
    corresponds to a different key which is a category.
    :return: None
    '''

    # Calculate total expenses
    total_expenses = sum(expense_entries.values())

    # Calculate savings
    savings = income - total_expenses

    # Determine the percentage of income spent on each category
    expense_percentages = {category: (amount / income) * 100 for category, amount in expense_entries.items()}

    # Identify the highest expense category
    highest_expense_category = max(expense_entries, key=expense_entries.get)

    # Create the main window
    root = tk.Tk()
    root.title("Expense Analysis")

    # # Display each category with its percentage
    for category, percentage in expense_percentages.items():
        tk.Label(root, text=f"{category}: {percentage:.2f}%").pack()

    # Display the results
    tk.Label(root, text=f"Total Income: {income}").pack()
    tk.Label(root, text=f"Total Expenses: {total_expenses}").pack()
    tk.Label(root, text=f"Savings: {savings}").pack()
    tk.Label(root, text=f"Highest Expense Category: {highest_expense_category}").pack()

    # Pie chart for expense distribution
    fig1, ax1 = plt.subplots()
    ax1.pie(expense_entries.values(), labels=expense_entries.keys(), autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1_widget = canvas1.get_tk_widget()
    canvas1_widget.pack()

    # Run the application
    root.mainloop()

