import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path

from password_utils import generate_salt, hash_password
from crypto_utils import create_cipher
import db_manager

def _lazy_dashboard():
    import dashboard
    return dashboard


USER_FILE = Path('users.txt')

def _load_user_record(username: str):
    if not USER_FILE.exists():
        return None, None
    with USER_FILE.open() as f:
        for line in f:
            name, data = line.strip().split(':')
            if name == username:
                pw_hash, salt_hex = data.split('$')
                return pw_hash, bytes.fromhex(salt_hex)
    return None, None

def register_user(username: str, password: str) -> bool:
    if not username or not password:
        messagebox.showerror('Error', 'Username/password cannot be empty')
        return False
    pw_hash_existing, _ = _load_user_record(username)
    if pw_hash_existing:
        messagebox.showerror('Error', 'Username already exists')
        return False

    salt = generate_salt()
    pw_hash = hash_password(password, salt)
    with USER_FILE.open('a') as f:
        f.write(f"{username}:{pw_hash}${salt.hex()}\n")
    messagebox.showinfo('Registered', 'Registration successful – you can now log in')
    return True

def login_user(username: str, password: str) -> bool:
    pw_hash_saved, salt = _load_user_record(username)
    if not pw_hash_saved:
        messagebox.showerror('Error', 'User not found')
        return False
    if pw_hash_saved != hash_password(password, salt):
        messagebox.showerror('Error', 'Incorrect password')
        return False
    cipher = create_cipher(password, salt)
    db_manager.set_cipher(cipher)
    db_manager.set_owner(username)
    return True

def create_style():
    style = ttk.Style()
    style.theme_use('default')
    style.configure('.', background='#ADD8E6', font=('Helvetica', 14))
    style.configure('RoundedButton.TButton',
                    relief='flat', padding=10, borderwidth=0,
                    foreground='#fff', background='#1E90FF',
                    focusthickness=3, focuscolor='none')
    style.map('RoundedButton.TButton',
              background=[('active', '#1C86EE'), ('pressed', '#1C86EE')])
    return style

def open_welcome():
    root = tk.Tk()
    root.title('Password Manager – Welcome')
    root.geometry('600x450')
    root.resizable(False, False)
    root.configure(bg='#ADD8E6')
    create_style()

    container = ttk.Frame(root, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    ttk.Label(container, text='🔐 Welcome', font=('Helvetica', 18, 'bold'),
              background='#ADD8E6').pack(pady=10)

    ttk.Label(container, text='Username:', background='#ADD8E6').pack()
    user_entry = ttk.Entry(container, width=30, font=('Helvetica', 14))
    user_entry.pack(pady=5)

    ttk.Label(container, text='Master Password:', background='#ADD8E6').pack()
    pass_entry = ttk.Entry(container, width=30, font=('Helvetica', 14), show='*')
    pass_entry.pack(pady=5)

    def handle_login():
        u = user_entry.get().strip()
        p = pass_entry.get().strip()
        if login_user(u, p):
            messagebox.showinfo('Success', 'Login successful')
            root.destroy()
            _lazy_dashboard().open_dashboard()

    def open_register_window():
        reg = tk.Toplevel(root)
        reg.title('Register')
        reg.geometry('400x300')
        reg.configure(bg='#ADD8E6')
        create_style()

        ttk.Label(reg, text='Register', font=('Helvetica', 16, 'bold'),
                  background='#ADD8E6').pack(pady=10)
        ttk.Label(reg, text='Username:', background='#ADD8E6').pack()
        r_user = ttk.Entry(reg, width=25, font=('Helvetica', 12))
        r_user.pack(pady=5)
        ttk.Label(reg, text='Master Password:', background='#ADD8E6').pack()
        r_pass = ttk.Entry(reg, width=25, font=('Helvetica', 12), show='*')
        r_pass.pack(pady=5)

        def do_reg():
            if register_user(r_user.get().strip(), r_pass.get().strip()):
                reg.destroy()

        ttk.Button(reg, text='Register', style='RoundedButton.TButton',
                   command=do_reg).pack(pady=15)

    ttk.Button(container, text='Login', style='RoundedButton.TButton',
               command=handle_login).pack(pady=10)

    ttk.Button(container, text='Register',
               style='RoundedButton.TButton',
               command=open_register_window).pack(pady=5)

    root.mainloop()

if __name__ == '__main__':
    open_welcome()
