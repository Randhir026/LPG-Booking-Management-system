from tkinter import *
from tkinter import messagebox
import mysql.connector
import tkinter as tk
from tkcalendar import DateEntry
from tkinter import messagebox, simpledialog
from datetime import datetime
import re
import pl

def impreport():
    pl.create_window()


def fetch_bookings_between_dates():
    def get_bookings_between_dates(start_date, end_date):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Randhir@1#',
                database='userinfo'
            )
            cursor = connection.cursor(dictionary=True)
            query = """
            SELECT * FROM book_final
            WHERE booked_date BETWEEN %s AND %s
            """
            cursor.execute(query, (start_date, end_date))
            bookings = cursor.fetchall()
            cursor.close()
            connection.close()
            return bookings
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return []

    def fetch_and_display_bookings():
        start_date = entry_start_date.get()
        end_date = entry_end_date.get()

        try:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Input Error", "Please enter dates in YYYY-MM-DD format.")
            fetch_bookings_between_dates()
            return

        bookings = get_bookings_between_dates(start_date, end_date)

        if not bookings:
            messagebox.showinfo("No Bookings", "No bookings found for the specified date range.")
            return

        # Create a new window to display the bookings
        bookings_window = tk.Toplevel(root)
        bookings_window.title("Bookings Between Dates")
        bookings_window.geometry("800x600")
        bookings_window.configure(bg='#A6D7DB')

        # Create a text widget to display the bookings
        text_widget = tk.Text(bookings_window, wrap=tk.WORD, bg="white", fg="black", font=("Arial", 12))
        text_widget.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

        # Add booking details to the text widget
        for booking in bookings:
            booking_details = f"""
            Booking Number: {booking['booking_number']}
            Customer Number: {booking['customer_number']}
            Customer Name: {booking['customer_name']}
            Contact Number: {booking['contact_number']}
            Cylinder Count: {booking['cylinder_count']}
            Booking Date: {booking['booked_date']}
            ------------------------------
            """
            text_widget.insert(tk.END, booking_details)

    # Create the main window
    root = tk.Tk()
    root.title("Fetch Bookings Between Dates")
    root.geometry("400x400")
    root.configure(bg='#A6D7DB')

    # Add a title label
    title_label = tk.Label(root, text="Enter Date Range", font=("Arial", 20, "bold"), bg="#A6D7DB", fg="black")
    title_label.pack(pady=20)

    # Add entry fields for start date and end date
    tk.Label(root, text="Start Date (YYYY-MM-DD):", bg="#A6D7DB", fg="black", font=("Arial", 12)).pack(pady=5)
    entry_start_date = tk.Entry(root, width=20, font=("Arial", 12))
    entry_start_date.pack(pady=5)

    tk.Label(root, text="End Date (YYYY-MM-DD):", bg="#A6D7DB", fg="black", font=("Arial", 12)).pack(pady=5)
    entry_end_date = tk.Entry(root, width=20, font=("Arial", 12))
    entry_end_date.pack(pady=5)

    # Add a submit button
    submit_button = tk.Button(root, text="Fetch Bookings", bg="white", fg="#007FFF", font=("Arial", 15, "bold"),
                              activebackground="white", activeforeground="#007FFF", width=15, bd=5, cursor="hand2", 
                              command=fetch_and_display_bookings)
    submit_button.pack(pady=20)
    st_button = tk.Button(root, text="Back", bg="white", fg="#007FFF", font=("Arial", 15, "bold"),
                              activebackground="white", activeforeground="#007FFF", width=15, bd=5, cursor="hand2", 
                              command=root.destroy)
    st_button.pack(pady=20)

    # Start the main loop
    root.mainloop()

