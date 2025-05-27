from tkinter import *
from tkinter import messagebox
import mysql.connector
import signup
import user
import user_main

def call_umain(root):
    root.destroy()
    user_main.user_window()

def call_sign(root):
    root.destroy()
    signup.run_signup_app()

def call_user(root):
    root.destroy()
    user.user()

def run_login_app():
    def forget_password():
        def clear():
            user_name_entry.delete(0, END)
            new_password_entry.delete(0, END)
            c_password_entry.delete(0, END)

        def reset_password():
            if new_password_entry.get() == "" or c_password_entry.get() == "" or user_name_entry.get() == "":
                messagebox.showerror("Error", "All fields required!", parent=window)
            elif new_password_entry.get() != c_password_entry.get():
                messagebox.showerror("Error", "Password mismatch", parent=window)
            else:
                try:
                    con = mysql.connector.connect(host="localhost", user="root", password="Randhir@1#", database='userinfo')
                    mycursor = con.cursor()
                except:
                    messagebox.showerror("Error", "Database connection failed!", parent=window)
                    return
                query = "select * from user where username = %s"
                mycursor.execute(query, (user_name_entry.get(),))
                row = mycursor.fetchone()
                if row is None:
                    messagebox.showerror("Error", "Invalid username!", parent=window)
                else:
                    query = "UPDATE user SET password = %s WHERE username = %s"
                    mycursor.execute(query, (new_password_entry.get(), user_name_entry.get()))
                    con.commit()
                    messagebox.showinfo("Success", "Password updated", parent=window)
                    window.destroy()

        window = Toplevel()
        window.title("Reset Password")
        window.geometry("600x500")
        window.configure(bg="#263238")

        Label(window, text="🔒 RESET PASSWORD", font=("Segoe UI", 22, "bold"), fg="#FF6F00", bg="#263238").pack(pady=30)

        global user_name_entry, new_password_entry, c_password_entry
        entries = [
            ("Username", 130),
            ("New Password", 190),
            ("Confirm Password", 250)
        ]

        for label, y in entries:
            e = Entry(window, font=("Segoe UI", 14), width=25, bg="#37474F", fg="white", bd=0, insertbackground="white")
            e.place(x=180, y=y)
            e.insert(0, label)
            Frame(window, bg="#FF6F00", height=2, width=260).place(x=180, y=y+28)

            if label == "Username":
                user_name_entry = e
            elif label == "New Password":
                new_password_entry = e
            else:
                c_password_entry = e

        Button(window, text="Submit", font=("Segoe UI", 14, "bold"), bg="#FF6F00", fg="white",
               activebackground="#FFA040", activeforeground="white", cursor="hand2",
               width=20, bd=0, command=reset_password).place(x=180, y=320)

    def clear():
        user_name_entry.delete(0, END)
        password_entry.delete(0, END)

    def connect_to_database(root):
        if user_name_entry.get() == "" or password_entry.get() == "":
            messagebox.showerror("Error", "All fields are required!")
        else:
            try:
                con = mysql.connector.connect(host="localhost", user="root", password="Randhir@1#", database='userinfo')
                mycursor = con.cursor()
            except:
                messagebox.showerror("Error", "Database not connected!")
                return
            query = "select * from user where username = %s and password = %s"
            mycursor.execute(query, (user_name_entry.get(), password_entry.get()))
            row = mycursor.fetchone()
            if row is None:
                messagebox.showerror("Error", "Wrong username or password!")
                clear()
            else:
                messagebox.showinfo("Welcome", "Login successful!")
                clear()
                call_user(root)

    def on_focus_in(event, placeholder):
        widget = event.widget
        if widget.get() == placeholder:
            widget.delete(0, END)

    root = Tk()
    root.title("Login Portal")
    root.geometry("700x720")
    root.config(bg="#263238")

    # Title and icon
    Label(root, text="👤 LPG USER LOGIN", font=("Segoe UI", 28, "bold"), fg="#FF6F00", bg="#263238").pack(pady=40)

    # Entry Fields
    user_name_entry = Entry(root, font=("Segoe UI", 14), width=28, bg="#37474F", fg="white", bd=0, insertbackground="white")
    user_name_entry.insert(0, "Username")
    user_name_entry.bind("<FocusIn>", lambda e: on_focus_in(e, "Username"))
    user_name_entry.pack(pady=10)
    Frame(root, bg="#FF6F00", height=2, width=280).pack()

    password_entry = Entry(root, font=("Segoe UI", 14), width=28, bg="#37474F", fg="white", bd=0, insertbackground="white")
    password_entry.insert(0, "Password")
    password_entry.bind("<FocusIn>", lambda e: on_focus_in(e, "Password"))
    password_entry.pack(pady=20)
    Frame(root, bg="#FF6F00", height=2, width=280).pack()

    # Forgot Password
    Button(root, text="Forgot Password?", font=("Segoe UI", 10, "bold"), bg="#263238", fg="#FFA040",
           activebackground="#263238", activeforeground="#FFA040", bd=0, cursor="hand2",
           command=forget_password).pack(pady=10)

    # Login Button
    Button(root, text="LOGIN", font=("Segoe UI", 14, "bold"), bg="#FF6F00", fg="white",
           activebackground="#FFA040", activeforeground="white", cursor="hand2",
           width=23, bd=0, command=lambda: connect_to_database(root)).pack(pady=20)

    # OR Separator
    Label(root, text="──────────────  OR  ──────────────", font=("Segoe UI", 14), fg="white", bg="#263238").pack(pady=20)

    # Signup Text
    Label(root, text="Don't have an account?", font=("Segoe UI", 11, "bold"), fg="white", bg="#263238").pack(pady=5)

    Button(root, text="Create new one", font=("Segoe UI", 11, "underline"), fg="#29B6F6", bg="#263238",
           activebackground="#263238", activeforeground="#29B6F6", bd=0, cursor="hand2",
           command=lambda: call_sign(root)).pack(pady=10)

    # Back Button
    Button(root, text="Back", font=("Segoe UI", 11, "underline"), fg="#29B6F6", bg="#263238",
           activebackground="#263238", activeforeground="#29B6F6", bd=0, cursor="hand2",
           command=lambda: call_umain(root)).pack(pady=10)

    root.mainloop()
run_login_app()