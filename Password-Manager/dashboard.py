import tkinter as tk
from tkinter import ttk
from password_manager import open_password_manager, add_new_password
import main

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

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Password Manager - Dashboard")
    dashboard.geometry("600x450")
    dashboard.resizable(False, False)
    dashboard.configure(bg="#ADD8E6")

    style = create_style()

    container = ttk.Frame(dashboard, padding=20, style='TFrame')
    container.place(relx=0.5, rely=0.5, anchor='center')

    lbl_title = ttk.Label(container, text="🔐 Password Manager",
                          font=("Helvetica", 18, "bold"),
                          background="#ADD8E6")
    lbl_title.pack(pady=20)

    btn_generate = ttk.Button(container,
                              text="➕ Generate Password",
                              style='RoundedButton.TButton',
                              width=25,
                              command=lambda: [dashboard.destroy(), add_new_password(back_target=open_dashboard)])
    btn_generate.pack(pady=10)

    btn_view = ttk.Button(container,
                          text="📂 View Saved Passwords",
                          style='RoundedButton.TButton',
                          width=25,
                          command=lambda: [dashboard.destroy(), open_password_manager(back_target=open_dashboard)])
    btn_view.pack(pady=10)

    btn_logout = ttk.Button(container,
                            text="← Logout",
                            style='RoundedButton.TButton',
                            width=25,
                            command=lambda: [dashboard.destroy(), main.open_welcome()])
    btn_logout.pack(pady=10)

    dashboard.mainloop()