def admin():
    
    
    
    def login():
        admin_id = entry_admin_id.get()
        password = entry_password.get()

        if admin_id == "1" and password == "1":
            messagebox.showinfo("Login Successful", "Welcome, Admin!")
            open_main_window()
        else:
            messagebox.showerror("Login Failed", "Invalid Admin ID or Password")

    def delete_user():
        # Prompt user for the customer number
        customer_number = simpledialog.askinteger("Delete User ", " Enter Customer Number: ")
        if customer_number is not None:
            if check_user_existence(customer_number):
                try:
                # Connect to the database
                   con = mysql.connector.connect(host='localhost', user='root', password='Randhir@1#', database='userinfo')
                   cursor = con.cursor()

                # Delete the record from the user_details table
                   query = "DELETE FROM user_detail WHERE customer_number = %s"
                   cursor.execute(query, (customer_number,))
                   con.commit()

                   messagebox.showinfo("Success", "User deleted successfully")
                   open_main_window()

                except mysql.connector.Error as err:
                   messagebox.showerror("Error", f"Error: {err}")
                   open_main_window()

                finally:
                # Close database connection
                    if con.is_connected():
                       cursor.close()
                       con.close()

            else:
               messagebox.showinfo("User Not Found", "User with the specified customer number was not found.")
               open_main_window()
    def check_user_existence(customer_number):
        try:
            con = mysql.connector.connect(host='localhost', user='root', password='Randhir@1#', database='userinfo')
            cursor = con.cursor()

        # Check if the user exists
            query = "SELECT * FROM user_detail WHERE customer_number = %s"
            cursor.execute(query, (customer_number,))
            row = cursor.fetchone()

            if row is not None:
               return True
            else:
               return False

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
            return False

        finally:
            if con.is_connected():
               cursor.close()
               con.close()




    def amt_upd():
    # Create a window for updating the amount
        window = tk.Tk()
        window.title("Update Amount")
        window.geometry("500x300")
        window.configure(bg='#A6D7DB')

        def update_amount(new_amount):
            try:
            # Connect to the database
                connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Randhir@1#',
                database='userinfo'
                )
                cursor = connection.cursor()

            # Execute the update query
                query = "UPDATE amount SET amount = %s WHERE id = 1234"
                cursor.execute(query, (new_amount,))

            # Commit the changes
                connection.commit()

                messagebox.showinfo("Success", "Amount updated successfully.")
                open_main_window()
            except mysql.connector.Error as err:
                messagebox.showerror("Database Error", f"Error: {err}")
            finally:
            # Close the cursor and connection
                cursor.close()
                connection.close()

        def submit_amount():
            new_amount = entry_amount.get()
            if new_amount.isdigit():
                update_amount(new_amount)
            else:
                messagebox.showerror("Invalid Amount", "Please enter a valid integer amount.")
                amt_upd()

    # Create labels, entry field, and button for inputting and updating the amount
        label_amount = tk.Label(window, text="Enter New Amount:", font=("Arial", 14), bg="#A6D7DB")
        label_amount.pack(pady=10)

        entry_amount = tk.Entry(window, font=("Arial", 12), width=20)
        entry_amount.pack(pady=5)

        submit_button = tk.Button(window, text="Submit", font=("Arial", 12), bg="white", fg="#007FFF", command=submit_amount)
        submit_button.pack(pady=10)
        back_button = tk.Button(window, text="Back", font=("Arial", 12), bg="white", fg="#007FFF", command=lambda:(window.destroy(), open_main_window()))
        back_button.pack(pady=20)

        window.mainloop()
    
     
    def show_all_bookings():
        # Connect to the MySQL database (replace placeholders with your actual credentials)
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Randhir@1#",
            database="userinfo"
        )

        # Create a cursor
        cursor = db.cursor()

        try:
            # Execute the SQL query to fetch all booking details
            cursor.execute("SELECT id, customer_number, customer_name, contact_number, cylinder_count, booking_number, booked_date FROM book_final")

            # Fetch all rows
            rows = cursor.fetchall()

            # Create a new Tkinter window to display all booking details
            all_bookings_window = tk.Toplevel(root)
            all_bookings_window.title("All Bookings")
            all_bookings_window.geometry("800x300")

            # Create and place labels for column headers
            headers = ["ID", "Customer Number", "Customer Name", "Contact Number", "Cylinder Count", "Booking Number", "Booked Date"]
            for col, header in enumerate(headers):
                label = tk.Label(all_bookings_window, text=header, font=("bold", 10))
                label.grid(row=0, column=col, padx=5, pady=5)

            # Iterate through rows and display data
            for row_idx, row in enumerate(rows, start=1):
                for col, value in enumerate(row):
                    label = tk.Label(all_bookings_window, text=str(value))
                    label.grid(row=row_idx, column=col, padx=5, pady=5)
            back_button = tk.Button(all_bookings_window, text="Back", command=all_bookings_window.destroy)
            back_button.grid(row=len(rows) + 1, column=0, columnspan=len(headers), pady=10)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching booking details: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

    def show_user_details():
        # Connect to the MySQL database (replace placeholders with your actual credentials)
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Randhir@1#",
            database="userinfo"
        )

        # Create a cursor
        cursor = db.cursor()

        try:
            # Execute the SQL query to fetch user details
            cursor.execute("SELECT id, customer_number, name, lpg_type, dob, father_name, mother_name, address, contact_number FROM user_detail")

            # Fetch all rows
            rows = cursor.fetchall()

            # Print fetched rows for debugging
            print(rows)

            # Create a new Tkinter window to display user details
            user_details_window = tk.Toplevel(root)
            user_details_window.title("User Details")
            user_details_window.geometry("760x450")
            

            # Create and place labels for column headers
            headers = ["ID", "Customer Number", "Name", "LPG Type", "DOB", "Father Name", "Mother Name", "Address", "Contact Number"]
            for col, header in enumerate(headers):
                label = tk.Label(user_details_window, text=header, font=("bold", 10))
                label.grid(row=0, column=col, padx=5, pady=5)

            # Iterate through rows and display data
            for row_idx, row in enumerate(rows, start=1):
                for col, value in enumerate(row):
                    label = tk.Label(user_details_window, text=str(value))
                    label.grid(row=row_idx, column=col, padx=5, pady=5)
           
            back_button = tk.Button(user_details_window, text="Back", command=user_details_window.destroy)
            back_button.grid(row=len(rows) + 1, column=0, columnspan=len(headers), pady=10)


        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching user details: {err}")

        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()

    def search_user():
        # Create a new window for searching user
        search_window = tk.Toplevel(root)
        search_window.title("Search User")
        search_window.geometry("500x500")
        search_window.configure(bg='#A6D7DB')

        # Create and place labels and entry field for searching user
        label_customer_number = tk.Label(search_window, text="Customer Number:",font=("Arial", 15), bg="#A6D7DB", fg="white")
        label_customer_number.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

        entry_customer_number = tk.Entry(search_window)
        entry_customer_number.grid(row=0, column=1, padx=10, pady=10)

        # Create and place the search button
        search_button = tk.Button(search_window, text="Search", command=lambda: show_user_by_customer_number(entry_customer_number.get()), bg="white", fg="#007FFF", font=("Arial", 12, "bold"), activebackground="white", activeforeground="#007FFF", bd=0, cursor="hand2")
        search_button.grid(row=1, column=0, columnspan=2, pady=10)
        back_button = tk.Button(search_window, text="Back",command=lambda: (search_window.destroy(), open_main_window()), bg="white", fg="#007FFF", font=("Arial", 12, "bold"), activebackground="white", activeforeground="#007FFF", bd=0, cursor="hand2")
        back_button.grid(row=2, column=0, columnspan=2, pady=10)
        

    def show_user_by_customer_number(customer_number):
        # Connect to the MySQL database (replace placeholders with your actual credentials)
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Randhir@1#",
            database="userinfo"
        )

        # Create a cursor
        cursor = db.cursor()

        try:
            # Execute the SQL query to fetch user details based on customer number
            cursor.execute("SELECT id, customer_number, name, lpg_type, dob, father_name, mother_name, address, contact_number FROM user_detail WHERE customer_number = %s", (customer_number,))

            # Fetch all rows
            rows = cursor.fetchall()

            # Create a new Tkinter window to display user details
            user_details_window = tk.Toplevel(root)
            user_details_window.title("User Details")
            user_details_window.geometry("750x300")
            

            # Create and place labels for column headers
            headers = ["ID", "Customer Number", "Name", "LPG Type", "DOB", "Father Name", "Mother Name", "Address", "Contact Number"]
            for col, header in enumerate(headers):
                label = tk.Label(user_details_window, text=header, font=("bold", 10))
                label.grid(row=0, column=col, padx=5, pady=5)
            if not rows:
                messagebox.showinfo("No Data", "No user found with the specified customer number.")
                search_user()

            # Iterate through rows and display data
            for row_idx, row in enumerate(rows, start=1):
                for col, value in enumerate(row):
                    label = tk.Label(user_details_window, text=str(value))
                    label.grid(row=row_idx, column=col, padx=5, pady=5)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error fetching user details: {err}")
            

        finally:
            # Close the cursor and database connection
            cursor.close()
            db.close()
    
    def update_details():
        def check_customer_number(customer_number):
            try:
                 con = mysql.connector.connect(host='localhost', user='root', password='Randhir@1#', database='userinfo')
                 cursor = con.cursor()
                 query = "SELECT * FROM user_detail WHERE customer_number = %s"
                 cursor.execute(query, (customer_number,))
                 row = cursor.fetchone()
                 if row is not None:
                     return True
                 else:
                     messagebox.showinfo("User Not Found", "User with the specified customer number was not found.")
                     open_main_window()
                     return False
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error: {err}")

                return False
            finally:
                 if con.is_connected():
                      cursor.close()
                      con.close()
        customer_number = simpledialog.askinteger("Input", "Enter Customer Number:")
        if customer_number:
            if check_customer_number(customer_number):
                update_window = tk.Toplevel(root)
                update_window.title("Update Details")
                update_window.geometry("500x500")
                update_window.configure(bg='#A6D7DB')

            # Create and place buttons for updating details
                name_button = tk.Button(update_window, text="Update Name", command=lambda: update_user_detail(update_window, customer_number, "name"), bg="white", fg="#007FFF", font=("Arial", 12, "bold"), activebackground="white", activeforeground="#007FFF", bd=0, cursor="hand2")
                name_button.pack(pady=10)

                father_name_button = tk.Button(update_window, text="Update Father Name", command=lambda: update_user_detail(update_window,customer_number, "father_name"), bg="white", fg="#007FFF", font=("Arial", 12, "bold"), activebackground="white", activeforeground="#007FFF", bd=0, cursor="hand2")
                father_name_button.pack(pady=10)

                mother_name_button = tk.Button(update_window, text="Update Mother Name", command=lambda: update_user_detail(update_window,customer_number, "mother_name"), bg="white", fg="#007FFF", font=("Arial", 12, "bold"), activebackground="white", activeforeground="#007FFF", bd=0, cursor="hand2")
                mother_name_button.pack(pady=10)
                contact_button = tk.Button(update_window, text="Update Contact ", command=lambda: update_contact_number(update_window,customer_number), bg="white", fg="#007FFF", font=("Arial", 12, "bold"), activebackground="white", activeforeground="#007FFF", bd=0, cursor="hand2")
                contact_button.pack(pady=10)

               

    def update_user_detail(update_window,customer_number, field):
        new_value = simpledialog.askstring("Input", f"Enter new {field.capitalize()}:")
        
        # Check if the new value contains only alphabets
        if new_value.isalpha():
            # Connect to the MySQL database (replace placeholders with your actual credentials)
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Randhir@1#",
                database="userinfo"
            )

            # Create a cursor
            cursor = db.cursor()

            try:
                # Execute the SQL query to update user details
                cursor.execute(f"UPDATE user_detail SET {field} = %s WHERE customer_number = %s", (new_value, customer_number))

                # Commit the changes
                db.commit()

                messagebox.showinfo("Update Successful", f"{field.capitalize()} updated successfully.")
                open_main_window()
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating user details: {err}")

            finally:
                # Close the cursor and database connection
                cursor.close()
                db.close()
        else:
            messagebox.showerror("Invalid Input", "Please enter only alphabets for the name.",parent=update_window)
            #update_details()


    def update_contact_number(update_window,customer_number):
        
        
            # Prompt the user to enter the new contact number
            new_contact_number = simpledialog.askstring("Input", "Enter New Contact Number:")

            if new_contact_number:
                # Validate the contact number
                if re.match(r'^[6789]\d{9}$', new_contact_number):
                    try:
                        con = mysql.connector.connect(host='localhost', user='root', password='Randhir@1#', database='userinfo')
                        cursor = con.cursor()
                        query = "UPDATE user_detail SET contact_number = %s WHERE customer_number = %s"
                        cursor.execute(query, (new_contact_number, customer_number))
                        con.commit()
                        messagebox.showinfo("Success", "Contact number updated successfully.")
                        open_main_window()
                    except mysql.connector.Error as err:
                        messagebox.showerror("Error", f"Error: {err}")
                    finally:
                        if con.is_connected():
                            cursor.close()
                            con.close()
                else:
                    messagebox.showwarning("Input Error", "Contact number must be 10 digits long and start with 6, 7, 8, or 9.",parent=update_window)
                    #update_details()
            else:
                messagebox.showwarning("Input Error", "No contact number entered.",parent=update_window)
                #update_details()
                
    def open_main_window():
        
    # Create the main window
        main_window = tk.Toplevel(root)
        main_window.title("Admin Dashboard")
        main_window.geometry("800x750")
        main_window.configure(bg='#A6D7DB')
        main_window.resizable(False, False)

    # Title
        title_label = tk.Label(
            main_window,
            text="🛠 Admin Panel",
            font=("Segoe UI", 28, "bold"),
            bg="#A6D7DB",
            fg="#004d40"
        )
        title_label.pack(pady=30)

    # Container for buttons
        button_frame = tk.Frame(main_window, bg="#A6D7DB")
        button_frame.pack(pady=10)

    # Style for all buttons
        button_style = {
            "bg": "white",
        "fg": "#007FFF",
        "activebackground": "#007FFF",
        "activeforeground": "white",
        "font": ("Arial", 15, "bold"),
        "width": 28,
        "bd": 4,
        "relief": "raised",
        "cursor": "hand2",
        "highlightthickness": 0,
        "padx": 10,
        "pady": 5
        }

    # Hover effects
        def on_enter(e, btn):
            btn.config(bg="#007FFF", fg="white")

        def on_leave(e, btn):
            btn.config(bg="white", fg="#007FFF")

    # Create buttons using helper
        def add_button(text, command):
            btn = tk.Button(button_frame, text=text, command=command, **button_style)
            btn.pack(pady=10)
            btn.bind("<Enter>", lambda e: on_enter(e, btn))
            btn.bind("<Leave>", lambda e: on_leave(e, btn))
            return btn

    # Buttons with same commands
        add_button("📋 User Details", show_user_details)
        add_button("📝 Update Details", update_details)
        add_button("🔍 Search User", search_user)
        add_button("📦 All Bookings", show_all_bookings)
        add_button("🗑️ Delete User", delete_user)
        add_button("💰 Update Amount", amt_upd)
        add_button("📅 View Bookings Between Dates", fetch_bookings_between_dates)
        add_button("📊 Report", impreport)

        main_window.mainloop()
    
    # Create the login window
    root = tk.Tk()
    root.title("🔐 Admin Login")
    root.geometry("500x400")
    root.configure(bg='#A6D7DB')
    root.resizable(False, False)

