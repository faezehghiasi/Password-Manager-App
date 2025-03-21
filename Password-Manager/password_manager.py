# password_manager.py
import tkinter as tk
from tkinter import ttk, messagebox
import db_manager
import secrets
import string
import pyperclip

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

def open_password_manager(back_target):
    manager = tk.Tk()
    manager.title("Password Manager - Saved Passwords")
    manager.geometry("600x450")
    manager.resizable(False, False)
    manager.configure(bg="#ADD8E6")

    style = create_style()

    container = ttk.Frame(manager, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    lbl_title = ttk.Label(container, text="🔑 Your Saved Passwords",
                          font=("Helvetica", 16, "bold"),
                          background="#ADD8E6")
    lbl_title.pack(pady=10)

    # Treeview را بیرون از container هم می‌توان ساخت، ولی برای هماهنگی با استایل، اینجا ساختیم
    tree = ttk.Treeview(container, columns=("Website", "Username", "Password"), show="headings")
    tree.heading("Website", text="Website")
    tree.heading("Username", text="Username")
    tree.heading("Password", text="Password")

    tree.column("Website", width=200)
    tree.column("Username", width=150)
    tree.column("Password", width=150)
    tree.pack(pady=10)

    passwords = db_manager.get_all_passwords()

    for pwd in passwords:
        website = pwd[1]
        username = pwd[2]
        tree.insert("", "end", values=(website, username, "******"))

    def copy_selected_password():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an entry!")
            return
        index_in_list = tree.index(selected_item[0])
        enc_pass = passwords[index_in_list][3]
        actual_pass = db_manager.decrypt_password(enc_pass)
        pyperclip.copy(actual_pass)
        messagebox.showinfo("Copied!", "Password copied to clipboard!")

    btn_copy = ttk.Button(container, text="📋 Copy Selected Password",
                          style='RoundedButton.TButton',
                          command=copy_selected_password)
    btn_copy.pack(pady=5)

    btn_add = ttk.Button(container, text="➕ Add New Password",
                         style='RoundedButton.TButton',
                         command=lambda: [manager.destroy(),
                                          add_new_password(back_target=lambda: open_password_manager(back_target))])
    btn_add.pack(pady=5)

    btn_back = ttk.Button(container, text="← Back",
                          style='RoundedButton.TButton',
                          command=lambda: [manager.destroy(), back_target()])
    btn_back.pack(pady=5)

    manager.mainloop()

def add_new_password(back_target):
    add_window = tk.Tk()
    add_window.title("Add Password")
    add_window.geometry("600x450")
    add_window.resizable(False, False)
    add_window.configure(bg="#ADD8E6")

    style = create_style()

    container = ttk.Frame(add_window, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    lbl_website = ttk.Label(container, text="Website:",
                            font=("Helvetica", 12),
                            background="#ADD8E6")
    lbl_website.pack(pady=5)
    website_entry = ttk.Entry(container, width=30, font=("Helvetica", 14))
    website_entry.pack(pady=5)

    lbl_username = ttk.Label(container, text="Username:",
                             font=("Helvetica", 12),
                             background="#ADD8E6")
    lbl_username.pack(pady=5)
    username_entry = ttk.Entry(container, width=30, font=("Helvetica", 14))
    username_entry.pack(pady=5)

    password_var = tk.StringVar()
    lbl_genpass = ttk.Label(container, text="Generated Password:",
                            font=("Helvetica", 12),
                            background="#ADD8E6")
    lbl_genpass.pack(pady=5)
    password_entry = ttk.Entry(container, width=30, textvariable=password_var,
                               state="readonly", font=("Helvetica", 14))
    password_entry.pack(pady=5)

    def generate_and_save():
        website = website_entry.get().strip()
        username = username_entry.get().strip()
        if not website or not username:
            messagebox.showerror("Error", "Please enter Website and Username!")
            return

        new_password = generate_password()
        password_var.set(new_password)
        pyperclip.copy(new_password)
        db_manager.save_password(website, username, new_password)
        messagebox.showinfo("Success", "Password copied and saved successfully!")
        add_window.destroy()
        back_target()

    btn_gen_save = ttk.Button(container, text="Generate & Save",
                              style='RoundedButton.TButton',
                              command=generate_and_save)
    btn_gen_save.pack(pady=10)

    btn_back = ttk.Button(container, text="← Back",
                          style='RoundedButton.TButton',
                          command=lambda: [add_window.destroy(), back_target()])
    btn_back.pack(pady=5)

    add_window.mainloop()

def generate_password(length=16):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))
