import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from weekly_plan_generator import generate_weekly_plan

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

    # Display each category with its percentage using grid
    row_num = 0
    for category, percentage in expense_percentages.items():
        tk.Label(root, text=f"{category}:", padx=10).grid(row=row_num, column=0, sticky="w")
        tk.Label(root, text=f"{percentage:.2f}%", padx=10).grid(row=row_num, column=1, sticky="e")
        row_num += 1

    # Display the results using grid
    tk.Label(root, text="Total Income:", padx=10).grid(row=row_num, column=0, sticky="w")
    tk.Label(root, text=f"{income}", padx=10).grid(row=row_num, column=1, sticky="e")
    row_num += 1

    tk.Label(root, text="Total Expenses:", padx=10).grid(row=row_num, column=0, sticky="w")
    tk.Label(root, text=f"{total_expenses}", padx=10).grid(row=row_num, column=1, sticky="e")
    row_num += 1

    tk.Label(root, text="Savings:", padx=10).grid(row=row_num, column=0, sticky="w")
    tk.Label(root, text=f"{savings}", padx=10).grid(row=row_num, column=1, sticky="e")
    row_num += 1

    tk.Label(root, text="Highest Expense Category:", padx=10).grid(row=row_num, column=0, sticky="w")
    tk.Label(root, text=f"{highest_expense_category}", padx=10).grid(row=row_num, column=1, sticky="e")
    row_num += 1

    # Generate Weekly Plan button
    def generate_plan_callback():
        generate_weekly_plan(income)

    generate_plan_button = tk.Button(root, text="Generate Weekly Plan", command=generate_plan_callback)
    generate_plan_button.grid(row=row_num, columnspan=2, pady=10)

    row_num += 1

    # Pie chart for expense distribution
    fig1, ax1 = plt.subplots()
    ax1.pie(expense_entries.values(), labels=expense_entries.keys(), autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    canvas1 = FigureCanvasTkAgg(fig1, master=root)
    canvas1_widget = canvas1.get_tk_widget()
    canvas1_widget.grid(row=row_num, columnspan=2)

    # Run the application
    root.mainloop()
