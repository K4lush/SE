import tkinter as tk
from tkinter import messagebox
import sqlite3

# Create a SQLite database and a table for user information
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
''')
conn.commit()

def start():
    # Replace this with the code to launch your financial tracker
    print("Financial Tracker launched!")

class AuthenticationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Authentication App")
        self.root.geometry("400x300")  # Set a fixed size for the window

        # Create frames for login and signup forms
        self.login_frame = tk.Frame(root, bg="#f0f0f0")
        self.signup_frame = tk.Frame(root, bg="#f0f0f0")

        # Set up login form
        self.create_login_form()

        # Set up signup form
        self.create_signup_form()

        # Show login form initially
        self.show_login_form()

    def create_login_form(self):
        self.login_label = tk.Label(self.login_frame, text="Login", font=('Helvetica', 20), bg="#f0f0f0", fg="#333")
        self.login_label.pack(pady=10)

        self.login_username_label = tk.Label(self.login_frame, text="Username:", bg="#f0f0f0", fg="#333")
        self.login_username_label.pack()
        self.login_username_entry = tk.Entry(self.login_frame, bg="white", fg="#333")
        self.login_username_entry.pack(pady=5)

        self.login_password_label = tk.Label(self.login_frame, text="Password:", bg="#f0f0f0", fg="#333")
        self.login_password_label.pack()
        self.login_password_entry = tk.Entry(self.login_frame, show="*", bg="white", fg="#333")
        self.login_password_entry.pack(pady=10)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="#4CAF50", fg="white", relief=tk.GROOVE)
        self.login_button.pack(pady=10)

        self.signup_link = tk.Label(self.login_frame, text="Don't have an account? Signup here", fg="#007BFF", cursor="hand2", bg="#f0f0f0")
        self.signup_link.pack()
        self.signup_link.bind("<Button-1>", lambda e: self.show_signup_form())

    def create_signup_form(self):
        self.signup_label = tk.Label(self.signup_frame, text="Signup", font=('Helvetica', 20), bg="#f0f0f0", fg="#333")
        self.signup_label.pack(pady=10)

        self.signup_username_label = tk.Label(self.signup_frame, text="Username:", bg="#f0f0f0", fg="#333")
        self.signup_username_label.pack()
        self.signup_username_entry = tk.Entry(self.signup_frame, bg="white", fg="#333")
        self.signup_username_entry.pack(pady=5)

        self.signup_password_label = tk.Label(self.signup_frame, text="Password:", bg="#f0f0f0", fg="#333")
        self.signup_password_label.pack()
        self.signup_password_entry = tk.Entry(self.signup_frame, show="*", bg="white", fg="#333")
        self.signup_password_entry.pack(pady=10)

        self.signup_button = tk.Button(self.signup_frame, text="Signup", command=self.signup, bg="#007BFF", fg="white", relief=tk.GROOVE)
        self.signup_button.pack(pady=10)

        self.login_link = tk.Label(self.signup_frame, text="Already have an account? Login here", fg="#007BFF", cursor="hand2", bg="#f0f0f0")
        self.login_link.pack()
        self.login_link.bind("<Button-1>", lambda e: self.show_login_form())

    def show_login_form(self):
        self.signup_frame.pack_forget()
        self.login_frame.pack()

    def show_signup_form(self):
        self.login_frame.pack_forget()
        self.signup_frame.pack()

    def login(self):
        username = self.login_username_entry.get()
        password = self.login_password_entry.get()

        # Check if the username and password match the database
        cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        if cursor.fetchone():
            messagebox.showinfo("Login Successful", "Welcome, {}".format(username))
            # Open a new window on successful login
            self.open_welcome_window(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()

        # Check if the username already exists in the database
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        if cursor.fetchone():
            messagebox.showerror("Signup Failed", "Username already exists")
        else:
            # Insert the new user into the database
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            messagebox.showinfo("Signup Successful", "Account created successfully. Please login.")

    def open_welcome_window(self, username):
        welcome_window = tk.Toplevel(self.root)
        welcome_window.title("Welcome")
        welcome_window.geometry("300x100")  # Set a fixed size for the welcome window
        welcome_label = tk.Label(welcome_window, text=f"Hello, {username}! Welcome to the application.", font=('Helvetica', 14))
        welcome_label.pack(padx=20, pady=20)

        # Redirect to main.py
        start()  # Call the main function to launch the financial tracker

# Create the main application window
root = tk.Tk()
app = AuthenticationApp(root)
root.mainloop()

# Close the database connection after the main loop exits
conn.close()
