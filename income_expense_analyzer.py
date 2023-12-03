def analyze_expenses_and_income(income, expense_entries):
    '''
    Analyzes the user's monthly income and expenses, categorizing expenses and calculating savings.

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

    # Output the analysis
    print(f"Total Income: {income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Savings: {savings}")
    print(f"Expense Percentages: {expense_percentages}")
    print(f"Highest Expense Category: {highest_expense_category}")

    print("Analysis completed.")