# ----------------------
# Title Label
# ----------------------
    title_label = tk.Label(
        root,
        text="🔐 Admin Login",
        font=("Segoe UI", 28, "bold"),
        bg="#A6D7DB",
        fg="#004d40"
    )
    title_label.pack(pady=30)

# ----------------------
# Entry Frame (for cleaner layout)
# ----------------------
    entry_frame = tk.Frame(root, bg="#A6D7DB")
    entry_frame.pack(pady=10)

# Admin ID Label & Entry
    label_admin_id = tk.Label(entry_frame, text="Admin ID:", font=("Segoe UI", 14), bg="#A6D7DB", fg="#004d40")
    label_admin_id.grid(row=0, column=0, padx=10, pady=10, sticky=tk.E)

    entry_admin_id = tk.Entry(entry_frame, font=("Segoe UI", 12), bd=2, relief="groove")
    entry_admin_id.grid(row=0, column=1, padx=10, pady=10)

# Password Label & Entry
    label_password = tk.Label(entry_frame, text="Password:", font=("Segoe UI", 14), bg="#A6D7DB", fg="#004d40")
    label_password.grid(row=1, column=0, padx=10, pady=10, sticky=tk.E)

    entry_password = tk.Entry(entry_frame, font=("Segoe UI", 12), bd=2, show="*", relief="groove")
    entry_password.grid(row=1, column=1, padx=10, pady=10)

# ----------------------
# Hover effect functions
# ----------------------
    def on_enter(e):
        login_button['background'] = "#007FFF"
        login_button['foreground'] = "white"

    def on_leave(e):
        login_button['background'] = "white"
        login_button['foreground'] = "#007FFF"

# ----------------------
# Login Button
# ----------------------
    login_button = tk.Button(
        root,
        text="Login",
        command=login,
        font=("Segoe UI", 14, "bold"),
        bg="white",
        fg="#007FFF",
        activebackground="#007FFF",
        activeforeground="white",
        bd=0,
        relief="flat",
        cursor="hand2",
        width=15,
        height=2
    )
    login_button.pack(pady=30)
    login_button.bind("<Enter>", on_enter)
    login_button.bind("<Leave>", on_leave)

# ----------------------
# Mainloop
# ----------------------
    root.mainloop()