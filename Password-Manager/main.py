# main.py

import tkinter as tk
from tkinter import ttk, messagebox
import os
import db_manager
import hashlib
import binascii

USERS_FILE = "users.txt"
LOGIN_ATTEMPTS = {}  # دیکشنری برای محدود کردن تلاش‌های ورود

def generate_user_hash(password: str) -> str:

    import os
    salt = os.urandom(16)
    key = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return binascii.hexlify(salt + key).decode()

def check_user_hash(stored_str: str, provided: str) -> bool:

    stored_bytes = binascii.unhexlify(stored_str)
    salt = stored_bytes[:16]
    key = stored_bytes[16:]
    new_key = hashlib.pbkdf2_hmac("sha256", provided.encode("utf-8"), salt, 100_000)
    return new_key == key

def create_style():

    style = ttk.Style()
    style.theme_use('default')


    style.configure('.', background='#ADD8E6', font=('Helvetica', 14))

    style.configure('RoundedButton.TButton',
                    relief='flat',
                    padding=10,
                    borderwidth=0,
                    foreground='#fff',
                    background='#1E90FF',
                    focusthickness=3,
                    focuscolor='none')
    style.map('RoundedButton.TButton',
              background=[('active', '#1C86EE'), ('pressed', '#1C86EE')])

    return style

