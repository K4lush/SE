import tkinter as tk
from tkinter import ttk

def display_financial_education():
    # Replace this with your actual logic for financial education
    advice_list = [
        "Create a budget to track your spending.",
        "Save at least 20% of your income.",
        "Spend on low-cost groceries like LIDL, ALDI.",
        "Avoid unnecessary impulse purchases.",
        "Consider investing for long-term financial goals."
    ]

    # Display financial advice in the text widget
    education_text.configure(state=tk.NORMAL)
    education_text.delete(1.0, tk.END)
    for advice in advice_list:
        education_text.insert(tk.END, f"• {advice}\n")
    education_text.configure(state=tk.DISABLED)

# Create the main window
root = tk.Tk()
root.title("Financial Advice")

# Text widget to display financial advice
education_text = tk.Text(root, height=10, width=40, wrap=tk.WORD)
education_text.grid(row=0, column=0, pady=10)

# Call the function to display financial advice
display_financial_education()

# Start the Tkinter event loop
root.mainloop()
