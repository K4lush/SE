import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.messagebox as msg
# import pyscreenshot

def generate_weekly_plan(expense_values):
    # Hardcoded values for each day percentage of usage decided by system
    daily_expenses = {
        "Food": [0.15, 0.2, 0.15, 0.15, 0.15, 0.25, 0.1],  # Monday to Sunday, increased on Friday
        "Essentials": [0.1, 0.15, 0.1, 0.15, 0.2, 0.15, 0.15],
        "Shopping": [0.15, 0.1, 0.15, 0.1, 0.15, 0.2, 0.1]
    }

    # Ensure that the total expenses for each day do not exceed the expense values
    for day in range(7):
        total_expense = sum(daily_expenses[category][day] * expense_values[category] for category in expense_values)
        scaling_factor = 1.0
        if total_expense > expense_values["Food"]:
            scaling_factor = expense_values["Food"] / total_expense
        for category in expense_values:
            daily_expenses[category][day] *= scaling_factor

    # Advice messages for each day
    advice_messages = {
        0: 'Relax and recharge! This is your day where you should gather your finances and analyze what spending you have to do for the week.',
        # Sunday
        1: 'Start of the week! Start your week with your weekly shop for groceries.',  # Monday
        2: 'Restock some essentials today. Make sure to use your groceries to cook for today even try meal prepping!',  # Tuesday
        3: 'Midweek, finalize the use of your groceries that you bought on Monday and restock on some more today.',  # Wednesday
        4: 'Almost there! Plan for some shopping today. Also make use of the time and grab some essentials today as well',  # Thursday
        5: 'Treat yourself today! You made it to the end of the week, enjoy a takeaway today with your food! Make sure to stock on any essentials again.',  # Friday
        6: 'Enjoy the weekend! Plan for weekend activities and expenses.'  # Saturday
    }

    # Create the main window
    root = tk.Tk()
    root.title("Weekly Expense Plan")

    # Set a themed style
    style = ttk.Style(root)
    style.theme_use("clam")

    # Create a canvas to draw on the background
    canvas = tk.Canvas(root, width=1245, height=380, bg="#FFFFFF")
    canvas.pack()

    # Display the expense information
    expense_label = tk.Label(root, text="This calendar displays how much you should spend on each day based on your provided expenses and taking into consideration your income.",
                             font=('Helvetica', 10), wraplength=1000, justify="center")
    canvas.create_window(625, 20, window=expense_label)

    # Create a calendar-like grid for the week
    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    result_text_widgets = [tk.Text(root, height=7, width=25, wrap=tk.WORD) for _ in range(7)]
    advice_widgets = [tk.Text(root, height=7, width=25, wrap=tk.WORD) for _ in range(7)]

    # Use a loop to create the day boxes, labels, text widgets
    for i, day in enumerate(days_of_week):
        # Day label
        canvas.create_text(90 + i * 180, 100, text=day, font=('Helvetica', 12, 'bold'))

        # Text widget for each day (expenses)
        canvas.create_window(100 + i * 175, 180, window=result_text_widgets[i])

        # Text widget for each day (advice)
        canvas.create_window(100 + i * 175, 230, window=advice_widgets[i])

        result_text_widgets[i].configure(state=tk.DISABLED, font=('Helvetica', 9))
        advice_widgets[i].configure(state=tk.DISABLED, font=('Helvetica', 9))

    # Display the result in a readable format
    def update_result():
        for i, day in enumerate(daily_expenses["Food"]):
            for category, expenses in expense_values.items():
                expense = daily_expenses[category][i] * expenses
                result_text_widgets[i].configure(state=tk.NORMAL)
                result_text_widgets[i].insert(tk.END, f"{category.capitalize()}: {expense:.2f}\n")
                result_text_widgets[i].configure(state=tk.DISABLED)

    # Display the advice messages
    def update_advice():
        for i in range(7):
            advice_widgets[i].configure(state=tk.NORMAL)
            advice_widgets[i].insert(tk.END, advice_messages[i])
            advice_widgets[i].configure(state=tk.DISABLED)

    def save_plan_to_file():
        try:
            # Get the file path from the user
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

            # Ensure the user selected a file
            if file_path:
                with open(file_path, 'w') as file:
                    # Write the header
                    file.write("Weekly Expense Plan\n\n")

                    # Write the expense information
                    file.write(
                        "This calendar displays how much you should spend on each day based on your provided expenses and taking into consideration your income.\n\n")

                    # Create a calendar-like grid for the week
                    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

                    for i, day in enumerate(days_of_week):
                        # Day label
                        file.write(f"{day}:\n")

                        # Write the expenses for each day
                        for category, expenses in expense_values.items():
                            expense = daily_expenses[category][i] * expenses
                            file.write(f"  {category.capitalize()}: {expense:.2f}\n")

                        # Write the advice for each day
                        file.write(f"  Advice: {advice_messages[i]}\n")

                        file.write("\n")

                msg.showinfo("Plan Saved", "Weekly plan saved successfully!")
        except Exception as e:
            msg.showerror("Error", f"An error occurred while saving the plan:\n{str(e)}")

    # Add a "Save Plan" button to the main window
    save_plan_button = tk.Button(root, text="Save Plan", command=save_plan_to_file, font=('Helvetica', 12))
    canvas.create_window(650, 360, window=save_plan_button)  # Positioned at the bottom

    # Update the result initially
    update_result()
    # Update the advice initially
    update_advice()

    # Run the main loop
    root.mainloop()

# Example usage:
# generate_weekly_plan({"Food": 80, "Essentials": 30, "Shopping": 75})