def open_welcome():
    root = tk.Tk()
    root.title("Password Manager - Welcome")
    root.geometry("600x450")
    root.resizable(False, False)
    root.configure(bg="#ADD8E6")

    style = create_style()

    container = ttk.Frame(root, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    label = ttk.Label(container, text="👋 Welcome!", style='TLabel')
    label.configure(font=("Helvetica", 18, "bold"), background="#ADD8E6")
    label.pack(pady=20)

    btn_signup = ttk.Button(container, text="Sign Up",
                            style='RoundedButton.TButton',
                            command=lambda: [root.destroy(), open_signup()])
    btn_signup.pack(pady=10)

    btn_login = ttk.Button(container, text="Log In",
                           style='RoundedButton.TButton',
                           command=lambda: [root.destroy(), open_login()])
    btn_login.pack(pady=10)

    root.mainloop()

def open_signup():
    signup_win = tk.Tk()
    signup_win.title("Password Manager - Sign Up")
    signup_win.geometry("600x450")
    signup_win.resizable(False, False)
    signup_win.configure(bg="#ADD8E6")

    style = create_style()

    container = ttk.Frame(signup_win, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    label = ttk.Label(container, text="Sign Up",
                      font=("Helvetica", 16, "bold"),
                      background="#ADD8E6")
    label.pack(pady=10)

    signup_username = ttk.Entry(container, font=("Helvetica", 14))
    signup_username.pack(pady=5, padx=30, ipadx=5, ipady=5)
    add_placeholder(signup_username, "Username")

    signup_password = ttk.Entry(container, font=("Helvetica", 14))
    signup_password.pack(pady=5, padx=30, ipadx=5, ipady=5)
    add_placeholder(signup_password, "Password", is_password=True)

    signup_confirm = ttk.Entry(container, font=("Helvetica", 14))
    signup_confirm.pack(pady=5, padx=30, ipadx=5, ipady=5)
    add_placeholder(signup_confirm, "Confirm Password", is_password=True)

    btn_register = ttk.Button(container, text="Register",
                              style='RoundedButton.TButton',
                              command=lambda: register_user(signup_username,
                                                            signup_password,
                                                            signup_confirm,
                                                            signup_win))
    btn_register.pack(pady=10)

    btn_back = ttk.Button(container, text="← Back",
                          style='RoundedButton.TButton',
                          command=lambda: [signup_win.destroy(), open_welcome()])
    btn_back.pack()

    signup_win.mainloop()

def open_login():
    login_win = tk.Tk()
    login_win.title("Password Manager - Log In")
    login_win.geometry("600x450")
    login_win.resizable(False, False)
    login_win.configure(bg="#ADD8E6")

    style = create_style()

    container = ttk.Frame(login_win, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    label = ttk.Label(container, text="Log In",
                      font=("Helvetica", 16, "bold"),
                      background="#ADD8E6")
    label.pack(pady=10)

    login_username = ttk.Entry(container, font=("Helvetica", 14))
    login_username.pack(pady=5, padx=30, ipadx=5, ipady=5)
    add_placeholder(login_username, "Username")

    login_password = ttk.Entry(container, font=("Helvetica", 14))
    login_password.pack(pady=5, padx=30, ipadx=5, ipady=5)
    add_placeholder(login_password, "Password", is_password=True)

    btn_login = ttk.Button(container, text="Log In",
                           style='RoundedButton.TButton',
                           command=lambda: login_user(login_username,
                                                      login_password,
                                                      login_win))
    btn_login.pack(pady=10)

    btn_back = ttk.Button(container, text="← Back",
                          style='RoundedButton.TButton',
                          command=lambda: [login_win.destroy(), open_welcome()])
    btn_back.pack()

    login_win.mainloop()

def add_placeholder(entry_widget, text, is_password=False):
    def on_focus_in(event):
        if entry_widget.get() == text:
            entry_widget.delete(0, tk.END)
            entry_widget.config(foreground="black", show="*" if is_password else "")
    def on_focus_out(event):
        if entry_widget.get() == "":
            entry_widget.insert(0, text)
            entry_widget.config(foreground="grey", show="")
    entry_widget.insert(0, text)
    entry_widget.config(foreground="grey", show="")
    entry_widget.bind("<FocusIn>", on_focus_in)
    entry_widget.bind("<FocusOut>", on_focus_out)

def register_user(username_entry, password_entry, confirm_entry, current_win):
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm = confirm_entry.get().strip()

    if username == "Username" or password == "Password" or confirm == "Confirm Password":
        messagebox.showwarning("Error", "Please fill in all fields!")
        return

    if password != confirm:
        messagebox.showerror("Error", "Passwords do not match!")
        return

    hashed_pass = generate_user_hash(password)
    try:
        with open(USERS_FILE, "a") as f:
            f.write(f"{username}:{hashed_pass}\n")
    except Exception as e:
        messagebox.showerror("File Error", f"Error saving user data: {str(e)}")
        return

    messagebox.showinfo("Success", "Account created! You can now log in.")
    current_win.destroy()
    open_login()

def login_user(username_entry, password_entry, current_win):
    username = username_entry.get().strip()
    password = password_entry.get().strip()

    if username == "Username" or password == "Password":
        messagebox.showerror("Error", "Please enter your credentials!")
        return

    if LOGIN_ATTEMPTS.get(username, 0) >= 3:
        messagebox.showerror("Login Blocked", "Too many failed attempts. Please try again later.")
        return

    if not os.path.exists(USERS_FILE):
        messagebox.showerror("Error", "No users found. Please sign up first!")
        return

    try:
        with open(USERS_FILE, "r") as f:
            users = f.readlines()
    except Exception as e:
        messagebox.showerror("File Error", f"Error reading user data: {str(e)}")
        return

    for user_line in users:
        user_line = user_line.strip()
        if not user_line:
            continue
        try:
            u, hsh = user_line.split(":")
        except ValueError:
            continue  
        if u == username:
            if check_user_hash(hsh, password):
                messagebox.showinfo("Login Successful", f"Welcome back, {username}!")
                LOGIN_ATTEMPTS[username] = 0
                current_win.destroy()
                from dashboard import open_dashboard  
                open_dashboard()
                return
            else:
                LOGIN_ATTEMPTS[username] = LOGIN_ATTEMPTS.get(username, 0) + 1
                tries_left = 3 - LOGIN_ATTEMPTS[username]
                if tries_left <= 0:
                    messagebox.showerror("Login Blocked", "Too many failed attempts. Please try again later.")
                else:
                    messagebox.showerror("Login Failed", f"Invalid password! {tries_left} attempts left.")
                return

    messagebox.showerror("Login Failed", "Invalid username or password!")
    LOGIN_ATTEMPTS[username] = LOGIN_ATTEMPTS.get(username, 0) + 1

if __name__ == "__main__":
    db_manager.init_db()
    open_welcome()
