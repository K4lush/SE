import tkinter as tk
from tkinter import messagebox
import sqlite3
from financial_tracker import deploy

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserDatabaseManager:
    def __init__(self, db_name='user_database.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_user(self, user):
        self.cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (user.username, user.password))
        self.conn.commit()

    def check_credentials(self, username, password):
        self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
        return self.cursor.fetchone() is not None

    def user_exists(self, username):
        self.cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        return self.cursor.fetchone() is not None

class AuthenticationApp:
    def __init__(self, root, db_manager):
        self.root = root
        self.db_manager = db_manager
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

        if self.db_manager.check_credentials(username, password):
            self.root.destroy()
            deploy()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    def signup(self):
        username = self.signup_username_entry.get()
        password = self.signup_password_entry.get()

        if self.db_manager.user_exists(username):
            messagebox.showerror("Signup Failed", "Username already exists")
        else:
            new_user = User(username, password)
            self.db_manager.add_user(new_user)
            messagebox.showinfo("Signup Successful", "Account created successfully. Please login.")

# Create the main application window and database manager
root = tk.Tk()
db_manager = UserDatabaseManager()

# Pass the database manager to the AuthenticationApp
app = AuthenticationApp(root, db_manager)

root.mainloop()

# Close the database connection after the main loop exits
db_manager.conn.close()
