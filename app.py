import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error

# -----------------------------
# DATABASE CONFIGURATION
# -----------------------------
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",  # <-- Enter your MySQL password here
    "database": "training_centre"
}

TABLE_COLUMNS = {
    "Course": ["course_id", "course_name", "duration_weeks", "fee"],
    "Module": ["module_id", "course_id", "module_name"],
    "Session": ["session_id", "module_id", "session_date", "topic"],
    "Trainer": ["trainer_id", "trainer_name", "specialization", "phone"],
    "Batch": ["batch_id", "course_id", "trainer_id", "batch_name", "start_date", "end_date", "capacity"],
    "Learner": ["learner_id", "learner_name", "email", "phone"],
    "Enrollment": ["enrollment_id", "learner_id", "batch_id", "enrollment_date", "status"],
    "Attendance": ["attendance_id", "enrollment_id", "session_id", "status"],
    "Assessment": ["assessment_id", "enrollment_id", "assessment_name", "score"],
    "Fees": ["fee_id", "enrollment_id", "amount", "payment_date", "payment_status"],
    "Certificate": ["certificate_id", "enrollment_id", "certificate_number", "issue_date", "eligibility_status"]
}

PRIMARY_KEYS = {
    "Course": "course_id",
    "Module": "module_id",
    "Session": "session_id",
    "Trainer": "trainer_id",
    "Batch": "batch_id",
    "Learner": "learner_id",
    "Enrollment": "enrollment_id",
    "Attendance": "attendance_id",
    "Assessment": "assessment_id",
    "Fees": "fee_id",
    "Certificate": "certificate_id"
}


class Database:
    def __init__(self):
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(**DB_CONFIG)
            if self.connection.is_connected():
                return True
        except Error as exc:
            messagebox.showerror(
                "Database Connection Error",
                "Could not connect to MySQL.\n\n"
                f"Reason: {exc}\n\n"
                "Check DB_CONFIG in app.py and make sure MySQL is running."
            )
        return False

    def ensure_connection(self):
        if self.connection is None or not self.connection.is_connected():
            return self.connect()
        return True

    def fetch_all(self, table):
        if not self.ensure_connection():
            return [], []
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT * FROM `{table}`")
            rows = cursor.fetchall()
            columns = [description[0] for description in cursor.description]
            return columns, rows
        finally:
            cursor.close()

    def insert(self, table, values):
        if not self.ensure_connection():
            return False
        columns = TABLE_COLUMNS[table]
        placeholders = ", ".join(["%s"] * len(columns))
        column_sql = ", ".join(f"`{c}`" for c in columns)
        sql = f"INSERT INTO `{table}` ({column_sql}) VALUES ({placeholders})"
        cursor = self.connection.cursor()
        try:
            cursor.execute(sql, values)
            self.connection.commit()
            return True
        except Error as exc:
            self.connection.rollback()
            messagebox.showerror("Insert Error", str(exc))
            return False
        finally:
            cursor.close()

    def delete(self, table, primary_key_value):
        if not self.ensure_connection():
            return False
        pk = PRIMARY_KEYS[table]
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"DELETE FROM `{table}` WHERE `{pk}` = %s", (primary_key_value,))
            if cursor.rowcount == 0:
                messagebox.showwarning("Not Found", f"No record found with {pk} = {primary_key_value}")
                self.connection.rollback()
                return False
            self.connection.commit()
            return True
        except Error as exc:
            self.connection.rollback()
            messagebox.showerror("Delete Error", str(exc))
            return False
        finally:
            cursor.close()

    def count(self, table):
        if not self.ensure_connection():
            return 0
        cursor = self.connection.cursor()
        try:
            cursor.execute(f"SELECT COUNT(*) FROM `{table}`")
            return cursor.fetchone()[0]
        except Error:
            return 0
        finally:
            cursor.close()

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()


class TrainingManagementUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Training Institute Management System")
        self.geometry("1180x720")
        self.minsize(1000, 650)
        self.configure(bg="#f4f6f9")

        self.db = Database()
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass
        self.style.configure("Treeview", rowheight=30, font=("Helvetica", 11))
        self.style.configure("Treeview.Heading", font=("Helvetica", 11, "bold"))
        self.style.configure("TNotebook.Tab", font=("Helvetica", 11, "bold"), padding=(16, 8))

        self.build_header()
        self.build_tabs()
        self.after(300, self.initial_connect)

    def build_header(self):
        header = tk.Frame(self, bg="#1f4e78", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Training Institute Management System",
            font=("Helvetica", 24, "bold"),
            fg="white",
            bg="#1f4e78"
        ).pack(side="left", padx=24, pady=20)

        self.connection_label = tk.Label(
            header,
            text="● Not connected",
            font=("Helvetica", 11, "bold"),
            fg="#ffd166",
            bg="#1f4e78"
        )
        self.connection_label.pack(side="right", padx=24)

    def build_tabs(self):
        container = tk.Frame(self, bg="#f4f6f9")
        container.pack(fill="both", expand=True, padx=18, pady=16)

        self.notebook = ttk.Notebook(container)
        self.notebook.pack(fill="both", expand=True)

        self.dashboard_tab = tk.Frame(self.notebook, bg="#f4f6f9")
        self.view_tab = tk.Frame(self.notebook, bg="#f4f6f9")
        self.insert_tab = tk.Frame(self.notebook, bg="#f4f6f9")
        self.delete_tab = tk.Frame(self.notebook, bg="#f4f6f9")

        self.notebook.add(self.dashboard_tab, text="Dashboard")
        self.notebook.add(self.view_tab, text="View Records")
        self.notebook.add(self.insert_tab, text="Insert Record")
        self.notebook.add(self.delete_tab, text="Delete Record")

        self.build_dashboard()
        self.build_view_tab()
        self.build_insert_tab()
        self.build_delete_tab()

    def initial_connect(self):
        if self.db.connect():
            self.connection_label.config(text="● Connected", fg="#7CFC98")
            self.refresh_dashboard()
            self.load_table_data()
        else:
            self.connection_label.config(text="● Not connected", fg="#ffd166")

    def section_title(self, parent, title, subtitle=None):
        tk.Label(parent, text=title, font=("Helvetica", 20, "bold"), bg="#f4f6f9", fg="#1f2937").pack(anchor="w", padx=20, pady=(18, 2))
        if subtitle:
            tk.Label(parent, text=subtitle, font=("Helvetica", 11), bg="#f4f6f9", fg="#6b7280").pack(anchor="w", padx=20, pady=(0, 12))

    def build_dashboard(self):
        self.section_title(self.dashboard_tab, "Project Dashboard", "Quick overview of the database records")

        button_row = tk.Frame(self.dashboard_tab, bg="#f4f6f9")
        button_row.pack(fill="x", padx=20, pady=(0, 12))
        tk.Button(button_row, text="Refresh Dashboard", command=self.refresh_dashboard, bg="#1f4e78", fg="white", relief="flat", padx=16, pady=8).pack(side="left")
        tk.Button(button_row, text="Reconnect", command=self.reconnect, bg="#374151", fg="white", relief="flat", padx=16, pady=8).pack(side="left", padx=10)

        self.cards_frame = tk.Frame(self.dashboard_tab, bg="#f4f6f9")
        self.cards_frame.pack(fill="both", expand=True, padx=20, pady=8)

    def refresh_dashboard(self):
        for widget in self.cards_frame.winfo_children():
            widget.destroy()

        tables = list(TABLE_COLUMNS.keys())
        for idx, table in enumerate(tables):
            row = idx // 4
            col = idx % 4
            self.cards_frame.grid_columnconfigure(col, weight=1)
            count = self.db.count(table)
            card = tk.Frame(self.cards_frame, bg="white", bd=1, relief="solid")
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            tk.Label(card, text=table, font=("Helvetica", 13, "bold"), bg="white", fg="#374151").pack(pady=(18, 5))
            tk.Label(card, text=str(count), font=("Helvetica", 26, "bold"), bg="white", fg="#1f4e78").pack(pady=(0, 18))

    def build_view_tab(self):
        self.section_title(self.view_tab, "View Records", "Select any table to display its current MySQL records")

        controls = tk.Frame(self.view_tab, bg="#f4f6f9")
        controls.pack(fill="x", padx=20, pady=(0, 10))

        tk.Label(controls, text="Table:", bg="#f4f6f9", font=("Helvetica", 11, "bold")).pack(side="left")
        self.view_table_var = tk.StringVar(value="Course")
        table_combo = ttk.Combobox(controls, textvariable=self.view_table_var, values=list(TABLE_COLUMNS.keys()), state="readonly", width=24)
        table_combo.pack(side="left", padx=8)
        table_combo.bind("<<ComboboxSelected>>", lambda _e: self.load_table_data())

        tk.Button(controls, text="Refresh", command=self.load_table_data, bg="#1f4e78", fg="white", relief="flat", padx=16, pady=6).pack(side="left", padx=8)

        tree_frame = tk.Frame(self.view_tab, bg="white")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        self.tree = ttk.Treeview(tree_frame, show="headings")
        yscroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

    def load_table_data(self):
        table = self.view_table_var.get()
        columns, rows = self.db.fetch_all(table)

        self.tree.delete(*self.tree.get_children())
        self.tree["columns"] = columns

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            width = max(120, min(220, len(col) * 14))
            self.tree.column(col, width=width, anchor="center")

        for row in rows:
            self.tree.insert("", "end", values=row)

    def build_insert_tab(self):
        self.section_title(self.insert_tab, "Insert Record", "Choose a table, enter values, and save the record")

        top = tk.Frame(self.insert_tab, bg="#f4f6f9")
        top.pack(fill="x", padx=20)
        tk.Label(top, text="Table:", bg="#f4f6f9", font=("Helvetica", 11, "bold")).pack(side="left")
        self.insert_table_var = tk.StringVar(value="Course")
        combo = ttk.Combobox(top, textvariable=self.insert_table_var, values=list(TABLE_COLUMNS.keys()), state="readonly", width=24)
        combo.pack(side="left", padx=8)
        combo.bind("<<ComboboxSelected>>", lambda _e: self.render_insert_form())

        self.insert_form_frame = tk.Frame(self.insert_tab, bg="white", bd=1, relief="solid")
        self.insert_form_frame.pack(fill="both", expand=True, padx=20, pady=18)
        self.insert_entries = {}
        self.render_insert_form()

    def render_insert_form(self):
        for widget in self.insert_form_frame.winfo_children():
            widget.destroy()
        self.insert_entries.clear()

        table = self.insert_table_var.get()
        columns = TABLE_COLUMNS[table]

        form = tk.Frame(self.insert_form_frame, bg="white")
        form.pack(padx=35, pady=28, anchor="nw")

        for i, col in enumerate(columns):
            tk.Label(form, text=col.replace("_", " ").title(), font=("Helvetica", 11, "bold"), bg="white", fg="#374151").grid(row=i, column=0, sticky="w", padx=(0, 20), pady=8)
            entry = ttk.Entry(form, width=42)
            entry.grid(row=i, column=1, sticky="w", pady=8)
            self.insert_entries[col] = entry

        hint = tk.Label(
            form,
            text="Date format: YYYY-MM-DD   •   Numeric fields should contain numbers only",
            font=("Helvetica", 10), bg="white", fg="#6b7280"
        )
        hint.grid(row=len(columns), column=0, columnspan=2, sticky="w", pady=(12, 4))

        tk.Button(
            form,
            text="Insert Record",
            command=self.insert_record,
            bg="#15803d",
            fg="white",
            relief="flat",
            padx=20,
            pady=9,
            font=("Helvetica", 11, "bold")
        ).grid(row=len(columns) + 1, column=0, columnspan=2, sticky="w", pady=(12, 0))

    def insert_record(self):
        table = self.insert_table_var.get()
        values = [self.insert_entries[col].get().strip() for col in TABLE_COLUMNS[table]]

        if any(value == "" for value in values):
            messagebox.showwarning("Missing Data", "Please fill in every field before inserting.")
            return

        if self.db.insert(table, values):
            messagebox.showinfo("Success", f"Record inserted into {table} successfully.")
            for entry in self.insert_entries.values():
                entry.delete(0, tk.END)
            self.view_table_var.set(table)
            self.load_table_data()
            self.refresh_dashboard()

    def build_delete_tab(self):
        self.section_title(self.delete_tab, "Delete Record", "Delete a record using the table's primary key")

        panel = tk.Frame(self.delete_tab, bg="white", bd=1, relief="solid")
        panel.pack(fill="x", padx=20, pady=18)

        form = tk.Frame(panel, bg="white")
        form.pack(padx=35, pady=32, anchor="w")

        tk.Label(form, text="Table", font=("Helvetica", 11, "bold"), bg="white").grid(row=0, column=0, sticky="w", padx=(0, 20), pady=8)
        self.delete_table_var = tk.StringVar(value="Course")
        combo = ttk.Combobox(form, textvariable=self.delete_table_var, values=list(TABLE_COLUMNS.keys()), state="readonly", width=28)
        combo.grid(row=0, column=1, sticky="w", pady=8)
        combo.bind("<<ComboboxSelected>>", lambda _e: self.update_delete_label())

        self.delete_key_label = tk.Label(form, text="Course Id", font=("Helvetica", 11, "bold"), bg="white")
        self.delete_key_label.grid(row=1, column=0, sticky="w", padx=(0, 20), pady=8)
        self.delete_key_entry = ttk.Entry(form, width=31)
        self.delete_key_entry.grid(row=1, column=1, sticky="w", pady=8)

        tk.Button(
            form,
            text="Delete Record",
            command=self.delete_record,
            bg="#b91c1c",
            fg="white",
            relief="flat",
            padx=20,
            pady=9,
            font=("Helvetica", 11, "bold")
        ).grid(row=2, column=0, columnspan=2, sticky="w", pady=(15, 0))

    def update_delete_label(self):
        pk = PRIMARY_KEYS[self.delete_table_var.get()]
        self.delete_key_label.config(text=pk.replace("_", " ").title())
        self.delete_key_entry.delete(0, tk.END)

    def delete_record(self):
        table = self.delete_table_var.get()
        pk = PRIMARY_KEYS[table]
        value = self.delete_key_entry.get().strip()
        if not value:
            messagebox.showwarning("Missing ID", f"Enter the {pk} value to delete.")
            return

        confirmed = messagebox.askyesno("Confirm Delete", f"Delete {table} record where {pk} = {value}?")
        if not confirmed:
            return

        if self.db.delete(table, value):
            messagebox.showinfo("Success", "Record deleted successfully.")
            self.delete_key_entry.delete(0, tk.END)
            self.view_table_var.set(table)
            self.load_table_data()
            self.refresh_dashboard()

    def reconnect(self):
        self.db.close()
        if self.db.connect():
            self.connection_label.config(text="● Connected", fg="#7CFC98")
            messagebox.showinfo("Connected", "MySQL connection successful.")
            self.refresh_dashboard()
            self.load_table_data()
        else:
            self.connection_label.config(text="● Not connected", fg="#ffd166")

    def on_close(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = TrainingManagementUI()
    app.mainloop()
