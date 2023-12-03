import tkinter as tk
from tkinter import ttk

def display_financial_education(income):
    advice_list = [
        "Create a budget to track your spending and set financial goals.",
        "Save at least 20% of your income in a dedicated savings account.",
        "Shop smart by choosing budget-friendly options for groceries and essentials.",
        "Avoid unnecessary impulse purchases by making a shopping list and sticking to it.",
        "Consider investing in diverse assets for long-term financial growth.",
        "Review and optimize your expenses regularly to identify potential savings.",
        "Build an emergency fund to cover unexpected expenses and ensure financial stability.",
        "Educate yourself about personal finance and stay informed about economic trends.",
        "Negotiate bills and explore ways to lower your fixed expenses.",
        "Stay disciplined and patient – financial success is a journey, not a sprint."
    ]

    # Create a new window for financial advice
    advice_window = tk.Toplevel()
    advice_window.title("Financial Advice")
    advice_window.geometry("800x600")

    # Center the window on the screen
    screen_width = advice_window.winfo_screenwidth()
    screen_height = advice_window.winfo_screenheight()
    x_coordinate = (screen_width - 800) // 2
    y_coordinate = (screen_height - 600) // 2
    advice_window.geometry(f"800x600+{x_coordinate}+{y_coordinate}")

    # Header
    header_label = ttk.Label(advice_window, text="Unlock Your Financial Freedom!", font=("Helvetica", 20, "bold"))
    header_label.pack(pady=20)

    # Create a canvas for scrolling
    canvas = tk.Canvas(advice_window)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Add a scrollbar to the canvas
    scrollbar = ttk.Scrollbar(advice_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas
    scroll_frame = ttk.Frame(canvas)
    canvas.create_window((0, 0), window=scroll_frame, anchor=tk.NW)

    # Income Section
    income_frame = ttk.Frame(scroll_frame, padding=10, relief="groove")
    income_frame.pack(pady=20)

    income_label = ttk.Label(income_frame, text=f"Your Income: ${income:,.2f}", font=("Helvetica", 16))
    income_label.grid(row=0, column=0, pady=10)

    # Tips Section
    tips_frame = ttk.Frame(scroll_frame, padding=10, relief="groove")
    tips_frame.pack(pady=20)

    tips_label = ttk.Label(tips_frame, text="Tips to Increase Income and Save:", font=("Helvetica", 16, "bold"))
    tips_label.grid(row=0, column=0, pady=5)

    increase_income_text = tk.Text(tips_frame, height=3, width=70, wrap=tk.WORD, font=("Arial", 12))
    increase_income_text.grid(row=1, column=0, pady=5)
    increase_income_text.insert(tk.END, "1. Explore opportunities for career advancement.\n"
                                       "2. Consider acquiring new skills or certifications.\n"
                                       "3. Investigate part-time or freelance opportunities.")

    save_money_text = tk.Text(tips_frame, height=3, width=70, wrap=tk.WORD, font=("Arial", 12))
    save_money_text.grid(row=2, column=0, pady=5)
    save_money_text.insert(tk.END, "1. Identify unnecessary expenses and cut them.\n"
                                   "2. Find ways to reduce utility bills.\n"
                                   "3. Look for discounts and use coupons when shopping.")

    # Budgeting Goals Section
    budgeting_frame = ttk.Frame(scroll_frame, padding=10, relief="groove")
    budgeting_frame.pack(pady=20)

    budgeting_label = ttk.Label(budgeting_frame, text="Add your budgeting goals:", font=("Helvetica", 16))
    budgeting_label.grid(row=0, column=0, pady=10)

    budgeting_text = tk.Text(budgeting_frame, height=3, width=70, wrap=tk.WORD, font=("Arial", 12))
    budgeting_text.grid(row=1, column=0, pady=5)

    # Advice Section
    advice_frame = ttk.Frame(scroll_frame, padding=10, relief="groove")
    advice_frame.pack(pady=20)

    advice_text = tk.Text(advice_frame, height=15, width=70, wrap=tk.WORD, font=("Arial", 12))
    advice_text.grid(row=0, column=0, pady=10)

    advice_text.configure(state=tk.NORMAL)
    for index, advice in enumerate(advice_list, start=1):
        advice_text.insert(tk.END, f"{index}. {advice}\n\n")
    advice_text.configure(state=tk.DISABLED)

    # Configure scrolling region
    scroll_frame.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

# Create the main window
# main_window = tk.Tk()
# main_window.title("Feature-rich Financial Advice")
#
# # Center the window on the screen
# screen_width = main_window.winfo_screenwidth()
# screen_height = main_window.winfo_screenheight()
# x_coordinate = (screen_width - 300) // 2
# y_coordinate = (screen_height - 100) // 2
# main_window.geometry(f"300x100+{x_coordinate}+{y_coordinate}")
#
# # Button to open the financial advice GUI
# open_button = ttk.Button(main_window, text="Open Financial Advice", command=lambda: display_financial_education(50000))
# open_button.pack(pady=30)
#
# # Start the Tkinter event loop
# main_window.mainloop()
