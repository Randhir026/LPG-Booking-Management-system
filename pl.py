import tkinter as tk
from tkinter import ttk, Listbox, Scrollbar, Entry
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import mysql.connector
from datetime import datetime

def create_window():
    # Function to fetch data from MySQL database
    def fetch_data():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Randhir@1#",
            database="userinfo"
        )
        cursor = conn.cursor()

        # Fetching data from user_detail table
        cursor.execute("SELECT customer_number, name FROM user_detail")
        user_details = cursor.fetchall()

        # Fetching data from final_booking table
        cursor.execute("SELECT customer_number, booked_date FROM book_final")
        final_bookings = cursor.fetchall()

        cursor.close()
        conn.close()

        return user_details, final_bookings

    # Function to process data and calculate monthly and user bookings
    def process_data(user_details, final_bookings):
        # Initialize the dictionary with all 12 months
        monthly_bookings = {f'{datetime.now().year}-{month:02d}': {'bookings': 0} for month in range(1, 13)}

        for booking in final_bookings:
            booking_date = booking[1]  # booking_date is already a datetime.date object
            month = booking_date.strftime('%Y-%m')

            if month in monthly_bookings:
                monthly_bookings[month]['bookings'] += 1

        # Calculate user bookings
        user_bookings = {}

        for booking in final_bookings:
            user_id = booking[0]
            if user_id in user_bookings:
                user_bookings[user_id] += 1
            else:
                user_bookings[user_id] = 1

        return monthly_bookings, user_bookings

    # Function to plot data
    def plot_data(monthly_bookings):
        months = sorted(monthly_bookings.keys())
        bookings = [monthly_bookings[month]['bookings'] for month in months]

        fig, ax = plt.subplots(figsize=(8, 6))  # Set the figure size

        # Plot number of bookings per month
        ax.plot(months, bookings, marker='o', linestyle='-', color='teal')
        ax.set_xlabel('Month')
        ax.set_ylabel('Number of Bookings')
        ax.set_title('Number of Bookings per Month')
        ax.set_xticks(months)
        ax.set_xticklabels(months, rotation=45, ha='right')

        # Set y-axis ticks from 1 to 10
        ax.set_yticks(range(1, 11))

        for i, booking in enumerate(bookings):
            ax.text(months[i], booking + 0.05 * max(bookings), str(booking), ha='center', va='bottom', fontsize=9, color='purple')

        ax.grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout()
        return fig

    # Function to filter users based on keyword
    def filter_users(user_bookings, user_details, keyword):
        filtered_users = []

        for user_id, bookings_count in user_bookings.items():
            user_name = next((name for (uid, name) in user_details if uid == user_id), "Unknown")
            if keyword.lower() in user_name.lower():
                filtered_users.append(f"{user_name}: Total Bookings - {bookings_count}")

        return filtered_users

    # Function to update Listbox based on search keyword
    def update_listbox(event=None):
        keyword = search_entry.get().strip().lower()
        filtered_users = filter_users(user_bookings, user_details, keyword)

        users_listbox.delete(0, tk.END)
        for user in filtered_users:
            users_listbox.insert(tk.END, user)

    # Main logic starts here
    user_details, final_bookings = fetch_data()
    monthly_bookings, user_bookings = process_data(user_details, final_bookings)
    fig = plot_data(monthly_bookings)

    root = tk.Tk()
    root.title("Monthly User Booking Report")
    root.configure(bg='#f0f0f0')  # Set the background color

    # Set the size of the window
    root.geometry("800x800")  # Adjust the window size as needed

    # Display total number of users above the graph
    total_user_count = len(user_details)
    total_users_label = tk.Label(root, text=f"Total Users: {total_user_count}", font=("Arial", 12), bg='#f0f0f0', fg='darkblue')
    total_users_label.pack(pady=10)

    # Search entry widget
    search_frame = ttk.Frame(root)
    search_frame.pack(pady=10)

    search_label = ttk.Label(search_frame, text="Search User:", font=("Arial", 10))
    search_label.pack(side=tk.LEFT, padx=5)

    search_entry = ttk.Entry(search_frame, width=30)
    search_entry.pack(side=tk.LEFT)
    search_entry.bind("<KeyRelease>", update_listbox)  # Bind KeyRelease event to update_listbox

    # Display user bookings in a Listbox with scrollbar
    users_frame = ttk.Frame(root)
    users_frame.pack(pady=10)

    users_listbox = Listbox(users_frame, width=50, height=10, font=("Arial", 10), bg='#ffffff', fg='black', selectbackground='lightblue')
    users_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))

    scrollbar = Scrollbar(users_frame, orient=tk.VERTICAL, command=users_listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    users_listbox.config(yscrollcommand=scrollbar.set)

    for user_id, bookings_count in user_bookings.items():
        user_name = next((name for (uid, name) in user_details if uid == user_id), "Unknown")
        users_listbox.insert(tk.END, f"{user_name}: Total Bookings - {bookings_count}")

    # Plotting the graph
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, pady=(10, 0))

    back_button = ttk.Button(root, text="Back", command=root.destroy)  # Close the window
    back_button.pack(pady=10)

    root.mainloop()


