




from tkinter import *
from tkinter import messagebox
import mysql.connector
import random
import string
import tkinter as tk
from tkcalendar import DateEntry
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from datetime import datetime, timedelta
from mysql.connector import Error
import user_main
def imp_user(user_window):
    user_window.destroy()
    user_main.user_window()

def have_conn():
    
    def get_last_booking_date(customer_number):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Randhir@1#',
                database='userinfo'
            )
            cursor = connection.cursor()
            query = ("SELECT booked_date FROM book_final WHERE customer_number = %s")
            cursor.execute(query,(customer_number,))
            result = cursor.fetchone()  # Fetch one row
            
            if result:
                return result[0]
            return None
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def check_booking_date(customer_number):
      last_booking_date = get_last_booking_date(customer_number)
    
      if last_booking_date:
        # Ensure last_booking_date is a datetime.date object
         if isinstance(last_booking_date, datetime):
            last_booking_date = last_booking_date.date()

        # Calculate today's date
         today = datetime.today().date()
        
        # Check if the difference is greater than or equal to 30 days
         difference = today - last_booking_date
         if difference >= timedelta(days=30):
             return True  # More than 30 days since last booking
         else:
            return False  # Less than 30 days since last booking
      else:
        return True  # No previ
    def show_message():
        window = tk.Tk()
        window.title("Booking Status")
        window.geometry("300x300")
    
        label = tk.Label(window, text="Cylinder booking successfully")
        label.pack(pady=20)
    
        button = tk.Button(window, text="OK", command=window.destroy)
        button.pack(pady=10)
    
        window.mainloop()   
    

    def book_cylinder():
        customer_number = entry_customer_number.get()
        
        if not check_booking_date(customer_number):
            messagebox.showerror("Booking Error", "You cannot book within 30 days from the previous booking.")
            user = get_user_details(customer_number)
            open_user_window(user)
            return

        booking_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        (booking_number, customer_number)
        
        cylinder_count = 1
        # Database connection
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Randhir@1#',
            database='userinfo'
        )
        cursor = connection.cursor()
        cursor.execute("SELECT name, contact_number FROM user_detail WHERE customer_number = %s", (customer_number,))
        user_details = cursor.fetchone()
        customer_name, contact_number = user_details
        insert_query = """
        INSERT INTO book_final (customer_number, customer_name, contact_number, cylinder_count, booking_number, booked_date)
        VALUES (%s, %s, %s, %s, %s, CURRENT_DATE)
        """
        cursor.execute(insert_query, (customer_number, customer_name, contact_number, cylinder_count, booking_number))

        connection.commit()
        # Fetch specific booking details from book_final table
        cursor.execute("SELECT customer_number, customer_name, contact_number,  booked_date FROM book_final WHERE booking_number = %s", (booking_number,))
        booking_details = cursor.fetchone()
         # Get the current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if booking_details is None:
            print("Booking number not found.")
            cursor.close()
            connection.close()
            return
        customer_number, customer_name, contact_number, booking_date = booking_details

        pdf_filename = f"{customer_name}_booking.pdf"

        c = canvas.Canvas(pdf_filename, pagesize=letter)

        c.setFont("Helvetica", 12)

        # Set fill color for the larger box
        c.setFillColorRGB(0.8, 0.8, 0.8)  # Light gray color
        c.rect(40, 520, 570, 300, fill=True)  # Larger Box with fill color

        c.setFillColorRGB(0, 0, 0)  # Black color
        c.setFont("Helvetica-Bold", 16)
        c.drawString(210, 780, "LPG Management System")
        c.line(210, 778, 380, 778)

        c.setFont("Helvetica", 12)
        c.drawString(50, 750, "Booking Details:")
        c.drawString(400, 760, f"Date : {current_time}")
        c.drawString(400, 750, f"Booking Number: {booking_number}")

        c.drawString(50, 730, f"Customer Number: {customer_number}")
        c.drawString(50, 710, f"Customer Name: {customer_name}")
        c.drawString(50, 690, f"Contact Number: {contact_number}")
        #c.drawString(50, 670, f"Number of Cylinders: {cylinders_count}")
        c.drawString(50, 650, f"Booking Date: {booking_date}")

        # Fetch address from user_details table
        cursor.fetchall()  # Consume any unread results
        cursor.execute("SELECT address FROM user_detail WHERE customer_number = %s", (customer_number,))
        address = cursor.fetchone()[0] 

        # Fetch amount from amount table where id is 1234
        cursor.fetchall()  # Consume any unread results
        cursor.execute("SELECT amount FROM amount WHERE id = 1234")
        amount = cursor.fetchone()[0]

        c.setFillColorRGB(0, 0, 0)  # Black color
        c.drawString(50, 630, f"Address: {address}")

        c.setFillColorRGB(1, 0, 0)  # Red color
        total_cost_text = f"Total Cost: Rs {amount}" 
        c.drawString(50, 610, total_cost_text)

        c.setFillColorRGB(0, 0, 0)  # Black color
        c.drawString(50, 580, "Refill amount shall be charged at delivery.")
        c.drawString(50, 560, "Kindly check cylinder for correct weight by the weighting scale of the delivery man at the time of delivery.")

        c.save()

        print(f"PDF saved as {pdf_filename}")

        # Close the cursor and connection
        cursor.close()
        connection.close()
        show_message()

    def submit_customer_number(root):
        
        customer_number = entry_customer_number.get()
        if not customer_number:
            messagebox.showerror("Input Error", "Please enter a customer number.")
            return
        
        user = get_user_details(customer_number)
        if user:
            
            open_user_window(user)
        else:
            messagebox.showerror("Not Found", "Customer not found. Please enter valid  customer number", parent=root)

    def get_user_details(customer_number):
        try:
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='Randhir@1#',
                database='userinfo'
            )
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM user_detail WHERE customer_number = %s"
            cursor.execute(query, (customer_number,))
            user = cursor.fetchone()
            cursor.close()
            connection.close()
            return user
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")
            return None

    def view_details(user):
        details = f"""
        Customer Number: {user['customer_number']}
        Name: {user['name']}
        LPG Type: {user['lpg_type']}
        Date of Birth: {user['dob']}
        Father's Name: {user['father_name']}
        Mother's Name: {user['mother_name']}
        Address: {user['address']}
        Pincode: {user['pincode']}
        Contact Number: {user['contact_number']}
        """
        messagebox.showinfo("User Details", details)
        open_user_window(user)

    def open_user_window(user):
        user_window = tk.Toplevel(root)
        user_window.title("User Details")
        user_window.geometry("500x400")
        user_window.configure(bg='#A6D7DB')

        welcome_label = tk.Label(user_window, text=f"Welcome, {user['name']}", font=("Arial", 20, "bold"), bg="#A6D7DB", fg="black")
        welcome_label.pack(pady=20)

        view_details_button = tk.Button(user_window, text="View Details", bg="white", fg="#007FFF", font=("Arial", 15, "bold"),
                                        activebackground="white", activeforeground="#007FFF", width=15, bd=5, cursor="hand2", 
                                        command=lambda: view_details(user))
        view_details_button.pack(pady=10)

        book_cylinder_button = tk.Button(user_window, text="Book Cylinder", bg="white", fg="#007FFF", font=("Arial", 15, "bold"),
                                         activebackground="white", activeforeground="#007FFF", width=15, bd=5, cursor="hand2", 
                                         command=book_cylinder)
        book_cylinder_button.pack(pady=10)
        b_button = tk.Button(user_window, text="Exit ", bg="white", fg="#007FFF", font=("Arial", 15, "bold"),
                                         activebackground="white", activeforeground="#007FFF", width=15, bd=5, cursor="hand2", 
                                         command=lambda:imp_user(user_window))
        b_button.pack(pady=10)

        user_window.mainloop()

    # Create the main window
    root = tk.Tk()
    root.title("Enter Customer Number")
    root.geometry("500x400")
    root.configure(bg='#A6D7DB')

    # Add a title label
    title_label = tk.Label(root, text="Enter Customer Number", font=("Arial", 20, "bold"), bg="#A6D7DB", fg="black")
    title_label.pack(pady=20)

    # Add an entry for customer number
    entry_customer_number = tk.Entry(root, width=30, font=("Arial", 15), fg="black", bd=0, bg="white")
    entry_customer_number.pack(pady=10)

    # Add a submit button
    submit_button = tk.Button(root, text="Submit", bg="white", fg="#007FFF", font=("Arial", 15, "bold"),
                              activebackground="white", activeforeground="#007FFF", width=15, bd=5, cursor="hand2", 
                              command=lambda:(submit_customer_number(root),root.destroy()))
    submit_button.pack(pady=10)

    # Start the main loop
    root.mainloop()

