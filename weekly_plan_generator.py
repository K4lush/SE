import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg


def generate_weekly_plan(expense_values):
    # Hardcoded values for each day
    daily_expenses = {
        "Food": [0, 0.25, 0.15, 0, 0.2, 0, 0.4],  # Monday to Sunday
        "Essentials": [0.1, 0.2, 0.15, 0.2, 0.1, 0.1, 0.1],
        "Shopping": [0.2, 0.1, 0.2, 0.1, 0.1, 0.2, 0.1]
    }

    # Advice messages for each day
    advice_messages = {
        0: 'Relax and recharge! This is your day where you should gather your finances and analyze what spending you have to do for the week.',
        # Sunday
        1: 'Start of the week! Start your week with your weekly shop for groceries.',  # Monday
        2: 'Restock some essentials today.',  # Tuesday
        3: 'No specific advice for today.',  # Wednesday
        4: 'Almost there! Plan for some shopping today.',  # Thursday
        5: 'Treat yourself today! You made it to the end of the week.',  # Friday
        6: 'Enjoy the weekend! Plan for weekend activities and expenses.'  # Saturday
    }

    # Create the main window
    root = tk.Tk()
    root.title("Weekly Expense Plan")

    # Set a themed style
    style = ttk.Style(root)
    style.theme_use("clam")

    # Create a canvas to draw on the background
    canvas = tk.Canvas(root, width=800, height=600)
    canvas.pack()

    # Draw some shapes on the canvas
    canvas.create_rectangle(0, 0, 800, 600, fill="#F0F0F0", outline="#F0F0F0")  # Background
    canvas.create_rectangle(50, 50, 750, 550, fill="#FFFFFF", outline="#000000")  # Main frame

    # Create a calendar-like grid for the week
    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    result_texts = [""] * 7
    result_text_widgets = [tk.Text(root, height=8, width=25, wrap=tk.WORD) for _ in range(7)]
    edit_buttons = [tk.Button(root, text="Edit", command=lambda i=i: edit_expenses(i), font=('Helvetica', 12)) for i in
                    range(7)]

    for i, day in enumerate(days_of_week):
        # Day box
        canvas.create_rectangle(50 + i * 100, 50, 150 + i * 100, 550, fill="#EDEDED", outline="#000000")

        # Day label
        canvas.create_text(125 + i * 100, 70, text=day, font=('Helvetica', 12, 'bold'))  # Day labels

        # Text widget for each day
        canvas.create_window(125 + i * 100, 275, window=result_text_widgets[i])

        # Button for each day
        canvas.create_window(125 + i * 100, 450, window=edit_buttons[i])

        result_text_widgets[i].configure(state=tk.DISABLED,
                                         font=('Helvetica', 9))  # Disable user interaction with the text widget

    # Display the result in a readable format
    def update_result():
        for i, day in enumerate(daily_expenses["Food"]):
            result_texts[i] = f"{day * 100:.0f}%:\n"  # Format as percentage
            for category, expenses in expense_values.items():
                expense = daily_expenses[category][i] * expenses
                result_texts[i] += f"{category.capitalize()}: {expense:.2f}\n"

            result_texts[i] += f"\nAdvice - {advice_messages[i]}\n\n"
            result_text_widgets[i].configure(state=tk.NORMAL)  # Enable user interaction with the text widget
            result_text_widgets[i].delete(1.0, tk.END)
            result_text_widgets[i].insert(tk.END, result_texts[i])
            result_text_widgets[i].configure(state=tk.DISABLED)  # Disable user interaction with the text widget

    # Edit the expenses or the advice messages for a given day
    def edit_expenses(day):
        # Create a new window for editing
        edit_window = tk.Toplevel(root)
        edit_window.title(f"Edit Expenses for {days_of_week[day]}")

        # Create some labels and sliders for each category of expenses
        tk.Label(edit_window, text="Adjust your expenses!", font=('Helvetica', 14, 'bold')).grid(
            row=0, column=0, columnspan=2, padx=10, pady=10)

        tk.Label(edit_window, text="Food:").grid(row=1, column=0, sticky=tk.E, padx=10, pady=10)
        tk.Label(edit_window, text="Essentials:").grid(row=2, column=0, sticky=tk.E, padx=10, pady=10)
        tk.Label(edit_window, text="Shopping:").grid(row=3, column=0, sticky=tk.E, padx=10, pady=10)

        food_slider = tk.Scale(edit_window, from_=0, to=100, orient=tk.HORIZONTAL)
        food_slider.grid(row=1, column=1, sticky=tk.W, padx=10, pady=10)
        food_slider.set(daily_expenses["Food"][day] * 100)  # Set the initial value

        essentials_slider = tk.Scale(edit_window, from_=0, to=100, orient=tk.HORIZONTAL)
        essentials_slider.grid(row=2, column=1, sticky=tk.W, padx=10, pady=10)
        essentials_slider.set(daily_expenses["Essentials"][day] * 100)  # Set the initial value

        shopping_slider = tk.Scale(edit_window, from_=0, to=100, orient=tk.HORIZONTAL)
        shopping_slider.grid(row=3, column=1, sticky=tk.W, padx=10, pady=10)
        shopping_slider.set(daily_expenses["Shopping"][day] * 100)  # Set the initial value

        # Create a label for the adjustment sliders
        tk.Label(edit_window, text="Adjustment of expense based on percentage:", font=('Helvetica', 10, 'italic')).grid(
            row=4, column=0, columnspan=2, padx=10, pady=10)

        # Create a label and a text widget for the advice message
        tk.Label(edit_window, text="Enter the new advice message:", font=('Helvetica', 14, 'bold')).grid(row=5,
                                                                                                         column=0,
                                                                                                         columnspan=2,
                                                                                                         padx=10,
                                                                                                         pady=10)
        advice_text = tk.Text(edit_window, height=5, width=40, wrap=tk.WORD)
        advice_text.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
        advice_text.insert(tk.END, advice_messages[day])

        # Function to update the values when the "Save" button is clicked
        def save_values():
            try:
                # Update the values for each category of expenses
                daily_expenses["Food"][day] = food_slider.get() / 100.0
                daily_expenses["Essentials"][day] = essentials_slider.get() / 100.0
                daily_expenses["Shopping"][day] = shopping_slider.get() / 100.0

                # Update the advice message
                advice_messages[day] = advice_text.get(1.0, tk.END).strip()

                # Update the result display in the main window
                update_result()

                # Close the editing window
                edit_window.destroy()

            except ValueError:
                msg.showerror("Invalid Input", "Please enter valid numerical values for expenses.")

        # Create a "Save" button to save the changes
        tk.Button(edit_window, text="Save", command=save_values, font=('Helvetica', 14)).grid(row=7, column=0,
                                                                                              columnspan=2, pady=10)

    # Update the result initially
    update_result()

    # Run the main loop
    root.mainloop()

# Example usage:
# generate_weekly_plan({"Food": 100, "Essentials": 50, "Shopping": 75})
