

from tkinter import *
from tkinter import messagebox
import mysql.connector
import login

def call_login(root1):
    root1.destroy()
    login.run_login_app()

def run_signup_app():
   
    def clear():
        email_entry.delete(0, END)
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        cPassword_entry.delete(0, END)

    def connect_database():
        if email_entry.get() == "" or password_entry.get() == "" or username_entry.get() == "" or cPassword_entry.get() == "":
            messagebox.showerror("Error", "All fields are required!")
        elif password_entry.get() != cPassword_entry.get():
            messagebox.showerror("Error", "Password mismatch!")
        else:
            try:
                con = mysql.connector.connect(host='localhost', user='root', password='Randhir@1#', database='userinfo')
                mycursor = con.cursor()
            except:
                messagebox.showerror("Error", "Not connected to database!")
                return

            query = "select * from user where username = %s"
            mycursor.execute(query, (username_entry.get(),))
            row = mycursor.fetchone()
            if row is not None:
                messagebox.showerror("Error", "Username already exists!")
                clear()
            else:
                mycursor.execute('insert into user (email, username, password) values (%s, %s, %s)', (
                    email_entry.get(),
                    username_entry.get(),
                    password_entry.get(),
                ))
                con.commit()
                con.close()
                messagebox.showinfo("Success", "Account created")
                clear()



    # Initialize the root window
    root1 = Tk()
    root1.title("Sign up")
    root1.geometry("1080x681")
    root1.resizable(0, 0)
    root1.configure(bg='#A6D7DB')

    # Create and place widgets
    title = Label(root1, text="CREATE NEW ACCOUNT", font=("Arial", 24, "bold"), bg='#A6D7DB')
    title.place(relx=0.5, rely=0.1, anchor="center")

    email_label = Label(root1, text="Email", font=("Arial", 15), bg='#A6D7DB')
    email_label.place(relx=0.5, rely=0.2, anchor="center")
    email_entry = Entry(root1, width=30, font=("Arial", 15))
    email_entry.place(relx=0.5, rely=0.27, anchor="center")

    username_label = Label(root1, text="Username", font=("Arial", 15), bg='#A6D7DB')
    username_label.place(relx=0.5, rely=0.33, anchor="center")
    username_entry = Entry(root1, width=30, font=("Arial", 15))
    username_entry.place(relx=0.5, rely=0.4, anchor="center")

    password_label = Label(root1, text="Password", font=("Arial", 15), bg='#A6D7DB')
    password_label.place(relx=0.5, rely=0.47, anchor="center")
    password_entry = Entry(root1, width=30, font=("Arial", 15), show="*")
    password_entry.place(relx=0.5, rely=0.54, anchor="center")

    cPassword_label = Label(root1, text="Confirm Password", font=("Arial", 15), bg='#A6D7DB')
    cPassword_label.place(relx=0.5, rely=0.61, anchor="center")
    cPassword_entry = Entry(root1, width=30, font=("Arial", 15), show="*")
    cPassword_entry.place(relx=0.5, rely=0.68, anchor="center")

    register_button = Button(root1, text="Signup", bg='#A6D7DB', fg="#007FFF", font=("Arial", 15, "bold"), command=connect_database)
    register_button.place(relx=0.5, rely=0.81, anchor="center")

    da_label = Label(root1, text="Already have an account?", font=("Arial", 11, "bold"), bg='#A6D7DB')
    da_label.place(relx=0.5, rely=0.87, anchor="center")

    ca_button = Button(root1, text="Login", bg="#A6D7DB", fg="blue", font=("Arial", 11, "underline"), command=lambda: call_login(root1))
    ca_button.place(relx=0.5, rely=0.9, anchor="center")

    root1.mainloop()
