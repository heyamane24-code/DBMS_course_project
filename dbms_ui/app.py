import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from mysql.connector import Error
from datetime import datetime

# ============================================================
# DATABASE CONFIGURATION
# Change ONLY these values to match your MySQL Workbench setup.
# ============================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",          # <-- enter your MySQL password
    "database": "training_management"  # <-- change if your schema name is different
}

TABLES = {
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
    "Certificate": ["certificate_id", "enrollment_id", "certificate_number", "issue_date", "eligibility_status"],
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
    "Certificate": "certificate_id",
}

DATE_COLUMNS = {"session_date", "start_date", "end_date", "enrollment_date", "payment_date", "issue_date"}
INTEGER_COLUMNS = {"duration_weeks", "capacity", "score"}
DECIMAL_COLUMNS = {"fee", "amount"}

# Professional neutral palette
BG = "#F4F7FB"
PANEL = "#FFFFFF"
SIDEBAR = "#111827"
SIDEBAR_HOVER = "#1F2937"
ACCENT = "#2563EB"
ACCENT_DARK = "#1D4ED8"
TEXT = "#111827"
MUTED = "#6B7280"
BORDER = "#E5E7EB"
SUCCESS = "#0F766E"
DANGER = "#B91C1C"
WARNING = "#B45309"


class Database:
    def __init__(self):
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**DB_CONFIG)
            return self.conn.is_connected()
        except Error as exc:
            messagebox.showerror(
                "Database Connection Error",
                "Could not connect to MySQL.\n\n"
                f"Reason: {exc}\n\n"
                "Check DB_CONFIG in app.py and make sure MySQL is running."
            )
            return False

    def ensure(self):
        if self.conn is None or not self.conn.is_connected():
            return self.connect()
        return True

    def query(self, sql, params=None, fetch=False):
        if not self.ensure():
            raise RuntimeError("Database connection unavailable")
        cursor = self.conn.cursor()
        try:
            cursor.execute(sql, params or ())
            if fetch:
                rows = cursor.fetchall()
                cols = [d[0] for d in cursor.description] if cursor.description else []
                return cols, rows
            self.conn.commit()
            return cursor.rowcount
        except Exception:
            self.conn.rollback()
            raise
        finally:
            cursor.close()

    def close(self):
        try:
            if self.conn and self.conn.is_connected():
                self.conn.close()
        except Exception:
            pass


class ProfessionalDBMSApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Training Institute Management System")
        self.geometry("1360x780")
        self.minsize(1150, 680)
        self.configure(bg=BG)
        self.db = Database()
        self.current_page = None
        self.nav_buttons = {}
        self.active_table = tk.StringVar(value="Learner")

        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self._configure_style()
        self._build_shell()
        if self.db.connect():
            self.show_dashboard()
        else:
            self.show_connection_help()

    def _configure_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("Treeview",
                        background=PANEL,
                        fieldbackground=PANEL,
                        foreground=TEXT,
                        rowheight=32,
                        borderwidth=0,
                        font=("Segoe UI", 10))
        style.configure("Treeview.Heading",
                        background="#EEF2F7",
                        foreground=TEXT,
                        relief="flat",
                        font=("Segoe UI Semibold", 10),
                        padding=(8, 8))
        style.map("Treeview", background=[("selected", "#DBEAFE")], foreground=[("selected", TEXT)])
        style.map("Treeview.Heading", background=[("active", "#E5EAF2")])

        style.configure("TCombobox", padding=7, font=("Segoe UI", 10))
        style.configure("TEntry", padding=7, font=("Segoe UI", 10))

    def _build_shell(self):
        self.sidebar = tk.Frame(self, bg=SIDEBAR, width=235)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(25, 28))
        tk.Label(brand, text="TIMS", bg=SIDEBAR, fg="white",
                 font=("Segoe UI Semibold", 24)).pack(anchor="w")
        tk.Label(brand, text="Training Institute\nManagement System", bg=SIDEBAR, fg="#9CA3AF",
                 justify="left", font=("Segoe UI", 9)).pack(anchor="w", pady=(3, 0))

        nav = [
            ("Dashboard", self.show_dashboard),
            ("View Records", self.show_records),
            ("Insert Record", self.show_insert),
            ("Delete Record", self.show_delete),
            ("Database Info", self.show_db_info),
        ]
        for label, cmd in nav:
            btn = tk.Button(self.sidebar, text=label, command=cmd,
                            bg=SIDEBAR, fg="#D1D5DB", activebackground=SIDEBAR_HOVER,
                            activeforeground="white", bd=0, relief="flat",
                            anchor="w", padx=22, pady=12,
                            font=("Segoe UI Semibold", 10), cursor="hand2")
            btn.pack(fill="x", padx=10, pady=2)
            self.nav_buttons[label] = btn

        bottom = tk.Frame(self.sidebar, bg=SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=20, pady=20)
        tk.Label(bottom, text="MySQL Connected UI", bg=SIDEBAR, fg="#6B7280",
                 font=("Segoe UI", 8)).pack(anchor="w")
        tk.Label(bottom, text="DBMS Course Project", bg=SIDEBAR, fg="#6B7280",
                 font=("Segoe UI", 8)).pack(anchor="w")

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.topbar = tk.Frame(self.main, bg=PANEL, height=68, highlightthickness=1, highlightbackground=BORDER)
        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        self.page_title = tk.Label(self.topbar, text="Dashboard", bg=PANEL, fg=TEXT,
                                   font=("Segoe UI Semibold", 18))
        self.page_title.pack(side="left", padx=28)

        self.status_label = tk.Label(self.topbar, text="● Connected", bg=PANEL, fg=SUCCESS,
                                     font=("Segoe UI Semibold", 9))
        self.status_label.pack(side="right", padx=28)

        self.content = tk.Frame(self.main, bg=BG)
        self.content.pack(fill="both", expand=True, padx=28, pady=24)

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def set_active_nav(self, label):
        for name, btn in self.nav_buttons.items():
            if name == label:
                btn.configure(bg=ACCENT, fg="white")
            else:
                btn.configure(bg=SIDEBAR, fg="#D1D5DB")

    def section_header(self, title, subtitle=""):
        wrap = tk.Frame(self.content, bg=BG)
        wrap.pack(fill="x", pady=(0, 18))
        tk.Label(wrap, text=title, bg=BG, fg=TEXT,
                 font=("Segoe UI Semibold", 22)).pack(anchor="w")
        if subtitle:
            tk.Label(wrap, text=subtitle, bg=BG, fg=MUTED,
                     font=("Segoe UI", 10)).pack(anchor="w", pady=(4, 0))
        return wrap

    def card(self, parent, **kwargs):
        return tk.Frame(parent, bg=PANEL, highlightthickness=1, highlightbackground=BORDER, **kwargs)

    def primary_button(self, parent, text, command, width=15):
        return tk.Button(parent, text=text, command=command, bg=ACCENT, fg="white",
                         activebackground=ACCENT_DARK, activeforeground="white",
                         bd=0, relief="flat", padx=16, pady=9,
                         width=width, font=("Segoe UI Semibold", 9), cursor="hand2")

    def secondary_button(self, parent, text, command, width=15):
        return tk.Button(parent, text=text, command=command, bg="#EEF2F7", fg=TEXT,
                         activebackground="#E5E7EB", bd=0, relief="flat",
                         padx=16, pady=9, width=width,
                         font=("Segoe UI Semibold", 9), cursor="hand2")

    # ---------------- DASHBOARD ----------------
    def show_dashboard(self):
        self.clear_content()
        self.page_title.configure(text="Dashboard")
        self.set_active_nav("Dashboard")
        self.section_header("Dashboard", "Overview of your training institute database")

        counts = {}
        for table in ["Course", "Trainer", "Learner", "Enrollment", "Batch", "Certificate"]:
            try:
                _, rows = self.db.query(f"SELECT COUNT(*) FROM `{table}`", fetch=True)
                counts[table] = rows[0][0]
            except Exception:
                counts[table] = "—"

        cards = tk.Frame(self.content, bg=BG)
        cards.pack(fill="x")
        labels = [
            ("Courses", counts.get("Course", "—"), "Available programs"),
            ("Learners", counts.get("Learner", "—"), "Registered learners"),
            ("Enrollments", counts.get("Enrollment", "—"), "Total enrollments"),
            ("Batches", counts.get("Batch", "—"), "Active course batches"),
        ]
        for i, (title, value, note) in enumerate(labels):
            c = self.card(cards, height=128)
            c.grid(row=0, column=i, padx=(0 if i == 0 else 10, 0), sticky="nsew")
            c.grid_propagate(False)
            cards.grid_columnconfigure(i, weight=1)
            tk.Label(c, text=title, bg=PANEL, fg=MUTED, font=("Segoe UI Semibold", 9)).pack(anchor="w", padx=18, pady=(17, 2))
            tk.Label(c, text=str(value), bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 28)).pack(anchor="w", padx=18)
            tk.Label(c, text=note, bg=PANEL, fg="#9CA3AF", font=("Segoe UI", 8)).pack(anchor="w", padx=18, pady=(2, 0))

        lower = tk.Frame(self.content, bg=BG)
        lower.pack(fill="both", expand=True, pady=(18, 0))
        lower.grid_columnconfigure(0, weight=3)
        lower.grid_columnconfigure(1, weight=2)
        lower.grid_rowconfigure(0, weight=1)

        recent = self.card(lower)
        recent.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        tk.Label(recent, text="Recent Enrollments", bg=PANEL, fg=TEXT,
                 font=("Segoe UI Semibold", 13)).pack(anchor="w", padx=18, pady=(16, 8))
        tree_holder = tk.Frame(recent, bg=PANEL)
        tree_holder.pack(fill="both", expand=True, padx=14, pady=(0, 14))
        cols = ("ID", "Learner", "Batch", "Date", "Status")
        tree = ttk.Treeview(tree_holder, columns=cols, show="headings", height=10)
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")
        tree.column("Learner", width=145, anchor="w")
        try:
            sql = """
                SELECT e.enrollment_id, l.learner_name, b.batch_name,
                       e.enrollment_date, e.status
                FROM Enrollment e
                JOIN Learner l ON e.learner_id = l.learner_id
                JOIN Batch b ON e.batch_id = b.batch_id
                ORDER BY e.enrollment_date DESC, e.enrollment_id DESC
                LIMIT 8
            """
            _, rows = self.db.query(sql, fetch=True)
            for row in rows:
                tree.insert("", "end", values=row)
        except Exception:
            pass
        tree.pack(fill="both", expand=True)

        actions = self.card(lower)
        actions.grid(row=0, column=1, sticky="nsew", padx=(10, 0))
        tk.Label(actions, text="Quick Actions", bg=PANEL, fg=TEXT,
                 font=("Segoe UI Semibold", 13)).pack(anchor="w", padx=18, pady=(16, 12))
        self.primary_button(actions, "View Records", self.show_records, 22).pack(padx=18, pady=6, fill="x")
        self.primary_button(actions, "Insert Record", self.show_insert, 22).pack(padx=18, pady=6, fill="x")
        self.secondary_button(actions, "Delete Record", self.show_delete, 22).pack(padx=18, pady=6, fill="x")
        tk.Frame(actions, bg=BORDER, height=1).pack(fill="x", padx=18, pady=16)
        tk.Label(actions, text="Database", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w", padx=18)
        tk.Label(actions, text=DB_CONFIG.get("database", ""), bg=PANEL, fg=TEXT,
                 font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=18, pady=(2, 14))

    # ---------------- VIEW ----------------
    def show_records(self):
        self.clear_content()
        self.page_title.configure(text="View Records")
        self.set_active_nav("View Records")
        self.section_header("View Records", "Browse and search records from any database table")

        toolbar = self.card(self.content)
        toolbar.pack(fill="x", pady=(0, 14))
        inner = tk.Frame(toolbar, bg=PANEL)
        inner.pack(fill="x", padx=16, pady=14)
        tk.Label(inner, text="Table", bg=PANEL, fg=MUTED, font=("Segoe UI Semibold", 9)).pack(side="left")
        combo = ttk.Combobox(inner, textvariable=self.active_table, values=list(TABLES.keys()), state="readonly", width=23)
        combo.pack(side="left", padx=(8, 20))
        self.search_var = tk.StringVar()
        search = ttk.Entry(inner, textvariable=self.search_var, width=32)
        search.pack(side="left", padx=(0, 10))
        search.insert(0, "")
        self.primary_button(inner, "Refresh", self.load_table_data, 10).pack(side="left", padx=4)
        self.secondary_button(inner, "Search", self.search_table_data, 10).pack(side="left", padx=4)
        combo.bind("<<ComboboxSelected>>", lambda e: self.load_table_data())
        search.bind("<Return>", lambda e: self.search_table_data())

        table_card = self.card(self.content)
        table_card.pack(fill="both", expand=True)
        self.table_frame = tk.Frame(table_card, bg=PANEL)
        self.table_frame.pack(fill="both", expand=True, padx=12, pady=12)
        self.record_count_label = tk.Label(table_card, text="", bg=PANEL, fg=MUTED, font=("Segoe UI", 9))
        self.record_count_label.pack(anchor="e", padx=16, pady=(0, 10))
        self.load_table_data()

    def _build_tree(self, columns, rows):
        for w in self.table_frame.winfo_children():
            w.destroy()
        yscroll = ttk.Scrollbar(self.table_frame, orient="vertical")
        xscroll = ttk.Scrollbar(self.table_frame, orient="horizontal")
        tree = ttk.Treeview(self.table_frame, columns=columns, show="headings",
                            yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        yscroll.config(command=tree.yview)
        xscroll.config(command=tree.xview)
        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            width = max(115, min(210, len(col) * 12 + 45))
            tree.column(col, width=width, anchor="center")
        for row in rows:
            tree.insert("", "end", values=row)
        tree.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

    def load_table_data(self):
        table = self.active_table.get()
        try:
            cols, rows = self.db.query(f"SELECT * FROM `{table}` ORDER BY `{PRIMARY_KEYS[table]}`", fetch=True)
            self._build_tree(cols, rows)
            self.record_count_label.configure(text=f"{len(rows)} record(s)")
        except Exception as exc:
            messagebox.showerror("Error", f"Could not load records.\n\n{exc}")

    def search_table_data(self):
        table = self.active_table.get()
        term = self.search_var.get().strip()
        if not term:
            self.load_table_data()
            return
        columns = TABLES[table]
        where = " OR ".join([f"CAST(`{c}` AS CHAR) LIKE %s" for c in columns])
        params = tuple([f"%{term}%"] * len(columns))
        try:
            cols, rows = self.db.query(f"SELECT * FROM `{table}` WHERE {where}", params, fetch=True)
            self._build_tree(cols, rows)
            self.record_count_label.configure(text=f"{len(rows)} matching record(s)")
        except Exception as exc:
            messagebox.showerror("Search Error", str(exc))

    # ---------------- INSERT ----------------
    def show_insert(self):
        self.clear_content()
        self.page_title.configure(text="Insert Record")
        self.set_active_nav("Insert Record")
        self.section_header("Insert Record", "Add a new record safely to the selected table")

        form_card = self.card(self.content)
        form_card.pack(fill="both", expand=True)

        header = tk.Frame(form_card, bg=PANEL)
        header.pack(fill="x", padx=24, pady=(22, 10))
        tk.Label(header, text="Select Table", bg=PANEL, fg=MUTED, font=("Segoe UI Semibold", 9)).pack(side="left")
        combo = ttk.Combobox(header, textvariable=self.active_table, values=list(TABLES.keys()), state="readonly", width=26)
        combo.pack(side="left", padx=12)
        combo.bind("<<ComboboxSelected>>", lambda e: self.build_insert_form())

        tk.Frame(form_card, bg=BORDER, height=1).pack(fill="x", padx=24)
        self.form_body = tk.Frame(form_card, bg=PANEL)
        self.form_body.pack(fill="both", expand=True, padx=24, pady=18)
        self.build_insert_form()

    def build_insert_form(self):
        for w in self.form_body.winfo_children():
            w.destroy()
        table = self.active_table.get()
        self.insert_entries = {}
        columns = TABLES[table]

        tk.Label(self.form_body, text=f"New {table} Record", bg=PANEL, fg=TEXT,
                 font=("Segoe UI Semibold", 14)).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 16))
        tk.Label(self.form_body, text="Dates use YYYY-MM-DD format.", bg=PANEL, fg=MUTED,
                 font=("Segoe UI", 9)).grid(row=1, column=0, columnspan=2, sticky="w", pady=(0, 12))

        for i, col in enumerate(columns, start=2):
            pretty = col.replace("_", " ").title()
            tk.Label(self.form_body, text=pretty, bg=PANEL, fg=TEXT,
                     font=("Segoe UI Semibold", 9)).grid(row=i, column=0, sticky="w", pady=7, padx=(0, 18))
            ent = ttk.Entry(self.form_body, width=46)
            ent.grid(row=i, column=1, sticky="ew", pady=7)
            self.insert_entries[col] = ent

        self.form_body.grid_columnconfigure(1, weight=1)
        button_row = tk.Frame(self.form_body, bg=PANEL)
        button_row.grid(row=len(columns) + 2, column=0, columnspan=2, sticky="w", pady=(20, 0))
        self.primary_button(button_row, "Insert Record", self.insert_record, 16).pack(side="left")
        self.secondary_button(button_row, "Clear", self.clear_insert_form, 10).pack(side="left", padx=10)

    def clear_insert_form(self):
        for ent in self.insert_entries.values():
            ent.delete(0, tk.END)

    def _validate_value(self, column, value):
        if column in DATE_COLUMNS and value:
            datetime.strptime(value, "%Y-%m-%d")
        if column in INTEGER_COLUMNS and value:
            int(value)
        if column in DECIMAL_COLUMNS and value:
            float(value)

    def insert_record(self):
        table = self.active_table.get()
        columns = TABLES[table]
        values = []
        for col in columns:
            val = self.insert_entries[col].get().strip()
            if not val:
                messagebox.showwarning("Missing Data", f"Please enter {col.replace('_', ' ')}.")
                self.insert_entries[col].focus_set()
                return
            try:
                self._validate_value(col, val)
            except ValueError:
                if col in DATE_COLUMNS:
                    hint = "Use YYYY-MM-DD."
                elif col in INTEGER_COLUMNS:
                    hint = "Enter a whole number."
                else:
                    hint = "Enter a valid number."
                messagebox.showwarning("Invalid Value", f"Invalid value for {col}. {hint}")
                return
            values.append(val)

        placeholders = ", ".join(["%s"] * len(columns))
        col_sql = ", ".join([f"`{c}`" for c in columns])
        sql = f"INSERT INTO `{table}` ({col_sql}) VALUES ({placeholders})"
        try:
            self.db.query(sql, tuple(values))
            messagebox.showinfo("Success", f"Record inserted successfully into {table}.")
            self.clear_insert_form()
        except Error as exc:
            messagebox.showerror("Insert Failed", f"Could not insert record.\n\n{exc}")

    # ---------------- DELETE ----------------
    def show_delete(self):
        self.clear_content()
        self.page_title.configure(text="Delete Record")
        self.set_active_nav("Delete Record")
        self.section_header("Delete Record", "Delete a record using its primary key")

        panel = self.card(self.content)
        panel.pack(fill="x")
        body = tk.Frame(panel, bg=PANEL)
        body.pack(fill="x", padx=28, pady=28)

        tk.Label(body, text="Table", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 9)).grid(row=0, column=0, sticky="w", pady=8)
        combo = ttk.Combobox(body, textvariable=self.active_table, values=list(TABLES.keys()), state="readonly", width=28)
        combo.grid(row=0, column=1, sticky="w", padx=(20, 0), pady=8)
        combo.bind("<<ComboboxSelected>>", lambda e: self._update_delete_label())

        self.delete_key_label = tk.Label(body, text="", bg=PANEL, fg=TEXT, font=("Segoe UI Semibold", 9))
        self.delete_key_label.grid(row=1, column=0, sticky="w", pady=8)
        self.delete_entry = ttk.Entry(body, width=31)
        self.delete_entry.grid(row=1, column=1, sticky="w", padx=(20, 0), pady=8)

        note = tk.Label(body, text="This action permanently removes the selected record from MySQL.",
                        bg=PANEL, fg=DANGER, font=("Segoe UI", 9))
        note.grid(row=2, column=0, columnspan=2, sticky="w", pady=(10, 18))
        tk.Button(body, text="Delete Record", command=self.delete_record,
                  bg=DANGER, fg="white", activebackground="#991B1B", activeforeground="white",
                  bd=0, relief="flat", padx=18, pady=10,
                  font=("Segoe UI Semibold", 9), cursor="hand2").grid(row=3, column=0, columnspan=2, sticky="w")
        self._update_delete_label()

    def _update_delete_label(self):
        table = self.active_table.get()
        key = PRIMARY_KEYS[table]
        self.delete_key_label.configure(text=key.replace("_", " ").title())
        if hasattr(self, "delete_entry"):
            self.delete_entry.delete(0, tk.END)

    def delete_record(self):
        table = self.active_table.get()
        key = PRIMARY_KEYS[table]
        value = self.delete_entry.get().strip()
        if not value:
            messagebox.showwarning("Missing ID", f"Enter the {key} to delete.")
            return
        try:
            _, rows = self.db.query(f"SELECT * FROM `{table}` WHERE `{key}`=%s", (value,), fetch=True)
            if not rows:
                messagebox.showwarning("Not Found", f"No {table} record found with {key} = {value}.")
                return
            if not messagebox.askyesno("Confirm Delete", f"Delete {table} record '{value}'?\n\nThis cannot be undone."):
                return
            affected = self.db.query(f"DELETE FROM `{table}` WHERE `{key}`=%s", (value,))
            if affected:
                messagebox.showinfo("Deleted", f"Record {value} was deleted successfully.")
                self.delete_entry.delete(0, tk.END)
            else:
                messagebox.showwarning("Not Deleted", "No record was deleted.")
        except Error as exc:
            messagebox.showerror("Delete Failed", f"Could not delete the record.\n\n{exc}")

    # ---------------- DB INFO ----------------
    def show_db_info(self):
        self.clear_content()
        self.page_title.configure(text="Database Info")
        self.set_active_nav("Database Info")
        self.section_header("Database Information", "Connection details and project table structure")

        info = self.card(self.content)
        info.pack(fill="x", pady=(0, 16))
        rows = [
            ("Host", DB_CONFIG.get("host", "")),
            ("User", DB_CONFIG.get("user", "")),
            ("Database", DB_CONFIG.get("database", "")),
            ("Tables", str(len(TABLES))),
            ("Connection", "Connected" if self.db.ensure() else "Disconnected"),
        ]
        body = tk.Frame(info, bg=PANEL)
        body.pack(fill="x", padx=24, pady=20)
        for r, (label, value) in enumerate(rows):
            tk.Label(body, text=label, bg=PANEL, fg=MUTED, font=("Segoe UI Semibold", 9), width=14, anchor="w").grid(row=r, column=0, sticky="w", pady=6)
            tk.Label(body, text=value, bg=PANEL, fg=TEXT, font=("Segoe UI", 10)).grid(row=r, column=1, sticky="w", pady=6)

        table_card = self.card(self.content)
        table_card.pack(fill="both", expand=True)
        tk.Label(table_card, text="Project Tables", bg=PANEL, fg=TEXT,
                 font=("Segoe UI Semibold", 13)).pack(anchor="w", padx=20, pady=(16, 8))
        list_frame = tk.Frame(table_card, bg=PANEL)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 18))
        for idx, table in enumerate(TABLES):
            r, c = divmod(idx, 3)
            box = tk.Frame(list_frame, bg="#F8FAFC", highlightthickness=1, highlightbackground=BORDER)
            box.grid(row=r, column=c, sticky="nsew", padx=6, pady=6)
            tk.Label(box, text=table, bg="#F8FAFC", fg=TEXT, font=("Segoe UI Semibold", 10)).pack(anchor="w", padx=12, pady=(10, 2))
            tk.Label(box, text=", ".join(TABLES[table]), bg="#F8FAFC", fg=MUTED,
                     wraplength=270, justify="left", font=("Segoe UI", 8)).pack(anchor="w", padx=12, pady=(0, 10))
        for c in range(3):
            list_frame.grid_columnconfigure(c, weight=1)

    def show_connection_help(self):
        self.clear_content()
        self.page_title.configure(text="Connection Setup")
        self.section_header("Database Connection Required", "Update DB_CONFIG in app.py and restart the application")
        panel = self.card(self.content)
        panel.pack(fill="x")
        text = (
            "1. Open app.py in VS Code.\n"
            "2. Find DB_CONFIG near the top.\n"
            "3. Enter your MySQL root password.\n"
            "4. Make sure the database name matches the schema in MySQL Workbench.\n"
            "5. Save and run: py app.py"
        )
        tk.Label(panel, text=text, bg=PANEL, fg=TEXT, justify="left",
                 font=("Segoe UI", 11), padx=24, pady=24).pack(anchor="w")

    def on_close(self):
        self.db.close()
        self.destroy()


if __name__ == "__main__":
    app = ProfessionalDBMSApp()
    app.mainloop()
