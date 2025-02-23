import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector

class RecordsWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Records Dashboard")
        self.root.geometry("800x600")
        self.root.configure(bg="#C4DCC3")

        # Create a Tab Frame to switch between views
        tab_frame = tk.Frame(self.root, bg="#C4DCC3")
        tab_frame.pack(pady=20)

        # Buttons to switch between views
        button_user_records = tk.Button(tab_frame, text="USERS", command=self.show_user_records, bg="#e0e0e0", font=("Arial", 10, "bold"))
        button_user_records.pack(side=tk.LEFT, padx=10)

        button_transaction_records = tk.Button(tab_frame, text="RECORDS", command=self.show_records, bg="#e0e0e0", font=("Arial", 10, "bold"))
        button_transaction_records.pack(side=tk.LEFT)

        # Delete Buttons
        self.delete_selected_button = tk.Button(tab_frame, text="DELETE SELECTED TRANSACTION", command=self.delete_selected_transaction, bg="#e06666", fg="white", font=("Arial", 10, "bold"))
        self.delete_selected_button.pack(side=tk.LEFT, padx=10)

        self.delete_all_button = tk.Button(tab_frame, text="DELETE ALL CUSTOMER RECORDS", command=self.delete_all_customer_records, bg="#b22222", fg="white", font=("Arial", 10, "bold"))
        self.delete_all_button.pack(side=tk.LEFT, padx=10)

        # Container for the Treeview widgets (Table view)
        self.table_frame = tk.Frame(self.root)
        self.table_frame.pack(fill=tk.BOTH, expand=True)
        self.current_view = None  # To track which table is currently visible

    # Function to show user records in a table
    def show_user_records(self):
        self.current_view = "users"
        self.load_data("SELECT * FROM users", ("ID", "Username", "Password"))

    # Function to show transaction records in a table
    def show_records(self):
        self.current_view = "records"
        self.load_data(
            "SELECT id, username, promo_selected, amount_paid, change_amount, date_time, expiry_date FROM records",
            ("ID", "Username", "Promo Selected", "Amount Paid", "Change Amount", "Date and Time", "Expiry Date")
        )
        
       
    # Function to load data into the Treeview
    def load_data(self, query, columns):
        # Clear previous table
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Treeview setup
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Fetch and load data into the table
        try:
            db = mysql.connector.connect(host="localhost", user="root", password="", database="retailing_system")
            cursor = db.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                self.tree.insert("", tk.END, values=row)
            db.close()
        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))

    # Function to delete the selected transaction
    def delete_selected_transaction(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Selection Required", "Please select a transaction to delete.")
                return

            # Get selected record ID
            selected_record = self.tree.item(selected_item, "values")
            record_id = selected_record[0]  # Assuming the first column is the ID

            # Confirm Deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete transaction ID {record_id}?")
            if not confirm:
                return

            # Execute Delete Query
            db = mysql.connector.connect(host="localhost", user="root", password="", database="retailing_system")
            cursor = db.cursor()
            delete_query = "DELETE FROM records WHERE id = %s"
            cursor.execute(delete_query, (record_id,))
            db.commit()
            db.close()

            # Reload Data
            self.show_records()
            messagebox.showinfo("Success", f"Transaction ID {record_id} has been deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Function to delete all records for a selected customer
    def delete_all_customer_records(self):
        try:
            selected_item = self.tree.selection()
            if not selected_item:
                messagebox.showwarning("Selection Required", "Please select a customer's transaction to delete all records.")
                return

            # Get selected Username/Phone Number
            selected_record = self.tree.item(selected_item, "values")
            customer_username = selected_record[1]  # Assuming column 2 is Username/Phone Number

            # Confirm Deletion
            confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete all records for '{customer_username}'?")
            if not confirm:
                return

            # Execute Delete Query
            db = mysql.connector.connect(host="localhost", user="root", password="", database="retailing_system")
            cursor = db.cursor()
            delete_query = "DELETE FROM records WHERE username = %s"
            cursor.execute(delete_query, (customer_username,))
            db.commit()
            db.close()

            # Reload Data
            self.show_records()
            messagebox.showinfo("Success", f"All records for '{customer_username}' have been deleted.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Main part to run the application
def main():
    root = tk.Tk()
    records_window = RecordsWindow(root)
    root.mainloop()

# Run the main function
main()
