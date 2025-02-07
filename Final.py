import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
from datetime import datetime, timedelta

def connect_to_database():
    try:
        open_dashboard = mysql.connector.connect(
            host='localhost',
            user='root',  # Default XAMPP username
            password='',  # Default XAMPP password
            database='retailing_system'
        )
        cursor = open_dashboard.cursor()
        print("Database connected successfully!")
        return open_dashboard
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    
def apply_border_radius(widget):
    widget.configure(highlightbackground="black", highlightthickness=1, relief="flat")
def process_payment(promo, price, expiry, username): 
    # Create Payment Window
    payment_window = tk.Toplevel(root)
    payment_window.title("Process Payment")
    payment_window.attributes('-fullscreen', True)  # Set fullscreen mode

    # Load Background Image
    bg_image_path = "C:/Users/PC/Downloads/360_F_398231758_6dclqrQdYd5hdOCo3M2G2stekJ8JGAZC.jpg"
    image = Image.open(bg_image_path)
    image = image.resize((payment_window.winfo_screenwidth(), payment_window.winfo_screenheight()))
    bg_image = ImageTk.PhotoImage(image)

    # Create a Canvas for the background
    canvas = tk.Canvas(payment_window, width=payment_window.winfo_screenwidth(), height=payment_window.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image)

    # Display Header
    header_label = tk.Label(payment_window, text=f"WELCOME {username})", bg="#f4f0e1", font=("Arial", 14, "bold"))
    canvas.create_window(payment_window.winfo_screenwidth() // 2, 50, window=header_label)

    # Selected Promo Details
    promo_label = tk.Label(
        payment_window,
        text=f"YOU SELECTED: {promo} - {price} (Expiry: {expiry})",
        bg="#f4f0e1",
        font=("Arial", 12, "bold")
    )
    canvas.create_window(payment_window.winfo_screenwidth() // 2, 160, window=promo_label)

    # Amount Entry
    amount_label = tk.Label(payment_window, text="ENTER AMOUNT:", bg="#f4f0e1", font=("Arial", 12, "bold"))
    canvas.create_window(payment_window.winfo_screenwidth() // 2, 220, window=amount_label)

    entry_amount = tk.Entry(payment_window, font=("Arial", 12))
    canvas.create_window(payment_window.winfo_screenwidth() // 2, 260, window=entry_amount)

    # Function to confirm payment
    def confirm_payment():
        try:
            amount = int(entry_amount.get())
            if amount < int(price.replace("P", "")):
                messagebox.showerror("Payment Error", "Insufficient amount entered.")
            else:
                change = amount - int(price.replace("P", ""))
                
                print(f"Change: {change}, Expiry: {expiry}")

                # Database saving logic
                try:
                    db = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="retailing_system"
                    )
                    cursor = db.cursor()
                    query = """
                        INSERT INTO records (username, promo_selected, amount_paid, change_amount, expiry_date) 
                        VALUES (%s, %s, %s, %s, %s)
                    """
                    values = (username, promo, amount, change, expiry)
                    cursor.execute(query, values)
                    db.commit()
                    db.close()
                except mysql.connector.Error as err:
                    messagebox.showerror(f"Database Error", "Error saving record: {err}")
                    return

                # Success message and balance update
                messagebox.showinfo("Payment Success",
                                    f"Promo Loaded Successfully!\nChange: P{change}\nPromo Expiry: {expiry}")
                payment_window.destroy()
                
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid number.")

    # Confirm Button
    confirm_button = tk.Button(
        payment_window,
        text="CONFIRM",
        bg="#e0e0e0",
        font=("Arial", 10, "bold"),
        command=confirm_payment
    )
    canvas.create_window(payment_window.winfo_screenwidth() // 2, 330, window=confirm_button)

    # Back Button
    def go_back_to_promos():
        payment_window.destroy()
        show_promos("TNT/SMART", username)

    back_button = tk.Button(
        payment_window,
        text="BACK",
        bg="#e0e0e0",
        font=("Arial", 10, "bold"),
        command=go_back_to_promos
    )
    canvas.create_window(payment_window.winfo_screenwidth() // 2, 380, window=back_button)

    # Escape Key to Exit
    payment_window.bind("<Escape>", lambda event: payment_window.destroy())
    payment_window.bg_image = bg_image  # Prevent garbage collection
    
def show_promos(carrier, username):
    import tkinter as tk
    from PIL import Image, ImageTk

    # Create the Promos window
    promos_window = tk.Toplevel(root)
    promos_window.title(f"{carrier} Promos")
    promos_window.attributes('-fullscreen', True)

    # Background setup
    bg_image_path = "C:/Users/PC/Downloads/360_F_398231758_6dclqrQdYd5hdOCo3M2G2stekJ8JGAZC.jpg"
    try:
        bg_image = Image.open(bg_image_path)
        bg_image = bg_image.resize((promos_window.winfo_screenwidth(), promos_window.winfo_screenheight()))
        bg_image_tk = ImageTk.PhotoImage(bg_image)
    except FileNotFoundError:
        print(f"Background image not found: {bg_image_path}")
        return

    canvas = tk.Canvas(promos_window, width=promos_window.winfo_screenwidth(), height=promos_window.winfo_screenheight())
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, anchor="nw", image=bg_image_tk)

    # Header
    header_text = f"{carrier.upper()}'s Promos for {username}"
    header_label = tk.Label(promos_window, text=header_text, bg="#f4f0e1", font=("Arial", 16, "bold"))
    canvas.create_window(promos_window.winfo_screenwidth() // 2, 50, window=header_label)

    # Promos Data
    promos = {
        "TNT/SMART": [
            ("GIGA50", "P55", "3 days", "C:/Users/PC/OneDrive/Pictures/GIGA50.png"),
            ("GIGA99", "P110", "7 days", "C:/Users/PC/OneDrive/Pictures/GIGA99.png"),
            ("SURFSAYA30", "P33", "3 days", "C:/Users/PC/OneDrive/Pictures/SURF30.png"),
            ("FB10", "P13", "3 days", "C:/Users/PC/OneDrive/Pictures/FB10.png"),
            ("ALLDATA50", "P50", "3 days", "C:/Users/PC/OneDrive/Pictures/ALLDATA50.png"),
            ("GIGA+149", "P160", "30 days", "C:/Users/PC/OneDrive/Pictures/GIGA149.png"),
        ],
        "GLOBE": [
            ("GOUNLI20", "P23", "2 days", "C:/Users/PC/OneDrive/Pictures/GOUNLI20.png"),
            ("GOUNLI50", "P55", "3 days", "C:/Users/PC/OneDrive/Pictures/GOUNLI50.png"),
            ("GOSURF30", "P33", "3 days", "C:/Users/PC/OneDrive/Pictures/GOSURF30.png"),
            ("GOSURF299", "P310", "30 days", "C:/Users/PC/OneDrive/Pictures/GOSURF299.png"),
            ("GOSURF999", "P1020", "30 days", "C:/Users/PC/OneDrive/Pictures/GOSURF999.png"),
            ("GOSURF599", "P610", "30 days", "C:/Users/PC/OneDrive/Pictures/GOSURF599.png"),
        ],
        "TM": [
            ("COMBOALL10", "P13", "1 day", "C:/Users/PC/OneDrive/Pictures/comboall10.png"),
            ("ALL-NETSURF20", "P23", "2 days", "C:/Users/PC/OneDrive/Pictures/allnetsurf20.png"),
            ("ALL-NETSURF30", "P33", "3 days", "C:/Users/PC/OneDrive/Pictures/allnetsurf30.png"),
            ("COMBO20", "P23", "2 days", "C:/Users/PC/OneDrive/Pictures/combo20.png"),
            ("EASYSURF50", "P55", "3 days", "C:/Users/PC/OneDrive/Pictures/easysurf50.png"),
            ("EASYSURF99", "P110", "7 days", "C:/Users/PC/OneDrive/Pictures/easysurf99.png"),
        ],
    }

    # Calculate center positions
    screen_width = promos_window.winfo_screenwidth()
    screen_height = promos_window.winfo_screenheight()
    x_offset = 350  # Horizontal spacing between items
    y_offset = 300  # Vertical spacing between rows
    starting_x = (screen_width - (2 * x_offset)) // 2  # Start in the middle
    starting_y = 150

    row = 0
    col = 0

    def handle_promo_click(promo_name, price, expiry):
        print(f"Promo clicked: {promo_name} - Price: {price}, Expiry: {expiry}")
        promos_window.destroy()  # Close the promos window
        process_payment(promo_name, price, expiry, username)  # Proceed to payment window

    # Render promos
    for promo, price, expiry, image_path in promos.get(carrier, []):
        try:
            # Load the image
            promo_image = Image.open(image_path).resize((150, 120))  # Resize promo image
            promo_image_tk = ImageTk.PhotoImage(promo_image)

            # Calculate position
            x_position = starting_x + col * x_offset
            y_position = starting_y + row * y_offset

            # Place image
            canvas.create_image(x_position, y_position, image=promo_image_tk, anchor="center")
            if not hasattr(canvas, "image_references"):
                canvas.image_references = []
            canvas.image_references.append(promo_image_tk)

            # Create a button for the promo
            promo_button = tk.Button(
                promos_window,
                text=f"{promo}\n{price}\n{expiry}",
                font=("Arial", 12),
                bg="lightblue",
                command=lambda p=promo, pr=price, e=expiry: handle_promo_click(p, pr, e),
            )
            canvas.create_window(x_position, y_position + 110, window=promo_button)

        except Exception as e:
            print(f"Error loading promo image: {image_path}, Error: {e}")

        col += 1
        if col >= 3:  # Max 3 items per row
            col = 0
            row += 1

    # Add Back Button
    def go_back_to_carrier_selection():
        promos_window.destroy()
        open_dashboard(username)  # Reopen the carrier selection screen

    back_button = tk.Button(
        promos_window,
        text="Back",
        font=("Arial", 14, "bold"),
        bg="red",
        fg="white",
        command=go_back_to_carrier_selection,  # Go back to the carrier selection
    )
    canvas.create_window(screen_width // 2, screen_height - 50, window=back_button)

    promos_window.mainloop()

def open_dashboard(username):
    # Hide the login/root window
    root.withdraw()

    # Create the Dashboard window
    dashboard = tk.Toplevel(root)
    dashboard.title("Dashboard")
    dashboard.attributes('-fullscreen', True)  # Fullscreen mode

    # Load the background image using Pillow
    bg_image_path = "C:/Users/PC/Downloads/360_F_398231758_6dclqrQdYd5hdOCo3M2G2stekJ8JGAZC.jpg"
    image = Image.open(bg_image_path)  # Open the image file
    image = image.resize((dashboard.winfo_screenwidth(), dashboard.winfo_screenheight()))  # Resize to full screen
    bg_image = ImageTk.PhotoImage(image)  # Convert to a format Tkinter understands

    # Create a Canvas to hold the background image
    canvas = tk.Canvas(dashboard, width=dashboard.winfo_screenwidth(), height=dashboard.winfo_screenheight())
    canvas.pack(fill="both", expand=True)

    # Set the background image
    canvas.create_image(0, 0, anchor="nw", image=bg_image)
    
    # Top border frame with sky blue background
    top_border = tk.Frame(dashboard, bg="sky blue", height=75)
    top_border.place(relx=0, rely=0, relwidth=1, height=75)

    # "Show Usage" Button in Options
    def show_usage():
        # Query the database for the user's current promo
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="retailing_system"
            )
            cursor = db.cursor()
            
            # Query to fetch the latest promo and expiry date
            query_current = "SELECT promo_selected, expiry_date FROM records WHERE username = %s ORDER BY id DESC LIMIT 1"
            cursor.execute(query_current, (username,))
            result_current = cursor.fetchone()

            # Query to fetch promo history
            query_history = "SELECT promo_selected, date_time FROM records WHERE username = %s ORDER BY id DESC LIMIT 5"
            cursor.execute(query_history, (username,))
            result_history = cursor.fetchall()

            
            db.close()

                # Format results for display
            if result_current:
                  current_promo = result_current[0]
                  expiry_date = result_current[1]
                  history_text = "\n".join([f"{promo} (Used on: {date})" for promo, date in result_history]) or "No previous promos found."

                  messagebox.showinfo(
                  "Usage Details",
                  f"Current Promo: {current_promo}\nExpiry Date: {expiry_date}\nPromo History:\n{history_text}"
               )
            else:
                messagebox.showinfo("Usage Details", "No active promo or history found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching promo: {err}")
        
# Create the user options frame (hidden by default)
    user_options_frame = tk.Frame(dashboard, bg="#f4f0e1", relief="solid", bd=1)
    show_usage_button = tk.Button(
        user_options_frame,
        text="Show Usage",
        bg="#e0e0e0",
        font=("Arial", 10, "bold"),
        command=show_usage
    )
    show_usage_button.pack(fill="x", padx=5, pady=5)

    # "Logout" Button in Options
    def logout():
        user_options_frame.place_forget()
        messagebox.showinfo("Logout", "Logout Successfully")
        dashboard.destroy()
        root.deiconify()  # Show the login screen again

    logout_button = tk.Button(
        user_options_frame,
        text="Logout",
        bg="#e0e0e0",
        font=("Arial", 10, "bold"),
        command=logout
    )
    logout_button.pack(fill="x", padx=5, pady=5)

    # Toggle the user options dropdown
    def toggle_user_options():
        if user_options_frame.winfo_ismapped():  # If already visible, hide it
            user_options_frame.place_forget()
        else:  # Otherwise, show it below the "Welcome" button
            user_options_frame.place(x=42, y=68)
            
# "Welcome (Username)" Button
    welcome_button = tk.Button(
        dashboard,
        text=f"WELCOME ({username})",
        font=("Arial", 12, "bold"),
        bg="#f4f0e1",
        fg="black",
        relief="ridge",
        command=toggle_user_options
    )
    canvas.create_window(150, 50, window=welcome_button)
    # Carrier Selection Label
    carrier_label = tk.Label(
        dashboard,
        text="SELECT YOUR CARRIER:",
        font=("Arial", 16, "bold"),
        bg="#f4f0e1",
        fg="black",
        relief="ridge",
        padx=10, pady=5
    )
    canvas.create_window(650, 120, window=carrier_label)
   
    # Define Promo Transition
    def open_promos(carrier):
        dashboard.destroy()  # Close the dashboard
        show_promos(carrier, username)  # Open the promos window

    # Carrier Buttons
    button_style = {"font": ("Arial", 16, "bold"), "bg": "#fdf5e6", "fg": "black", "width": 18 }

    btn_tnt_smart = tk.Button(dashboard, text="TNT/SMART", **button_style, command=lambda: open_promos("TNT/SMART"))
    canvas.create_window(400, 200, window=btn_tnt_smart)

    btn_globe = tk.Button(dashboard, text="GLOBE", **button_style, command=lambda: open_promos("GLOBE"))
    canvas.create_window(650, 200, window=btn_globe)

    btn_tm = tk.Button(dashboard, text="TM", **button_style, command=lambda: open_promos("TM"))
    canvas.create_window(900, 200, window=btn_tm)

    # Confirm Button (Optional)
    confirm_button = tk.Button(dashboard, text="CONFIRM", **button_style, bg="#f4f0e1", relief="ridge")
    canvas.create_window(650, 300, window=confirm_button)

    # Exit Fullscreen and Close Dashboard
    def on_close():
        root.deiconify()  # Show the login window again
        dashboard.destroy()

    # Allow Escape key to exit fullscreen and close the window
    dashboard.bind("<Escape>", lambda event: on_close())
    dashboard.protocol("WM_DELETE_WINDOW", on_close)

    # Keep reference to the background image
    dashboard.bg_image = bg_image

def show_database_window():
    db_window = tk.Toplevel(root)
    db_window.title("Database Records")
    db_window.geometry("800x600")
    db_window.configure(bg="#ffffff")

    try:
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="retailing_system"
        )
        cursor = db.cursor()
        cursor.execute("SELECT * FROM records")  # Replace 'records' with your table name
        rows = cursor.fetchall()

        # Display records
        for i, row in enumerate(rows):
            tk.Label(db_window, text=row, bg="#ffffff").grid(row=i, column=0)

        db.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")
        
       
# Function to validate login
def validate_login():
    username = entry_username.get()
    password = entry_password.get()

    try:
        # Connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="retailing_system"
        )
        cursor = db.cursor()

        # Check if the username and password match
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()

        if user:
            messagebox.showinfo("Login Successful", "Welcome to the Retailing System!")
            open_dashboard(username)  # Open the dashboard window
        else:
            messagebox.showerror("Login Failed", "Invalid username or password.")

        db.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error: {err}")


        
def open_registration_window():
    global background_image  # Ensure the image is not garbage collected

# Hide the root (old) window
    root.withdraw()
    
    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    registration_window.attributes("-fullscreen", True)  # Full-screen mode

    # Get screen dimensions
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()

    # Set the path to your specific background image
    background_image_path = r"C:/Users/PC/Downloads/360_F_398231758_6dclqrQdYd5hdOCo3M2G2stekJ8JGAZC.jpg"

    # Load and resize the background image
    image = Image.open(background_image_path)
    image = image.resize((screen_width, screen_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image)  # Global to persist

    # Canvas for the background
    canvas = tk.Canvas(registration_window, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Frame for the Registration Inputs (centered)
    register_frame = tk.Frame(registration_window, bg="#ffffff", padx=50, pady=30, highlightbackground="black", highlightthickness=1)
    canvas.create_window(screen_width // 2, screen_height // 2, window=register_frame, anchor="center")

    # Labels and Input Fields
    label_title = tk.Label(register_frame, text="EMAIL & PHONE NUMBER", bg="#ffffff", font=("Arial", 10, "bold"))
    label_title.pack(pady=(0, 10))

    entry_reg_username = tk.Entry(register_frame, width=30, font=("Arial", 10))
    entry_reg_username.pack(pady=(0, 15))

    label_password = tk.Label(register_frame, text="PASSWORD", bg="#ffffff", font=("Arial", 10, "bold"))
    label_password.pack(pady=(0, 10))

    entry_reg_password = tk.Entry(register_frame, show="*", width=30, font=("Arial", 10))
    entry_reg_password.pack(pady=(0, 15))

    label_confirm_password = tk.Label(register_frame, text="CONFIRM PASSWORD", bg="#ffffff", font=("Arial", 10, "bold"))
    label_confirm_password.pack(pady=(0, 10))

    entry_confirm_password = tk.Entry(register_frame, show="*", width=30, font=("Arial", 10))
    entry_confirm_password.pack(pady=(0, 15))

def open_registration_window():
    global background_image  # Ensure the image is not garbage collected

    # Hide the root (old) window
    root.withdraw()

    registration_window = tk.Toplevel(root)
    registration_window.title("Register")
    registration_window.attributes("-fullscreen", True)  # Full-screen mode

    # Get screen dimensions
    screen_width = registration_window.winfo_screenwidth()
    screen_height = registration_window.winfo_screenheight()

    # Set the path to your specific background image
    background_image_path = r"C:/Users/PC/Downloads/360_F_398231758_6dclqrQdYd5hdOCo3M2G2stekJ8JGAZC.jpg"

    # Load and resize the background image
    image = Image.open(background_image_path)
    image = image.resize((screen_width, screen_height), Image.LANCZOS)
    background_image = ImageTk.PhotoImage(image)  # Global to persist

    # Canvas for the background
    canvas = tk.Canvas(registration_window, width=screen_width, height=screen_height, highlightthickness=0)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=background_image, anchor="nw")

    # Frame for the Registration Inputs (centered)
    register_frame = tk.Frame(registration_window, bg="#ffffff", padx=50, pady=30, highlightbackground="black", highlightthickness=1)
    canvas.create_window(screen_width // 2, screen_height // 2, window=register_frame, anchor="center")

    # Labels and Input Fields
    label_title = tk.Label(register_frame, text="EMAIL & PHONE NUMBER", bg="#ffffff", font=("Arial", 10, "bold"))
    label_title.pack(pady=(0, 10))

    entry_reg_username = tk.Entry(register_frame, width=30, font=("Arial", 10))
    entry_reg_username.pack(pady=(0, 15))

    label_password = tk.Label(register_frame, text="PASSWORD", bg="#ffffff", font=("Arial", 10, "bold"))
    label_password.pack(pady=(0, 10))

    entry_reg_password = tk.Entry(register_frame, show="*", width=30, font=("Arial", 10))
    entry_reg_password.pack(pady=(0, 15))

    label_confirm_password = tk.Label(register_frame, text="CONFIRM PASSWORD", bg="#ffffff", font=("Arial", 10, "bold"))
    label_confirm_password.pack(pady=(0, 10))

    entry_confirm_password = tk.Entry(register_frame, show="*", width=30, font=("Arial", 10))
    entry_confirm_password.pack(pady=(0, 15))

    # Register User Function
    def register_user():
        username = entry_reg_username.get()
        password = entry_reg_password.get()
        confirm_password = entry_confirm_password.get()

        if password != confirm_password:
            messagebox.showerror("Registration Failed", "Passwords do not match.")
            return

        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="retailing_system"
            )
            cursor = db.cursor()

            # Check if username exists
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            if cursor.fetchone():
                messagebox.showerror("Registration Failed", "Username already exists.")
            else:
                cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
                db.commit()
                messagebox.showinfo("Registration Successful", "Your account has been created.")
                registration_window.destroy()

            db.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}")

    # Register Button
    button_register = tk.Button(register_frame, text="REGISTER", command=register_user, bg="#e0e0e0", font=("Arial", 10, "bold"), width=20)
    button_register.pack(pady=(10, 0))
    
    # Back Button
    def go_back_to_login():
        registration_window.destroy()
        root.deiconify()

    # Back Button Function
    def go_back():
        registration_window.destroy()  # Close the registration window

    # Back Button
    button_back = tk.Button(register_frame, text="BACK", command=go_back, bg="#e0e0e0", font=("Arial", 10, "bold"), width=20)
    button_back.pack(pady=(5, 0))

    # Escape key to exit full-screen mode
    registration_window.bind("<Escape>", lambda e: registration_window.attributes("-fullscreen", False))
    

def view_records():
    records_window = tk.Toplevel(root)
    records_window.title("Transaction Records")
    records_window.geometry("600x400")

    connection = connect_to_database()
    if connection:
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM transactions")
        records = cursor.fetchall()
        cursor.close()
        connection.close()

        # Display records
        for record in records:
            tk.Label(records_window, text=str(record), font=("Arial", 10)).pack()

# Create the main Tkinter window
root = tk.Tk()
root.title("Retailing System Login")
root.attributes("-fullscreen", True)

# Load the background image
background_image_path = "C:/Users/PC/Downloads/360_F_398231758_6dclqrQdYd5hdOCo3M2G2stekJ8JGAZC.jpg"
image = Image.open(background_image_path)
image = image.resize((root.winfo_screenwidth(), root.winfo_screenheight()), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image)

# Set the background with Canvas
canvas = tk.Canvas(root, width=root.winfo_screenwidth(), height=root.winfo_screenheight())
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=background_image, anchor="nw")

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """Draw a rounded rectangle on a Tkinter canvas."""
    points = [
        (x1 + radius, y1),
        (x2 - radius, y1),
        (x2 - radius, y1 + radius),
        (x2, y1 + radius),
        (x2, y2 - radius),
        (x2 - radius, y2 - radius),
        (x2 - radius, y2),
        (x1 + radius, y2),
        (x1 + radius, y2 - radius),
        (x1, y2 - radius),
        (x1, y1 + radius),
        (x1 + radius, y1 + radius),
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)

# Bigger frame for login inputs
login_frame_width = 500
login_frame_height = 400
login_frame = tk.Frame(root, bg="#ffffff", padx=50, pady=50, highlightbackground="black", highlightthickness=2)
canvas.create_window(root.winfo_screenwidth() * 0.5, root.winfo_screenheight() * 0.5, window=login_frame, anchor="center")

# Title Label
label_title = tk.Label(
    login_frame, 
    text="LOGIN TO YOUR ACCOUNT", 
    bg="#ffffff", 
    font=("Verdana", 14, "bold"), 
    pady=20
)
label_title.pack()

# Username Entry
label_username = tk.Label(login_frame, text="EMAIL OR PHONE NUMBER", bg="#ffffff", font=("Verdana", 12))
label_username.pack(pady=(20, 5))
entry_username = tk.Entry(login_frame, width=40, font=("Verdana", 12))
entry_username.pack(pady=(0, 15))

# Password Entry
label_password = tk.Label(login_frame, text="PASSWORD", bg="#ffffff", font=("Verdana", 12))
label_password.pack(pady=(10, 5))
entry_password = tk.Entry(login_frame, show="*", width=40, font=("Verdana", 12))
entry_password.pack(pady=(0, 15))

# Login Button
button_login = tk.Button(
    login_frame, 
    text="LOGIN", 
    command=validate_login, 
    bg="#007BFF", 
    fg="white", 
    font=("Verdana", 12, "bold"), 
    width=20
)
button_login.pack(pady=(20, 10))

# Register Button
button_register = tk.Button(
    login_frame, 
    text="REGISTER", 
    command=open_registration_window, 
    bg="#e0e0e0", 
    font=("Verdana", 12, "bold"), 
    width=20
)
button_register.pack(pady=(0, 0))

# Start the GUI event loop
root.mainloop()