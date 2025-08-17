import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import csv

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f9")

        
        self.conn = sqlite3.connect("expenses.db")
        self.cursor = self.conn.cursor()
        self.create_table()


        self.setup_ui()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount INTEGER NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
        """)
        self.conn.commit()

    def setup_ui(self):
        # Header Label
        header = tk.Label(self.root, text="Personal Expense Tracker", bg="#3a6ea5", fg="white", font=("Arial", 20, "bold"))
        header.pack(fill="x", pady=10)

        # Import Button
        self.import_button = tk.Button(self.root, text="Import from Paytm CSV", bg="#3a6ea5", fg="white",
                                        font=("Arial", 10, "bold"), command=self.import_csv)
        self.import_button.pack(pady=10)

        # Expense List Section
        self.tree = ttk.Treeview(self.root, columns=("amount", "category", "date", "description"), show="headings")
        self.tree.heading("amount", text="Amount")
        self.tree.heading("category", text="Category")
        self.tree.heading("date", text="Date")
        self.tree.heading("description", text="Description")
        self.tree.pack(pady=10, padx=10, fill="x")

        # Buttons for summary and export
        button_frame = tk.Frame(self.root, bg="#f4f4f9")
        button_frame.pack(pady=10)

        self.summary_button = tk.Button(button_frame, text="View Summary", bg="#3a6ea5", fg="white",
                                        font=("Arial", 10, "bold"), command=self.show_summary)
        self.summary_button.grid(row=0, column=0, padx=10)

        self.export_button = tk.Button(button_frame, text="Export to CSV", bg="#3a6ea5", fg="white",
                                       font=("Arial", 10, "bold"), command=self.export_data)
        self.export_button.grid(row=0, column=1, padx=10)

        self.load_expenses()

    def load_expenses(self):
        self.tree.delete(*self.tree.get_children())
        self.cursor.execute("SELECT * FROM expenses")
        for row in self.cursor.fetchall():
            self.tree.insert("", "end", values=row[1:])

    def import_csv(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        try:
            with open(file_path, "r") as file:
                reader = csv.DictReader(file)

                for row in reader:
                    amount = int(row["Amount"])
                    category = row["Category"] if "Category" in row else "Other"
                    date = row["Date"] if "Date" in row else datetime.now().strftime("%Y-%m-%d")
                    description = row["Description"] if "Description" in row else ""

                    self.cursor.execute("INSERT INTO expenses (amount, category, date, description) VALUES (?, ?, ?, ?)",
                                        (amount, category, date, description))

                self.conn.commit()
                self.load_expenses()
                messagebox.showinfo("Success", "Data imported successfully!")
        except Exception as e:
            messagebox.showerror("Import Error", f"Failed to import CSV: {e}")

    def show_summary(self):
        self.cursor.execute("SELECT category, SUM(amount) FROM expenses GROUP BY category")
        data = self.cursor.fetchall()
        if not data:
            messagebox.showinfo("Summary", "No data to show.")
            return

        categories, amounts = zip(*data)

        plt.figure(figsize=(6, 6))
        plt.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=140)
        plt.title("Expense Summary by Category")
        plt.show()

    def export_data(self):
        self.cursor.execute("SELECT * FROM expenses")
        data = self.cursor.fetchall()

        if not data:
            messagebox.showwarning("Export Error", "No data to export.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV Files", "*.csv")])
        if not file_path:
            return

        with open(file_path, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Category", "Date", "Description"])
            writer.writerows([row[1:] for row in data])

        messagebox.showinfo("Export Success", f"Data exported to {file_path} successfully!")

# Main Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
