from tkinter import *
import tkinter as tk
import login
import haveconn

def call_have(root):
    root.destroy()
    haveconn.have_conn()

def call_login(root):
    root.destroy()
    login.run_login_app()

def user_window():
    # Create the main window
    root = tk.Tk()
    root.title("LPG Management System")
    root.geometry("500x400")
    root.configure(bg='#E8F6F3')  # Soft pastel background

    # Title label
    title_label = tk.Label(
        root,
        text="Welcome to LPG Portal",
        font=("Helvetica", 22, "bold"),
        bg="#E8F6F3",
        fg="#2C3E50"
    )
    title_label.pack(pady=40)

    # Button style
    button_style = {
        "bg": "#ffffff",
        "fg": "#007FFF",
        "activebackground": "#D6EAF8",
        "activeforeground": "#007FFF",
        "font": ("Helvetica", 14, "bold"),
        "bd": 2,
        "relief": "ridge",
        "cursor": "hand2",
        "width": 20,
        "height": 2
    }

    # Get Connection Button
    get_connection_button = tk.Button(
        root,
        text="Get New Connection",
        command=lambda: call_login(root),
        **button_style
    )
    get_connection_button.pack(pady=15)

    # Have Connection Button
    have_connection_button = tk.Button(
        root,
        text="Already Have Connection",
        command=lambda: call_have(root),
        **button_style
    )
    have_connection_button.pack(pady=10)

    # Footer label (optional)
    footer = tk.Label(
        root,
        text="© 2025 GasCorp",
        font=("Helvetica", 10),
        bg="#E8F6F3",
        fg="#7F8C8D"
    )
    footer.pack(side="bottom", pady=15)

    root.mainloop()
