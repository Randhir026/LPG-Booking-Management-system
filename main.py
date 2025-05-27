from tkinter import *
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
import admin
import user_main

def run_admin():
    admin.admin()

def call_userm():
    user_main.user_window()

# Hover effect functions
def on_enter(e, btn, hover_color):
    btn['background'] = hover_color

def on_leave(e, btn, original_color):
    btn['background'] = original_color

# Initialize main window
root = Tk()
root.title("LPG Management System")
root.attributes('-fullscreen', True)

# Get screen dimensions
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Load and process background image
bg_image = Image.open("lgp.jpg").convert('RGBA')
bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=2))
bg_image = ImageEnhance.Brightness(bg_image).enhance(0.6)
bg_photo = ImageTk.PhotoImage(bg_image)

background_label = Label(root, image=bg_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Title Label
title_label = Label(
    root,
    text="🔥 LPG Management System 🔥",
    font=("Lucida Handwriting", 44, "bold italic"),
    bg="#004d40",
    fg="#ffe082",
    padx=20,
    pady=20
)
title_label.pack(pady=60)

# Button style
button_style = {
    "width": 20,
    "height": 2,
    "font": ("Segoe UI Semibold", 18, "bold"),
    "bg": "#ff7043",
    "fg": "white",
    "activebackground": "#ff8a65",
    "activeforeground": "white",
    "bd": 0,
    "relief": "flat",
    "cursor": "hand2"
}

# Admin Button
admin_button = Button(root, text="🛠 Admin Panel", command=run_admin, **button_style)
admin_button.pack(pady=20)
admin_button.bind("<Enter>", lambda e: on_enter(e, admin_button, "#ff8a65"))
admin_button.bind("<Leave>", lambda e: on_leave(e, admin_button, "#ff7043"))

# User Button
user_button = Button(root, text="👤 User Access", command=call_userm, **button_style)
user_button.pack(pady=20)
user_button.bind("<Enter>", lambda e: on_enter(e, user_button, "#ff8a65"))
user_button.bind("<Leave>", lambda e: on_leave(e, user_button, "#ff7043"))

# Separator
separator = Frame(root, bg="#ccc", height=2, width=400)
separator.pack(pady=30)

# Exit Button (unique color)
exit_button = Button(
    root,
    text="❌ Exit",
    command=root.destroy,
    font=("Segoe UI", 14, "bold"),
    bg="#d32f2f",
    fg="white",
    activebackground="#ef5350",
    activeforeground="white",
    padx=10,
    pady=5,
    bd=0,
    relief="flat",
    cursor="hand2",
    width=20
)
exit_button.pack(pady=10)
exit_button.bind("<Enter>", lambda e: on_enter(e, exit_button, "#ef5350"))
exit_button.bind("<Leave>", lambda e: on_leave(e, exit_button, "#d32f2f"))

# Footer
footer = Label(
    root,
    text="© 2025 LPG Management System | Designed with ❤️|RK",
    font=("Helvetica", 10, "italic"),
    bg="#e0f7fa",
    fg="#004d40",
    pady=5
)
footer.pack(side="bottom", pady=15)

root.mainloop()
