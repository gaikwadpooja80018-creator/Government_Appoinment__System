import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# DATABASE CONNECTION
conn = sqlite3.connect("appointments.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    token TEXT UNIQUE,
    name TEXT,
    mobile TEXT,
    department TEXT,
    date TEXT,
    status TEXT
)
""")
conn.commit()


# MAIN WINDOW
root = tk.Tk()
root.title("Government Office Appointment System")
root.geometry("1100x700")
root.configure(bg="#edf2f7")

# COLORS
BLUE = "#163A5F"
LIGHT_BLUE = "#2874A6"
GREEN = "#148F77"
RED = "#C0392B"
WHITE = "#FFFFFF"


# ---------------- LOGIN PAGE ----------------

def login_page():

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#163A5F")

    frame = tk.Frame(root, bg=WHITE, padx=40, pady=40)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    tk.Label(
        frame,
        text="ADMIN LOGIN",
        font=("Arial", 24, "bold"),
        bg=WHITE,
        fg=BLUE
    ).pack(pady=20)

    tk.Label(frame, text="Username", bg=WHITE).pack()

    username = tk.Entry(frame, width=30, font=("Arial", 12))
    username.pack(pady=10)

    tk.Label(frame, text="Password", bg=WHITE).pack()

    password = tk.Entry(
        frame,
        width=30,
        font=("Arial", 12),
        show="*"
    )
    password.pack(pady=10)

    def check_login():

        if username.get() == "admin" and password.get() == "admin123":
            dashboard()
        else:
            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password!"
            )

    tk.Button(
        frame,
        text="LOGIN",
        command=check_login,
        bg=GREEN,
        fg=WHITE,
        width=25,
        font=("Arial", 12, "bold")
    ).pack(pady=20)

    tk.Label(
        frame,
        text="Government Office Management System",
        bg=WHITE,
        fg="gray"
    ).pack()


# ---------------- DASHBOARD ----------------

def dashboard():

    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#edf2f7")

    header = tk.Frame(root, bg=BLUE, height=90)
    header.pack(fill="x")

    tk.Label(
        header,
        text="GOVERNMENT OFFICE APPOINTMENT SYSTEM",
        font=("Arial", 20, "bold"),
        bg=BLUE,
        fg=WHITE
    ).pack(side="left", padx=25, pady=25)

    tk.Button(
        header,
        text="LOGOUT",
        command=login_page,
        bg=RED,
        fg=WHITE
    ).pack(side="right", padx=25)

    # DASHBOARD COUNTS

    stats = tk.Frame(root, bg="#edf2f7")
    stats.pack(fill="x", padx=20, pady=20)

    cursor.execute("SELECT COUNT(*) FROM appointments")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM appointments WHERE status='Pending'"
    )
    pending = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM appointments WHERE status='Completed'"
    )
    completed = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM appointments WHERE status='In Progress'"
    )
    progress = cursor.fetchone()[0]

    cards = [
        ("TOTAL APPOINTMENTS", total, BLUE),
        ("PENDING", pending, "#D68910"),
        ("IN PROGRESS", progress, LIGHT_BLUE),
        ("COMPLETED", completed, GREEN)
    ]

    for title, number, color in cards:

        card = tk.Frame(stats, bg=WHITE, padx=20, pady=15)
        card.pack(side="left", expand=True, fill="x", padx=8)

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=color,
            font=("Arial", 11, "bold")
        ).pack()

        tk.Label(
            card,
            text=str(number),
            bg=WHITE,
            fg=BLUE,
            font=("Arial", 25, "bold")
        ).pack(pady=8)

    # MAIN BUTTONS

    buttons = tk.Frame(root, bg="#edf2f7")
    buttons.pack(pady=10)

    tk.Button(
        buttons,
        text="BOOK APPOINTMENT",
        command=booking_window,
        bg=GREEN,
        fg=WHITE,
        width=22,
        height=2
    ).pack(side="left", padx=10)

    tk.Button(
        buttons,
        text="VIEW APPOINTMENTS",
        command=view_window,
        bg=LIGHT_BLUE,
        fg=WHITE,
        width=22,
        height=2
    ).pack(side="left", padx=10)

    tk.Button(
        buttons,
        text="REFRESH DASHBOARD",
        command=dashboard,
        bg=BLUE,
        fg=WHITE,
        width=22,
        height=2
    ).pack(side="left", padx=10)

    tk.Label(
        root,
        text="Welcome to Government Office Administration",
        bg="#edf2f7",
        fg=BLUE,
        font=("Arial", 16, "bold")
    ).pack(pady=30)


# ---------------- BOOK APPOINTMENT ----------------

def booking_window():

    win = tk.Toplevel(root)
    win.title("Book Appointment")
    win.geometry("450x550")
    win.configure(bg=WHITE)

    tk.Label(
        win,
        text="NEW APPOINTMENT",
        font=("Arial", 18, "bold"),
        bg=WHITE,
        fg=BLUE
    ).pack(pady=20)

    fields = {}

    labels = [
        "Full Name",
        "Mobile Number",
        "Appointment Date (DD-MM-YYYY)"
    ]

    for label in labels:

        tk.Label(
            win,
            text=label,
            bg=WHITE,
            font=("Arial", 11)
        ).pack(pady=5)

        entry = tk.Entry(win, width=35)
        entry.pack(pady=5)

        fields[label] = entry

    tk.Label(
        win,
        text="Select Department",
        bg=WHITE
    ).pack(pady=5)

    dept = ttk.Combobox(
        win,
        values=[
            "Aadhaar Department",
            "Revenue Department",
            "Certificate Department",
            "Pension Department",
            "Other"
        ],
        state="readonly",
        width=32
    )

    dept.pack(pady=5)
    dept.set("Select Department")

    def save_appointment():

        name = fields["Full Name"].get().strip()
        mobile = fields["Mobile Number"].get().strip()
        date = fields["Appointment Date (DD-MM-YYYY)"].get().strip()
        department = dept.get()

        if not name or not mobile or not date:
            messagebox.showwarning(
                "Warning", "Please fill all details!"
            )
            return

        if not mobile.isdigit() or len(mobile) != 10:
            messagebox.showwarning(
                "Warning", "Enter valid 10 digit mobile number!"
            )
            return

        if department == "Select Department":
            messagebox.showwarning(
                "Warning", "Select Department!"
            )
            return

        try:
            appointment_date = datetime.strptime(date, "%d-%m-%Y")

            if appointment_date.date() < datetime.today().date():
                messagebox.showwarning(
                    "Warning", "Select a future date!"
                )
                return

        except ValueError:
            messagebox.showwarning(
                "Warning", "Use DD-MM-YYYY date format!"
            )
            return

        try:

            cursor.execute("""
                INSERT INTO appointments
                (token, name, mobile, department, date, status)
                VALUES (?, ?, ?, ?, ?, ?)
            """, ("TEMP", name, mobile, department, date, "Pending"))

            appointment_id = cursor.lastrowid
            token = "TKN" + str(appointment_id).zfill(4)

            cursor.execute(
                "UPDATE appointments SET token=? WHERE id=?",
                (token, appointment_id)
            )

            conn.commit()

            messagebox.showinfo(
                "Success",
                f"Appointment Booked Successfully!\n\nToken Number: {token}"
            )

            win.destroy()
            dashboard()

        except sqlite3.IntegrityError:
            conn.rollback()
            messagebox.showerror(
                "Database Error",
                "Appointment could not be saved. Please try again."
            )

    tk.Button(
        win,
        text="BOOK APPOINTMENT",
        command=save_appointment,
        bg=GREEN,
        fg=WHITE,
        font=("Arial", 12, "bold"),
        width=25
    ).pack(pady=25)


# ---------------- VIEW APPOINTMENTS ----------------

def view_window():

    win = tk.Toplevel(root)
    win.title("All Appointments")
    win.geometry("1050x550")

    tk.Label(
        win,
        text="APPOINTMENT RECORDS",
        font=("Arial", 18, "bold"),
        fg=BLUE
    ).pack(pady=15)

    search_frame = tk.Frame(win)
    search_frame.pack(pady=10)

    tk.Label(
        search_frame,
        text="Search Token:"
    ).pack(side="left", padx=5)

    search_entry = tk.Entry(search_frame, width=25)
    search_entry.pack(side="left", padx=5)

    columns = (
        "ID", "Token", "Name", "Mobile",
        "Department", "Date", "Status"
    )

    table = ttk.Treeview(
        win,
        columns=columns,
        show="headings",
        height=12
    )

    for col in columns:
        table.heading(col, text=col)
        table.column(col, width=135, anchor="center")

    table.pack(fill="both", expand=True, padx=15, pady=10)

    def load_records(search=""):

        for item in table.get_children():
            table.delete(item)

        if search:
            cursor.execute(
                "SELECT * FROM appointments WHERE token=?",
                (search,)
            )
        else:
            cursor.execute(
                "SELECT * FROM appointments ORDER BY id DESC"
            )

        for row in cursor.fetchall():
            table.insert("", tk.END, values=row)

    def search_record():
        load_records(search_entry.get().strip())

    def update_record():

        selected = table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select an appointment!"
            )
            return

        values = table.item(selected[0], "values")
        token = values[1]

        status_win = tk.Toplevel(win)
        status_win.title("Update Status")
        status_win.geometry("300x200")

        tk.Label(
            status_win,
            text="Select New Status",
            font=("Arial", 12, "bold")
        ).pack(pady=15)

        status = ttk.Combobox(
            status_win,
            values=["Pending", "In Progress", "Completed"],
            state="readonly"
        )

        status.pack(pady=10)
        status.set(values[6])

        def save_status():

            if not status.get():
                return

            cursor.execute(
                "UPDATE appointments SET status=? WHERE token=?",
                (status.get(), token)
            )

            conn.commit()

            status_win.destroy()
            load_records()

            messagebox.showinfo(
                "Success", "Status Updated Successfully!"
            )

        tk.Button(
            status_win,
            text="UPDATE",
            command=save_status,
            bg=GREEN,
            fg=WHITE
        ).pack(pady=15)

    def delete_record():

        selected = table.selection()

        if not selected:
            messagebox.showwarning(
                "Warning", "Select an appointment!"
            )
            return

        values = table.item(selected[0], "values")
        token = values[1]

        confirm = messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete this appointment?"
        )

        if confirm:

            cursor.execute(
                "DELETE FROM appointments WHERE token=?",
                (token,)
            )

            conn.commit()

            load_records()

            messagebox.showinfo(
                "Success", "Appointment Deleted!"
            )

    tk.Button(
        search_frame,
        text="SEARCH",
        command=search_record,
        bg=LIGHT_BLUE,
        fg=WHITE
    ).pack(side="left", padx=5)

    tk.Button(
        search_frame,
        text="SHOW ALL",
        command=lambda: load_records(),
        bg=GREEN,
        fg=WHITE
    ).pack(side="left", padx=5)

    action_frame = tk.Frame(win)
    action_frame.pack(pady=10)

    tk.Button(
        action_frame,
        text="UPDATE STATUS",
        command=update_record,
        bg=LIGHT_BLUE,
        fg=WHITE,
        width=20
    ).pack(side="left", padx=10)

    tk.Button(
        action_frame,
        text="DELETE APPOINTMENT",
        command=delete_record,
        bg=RED,
        fg=WHITE,
        width=20
    ).pack(side="left", padx=10)

    load_records()


# ---------------- APPLICATION CLOSE ----------------

def close_application():

    conn.close()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", close_application)

# START APPLICATION
login_page()

root.mainloop()