from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import tkinter as tk
import re
from tkinter import ttk
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime, timedelta
from mysql.connector import Error
import user_main
def impuser():
    user_main.user_window()
def backimp(root):
    root.destroy()
    user_main.user_window()
def user():
    
    def generate_customer_number():
        return str(random.randint(100000, 999999))

    def create_connection():
        try:
            connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Randhir@1#",
                database="userinfo"
            )
            return connection
        except Error as e:
            print(f"Error creating connection: {e}")
            return None

    def create_user_details_table():
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS user_detail (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        customer_number VARCHAR(6),
                        name VARCHAR(255),
                        lpg_type VARCHAR(20),
                        dob VARCHAR(20),
                        father_name VARCHAR(255),
                        mother_name VARCHAR(255),
                        address VARCHAR(255),
                        pincode VARCHAR(255),
                        contact_number VARCHAR(20)
                    );
                ''')
                connection.commit()
                print("Table 'user_details' created successfully.")
            except Error as e:
                print(f"Error creating table: {e}")
            finally:
                cursor.close()
                connection.close()

    def validate_input(char):
        if char.isalpha() or char == " ":
            entry_name.config(bg="white")
            return True
        else:
            entry_name.config(bg="red")
            messagebox.showinfo("Invalid Input", "Please enter only alphabets.", parent=root)
            return False

    def validate_father(char):
        if char.isalpha() or char == " ":
            entry_father_name.config(bg="white")
            return True
        else:
            entry_father_name.config(bg="red")
            messagebox.showinfo("Invalid Input", "Please enter only alphabets.", parent=root)
            return False
    def validate_address(char):
        if re.match(r"^[a-zA-Z0-9\s\-\/]*$", char):
            entry_address_user.config(bg="white")
            return True
        else:
            entry_address_user.config(bg="red")
            messagebox.showinfo("Invalid Input", "Address cannot contain special characters except '-', '/'.", parent=root)
            return False
    def validate_mother(char):
        if char.isalpha() or char == " ":
            entry_mother_name.config(bg="white")
            return True
        else:
            entry_mother_name.config(bg="red")
            messagebox.showinfo("Invalid Input", "Please enter only alphabets.", parent=root)
            return False

    def validate_pincode(char):
        pincode = entry_pincode_user.get() + char
        if pincode.isdigit() and len(pincode) <= 6 or char == "":
            if len(pincode) == 6:
                entry_pincode_user.config(bg="white")
            return True
        else:
            entry_pincode_user.config(bg="red")
            messagebox.showinfo("Invalid Input", "Pincode must be a 6-digit number.", parent=root)
            return False

    def validate_contact(char):
        current_input = entry_contact_user.get()
        if char.isdigit() and ((current_input == "" and char in "6789") or current_input != ""):
            new_input = current_input
            if len(new_input) <= 10:
                entry_contact_user.config(bg="white")
            if len(new_input) == 10:
                # Final validation when input length is 10
                return True
            return True
        entry_contact_user.config(bg="red")
        messagebox.showinfo("Invalid Input", "Please enter a valid contact number starting with 6, 7, 8, or 9 and exactly 10 digits long.", parent=root)
        return False

    def validate_fields():
        valid = True

        # Validate LPG Cylinder Type
        lpg_type = combo_lpg_type_user.get()
        if lpg_type not in ["Domestic", "Commercial"]:
            messagebox.showinfo("Invalid Input", "Please select a valid LPG Cylinder Type.", parent=root)
            valid = False

        # Validate Date of Birth
        dob = entry_dob.get()
        if not dob:
            messagebox.showinfo("Invalid Input", "Please enter a valid Date of Birth.", parent=root)
            valid = False

        # Validate Father's Name
        father_name = entry_father_name.get()
        if not father_name.isalpha():
            messagebox.showinfo("Invalid Input", "Please enter a valid Father's Name (only alphabets).")
            valid = False

        # Validate Mother's Name
        mother_name = entry_mother_name.get()
        if not mother_name.isalpha():
            messagebox.showinfo("Invalid Input", "Please enter a valid Mother's Name (only alphabets).")
            valid = False

        # Validate Address
        address = entry_address_user.get()
        if not address:
            messagebox.showinfo("Invalid Input", "Please enter a valid Address.")
            valid = False

        # Validate Contact Number
        contact_number = entry_contact_user.get()
        if not contact_number.isdigit() or len(contact_number) != 10:
            messagebox.showinfo("Invalid Input", "Please enter a valid 10-digit Contact Number.")
            valid = False

        return valid

    def check_user_exists():
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                query = '''
                    SELECT * FROM user_detail
                    WHERE name = %s OR father_name = %s OR mother_name = %s
                '''
                data = (entry_name.get(), entry_father_name.get(), entry_mother_name.get())

                cursor.execute(query, data)
                result = cursor.fetchone()

                if result:
                    return True
                return False

            except Error as e:
                print(f"Error executing query: {e}")
            finally:
                cursor.close()
                connection.close()

    def submit_user_form():
        if not validate_fields():
            # Validation failed, do not proceed with the submission
            return
        
        if check_user_exists():
            messagebox.showinfo("Duplicate Entry", "User already exists with the same Name, Father's Name, or Mother's Name.")
            impuser()
            return
        
        connection = create_connection()
        if connection:
            try:
                cursor = connection.cursor()

                # Your SQL query to insert data into the database
                query = '''
                    INSERT INTO user_detail(customer_number, name, lpg_type, dob, father_name, mother_name, address, pincode,  contact_number)
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s)
                '''

                # Data to be inserted
                data = (
                    generate_customer_number(),
                    entry_name.get(),
                    combo_lpg_type_user.get(),
                    entry_dob.get(),
                    entry_father_name.get(),
                    entry_mother_name.get(),
                    entry_address_user.get(),
                    entry_pincode_user.get(),
                    entry_contact_user.get()
                )

                # Execute the query
                cursor.execute(query, data)

                # Commit the changes
                connection.commit()
                success_window = Toplevel()
                success_window.title("Success")
                success_window.geometry("200x200")
                success_window.configure(bg='#A6D7DB')
                success_label = Label(success_window, text="Connection successful")
                success_label.pack(pady=20)
                print("Data inserted successfully")

                # Retrieve customer_number from the database
                cursor.execute("SELECT customer_number FROM user_detail WHERE name = %s", (entry_name.get(),))
                customer_number = cursor.fetchone()[0]

                # Save the data to a PDF file
                save_to_pdf(data, customer_number)

                # Clear the form fields
                entry_name.delete(0, tk.END)
                combo_lpg_type_user.set('')
                entry_dob.delete(0, tk.END)
                entry_father_name.delete(0, tk.END)
                entry_mother_name.delete(0, tk.END)
                entry_address_user.delete(0, tk.END)
                entry_contact_user.delete(0, tk.END)
                entry_pincode_user.delete(0, tk.END)

            except Error as e:
                print(f"Error executing query: {e}")
            finally:
                cursor.close()
                connection.close()

    def save_to_pdf(data, customer_number):
        user_name = data[1]
        filename = f"{user_name}_{customer_number}_User_Form_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"

        pdf_canvas = canvas.Canvas(filename)
        pdf_canvas.drawString(100, 820, f"Customer Number: {customer_number}")
        pdf_canvas.drawString(100, 800, "User Details Form")
        pdf_canvas.drawString(100, 780, "-" * 50)

        y_coordinate = 760
        for label, value in zip(["Name", "LPG Cylinder Type", "Date of Birth", "Father's Name", "Mother's Name", "Address", "pincode","Contact Number"], data[1:]):
            pdf_canvas.drawString(100, y_coordinate, f"{label}: {value}")
            y_coordinate -= 20

        pdf_canvas.save()

    def back():
        root.destroy()
        

    # Create the main window
    root = tk.Tk()
    root.title("User Details Form")
    root.geometry("1080x681")
    root.configure(bg='#A6D7DB')
    create_user_details_table()

    # Labels for User Form
    user_form_title = tk.Label(root, text="User Details Form", font=("Arial", 25, "bold"), bg="#A6D7DB", fg="black")
    user_form_title.place(relx=0.5, rely=0.05, anchor=tk.CENTER)

    label_name = tk.Label(root, text="Name:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_name.place(relx=0.2, rely=0.15, anchor=tk.E)
    vcmd = (root.register(validate_input), '%S')
    entry_name = tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white", validate="key", validatecommand=vcmd)
    entry_name.place(relx=0.3, rely=0.15, anchor=tk.W)

    label_lpg_type = tk.Label(root, text="LPG Cylinder Type:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_lpg_type.place(relx=0.2, rely=0.23, anchor=tk.E)
    combo_lpg_type_user = ttk.Combobox(root, values=["Domestic", "Commercial"])
    combo_lpg_type_user.place(relx=0.3, rely=0.23, anchor=tk.W)

    label_dob = tk.Label(root, text="Date of Birth:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_dob.place(relx=0.2, rely=0.31, anchor=tk.E)
    entry_dob = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2)
    entry_dob.place(relx=0.3, rely=0.31, anchor=tk.W)

    label_father_name = tk.Label(root, text="Father's Name:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_father_name.place(relx=0.2, rely=0.39, anchor=tk.E)
    vcmd = (root.register(validate_father), '%S')
    entry_father_name = tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white", validate="key", validatecommand=vcmd)
    entry_father_name.place(relx=0.3, rely=0.39, anchor=tk.W)

    label_mother_name = tk.Label(root, text="Mother's Name:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_mother_name.place(relx=0.2, rely=0.47, anchor=tk.E)
    vcmd = (root.register(validate_mother), '%S')
    entry_mother_name = tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white", validate="key", validatecommand=vcmd)
    entry_mother_name.place(relx=0.3, rely=0.47, anchor=tk.W)

    label_address_user = tk.Label(root, text="Address:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_address_user.place(relx=0.2, rely=0.55, anchor=tk.E)
    vcmd_address = (root.register(validate_address), '%S')
    entry_address_user = tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white", validate="key", validatecommand=vcmd_address)
    entry_address_user.place(relx=0.3, rely=0.55, anchor=tk.W)


    label_contact_user = tk.Label(root, text="Contact Number:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_contact_user.place(relx=0.2, rely=0.63, anchor=tk.E)
    vcmd_contact = (root.register(validate_contact), '%S')
    entry_contact_user = tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white", validate="key", validatecommand=vcmd_contact)
    entry_contact_user.place(relx=0.3, rely=0.63, anchor=tk.W)

    label_pincode_user = tk.Label(root, text="Pincode:", font=("Arial", 15), bg="#A6D7DB", fg="black")
    label_pincode_user.place(relx=0.2, rely=0.71, anchor=tk.E)
    vcmd_contact = (root.register(validate_pincode), '%S')
    entry_pincode_user= tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white", validate="key", validatecommand=vcmd_contact)
    entry_pincode_user.place(relx=0.3, rely=0.71, anchor=tk.W)

    submit_user_button = tk.Button(root, text="Submit User Form", bg="white", fg="#007FFF", font=("Arial", 15, "bold"), activebackground="white", activeforeground="#007FFF", width=27, bd=5, cursor="hand2", command=submit_user_form)
    submit_user_button.place(relx=0.3, rely=0.89, anchor=tk.CENTER)

    back_button = tk.Button(root, text="Back", bg="white", fg="#007FFF", font=("Arial", 15, "bold"), activebackground="white", activeforeground="#007FFF", width=23, bd=5, cursor="hand2", command=lambda:backimp(root))
    back_button.place(relx=0.7, rely=0.89, anchor=tk.CENTER)

    root.mainloop()


