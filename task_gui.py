import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class TaskGUI:
    def __init__(self, root, task_data):
        self.root = root
        self.task_data = task_data
        self.setup_gui()

    def setup_gui(self):
        self.root.title("Task Manager")
        self.root.geometry("1920x1080")

        style = ttk.Style()
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
        style.configure("Treeview", font=('Arial', 10), rowheight=25)

        # Input Fields
        tk.Label(self.root, text="Title").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = tk.Entry(self.root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Due Date").grid(row=2, column=0, padx=5, pady=5)
        self.due_date_picker = DateEntry(self.root, width=27, background='darkblue', foreground='white', borderwidth=2)
        self.due_date_picker.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Priority").grid(row=4, column=0, padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(self.root, textvariable=self.priority_var, values=["High", "Medium", "Low"], width=27)
        self.priority_menu.grid(row=4, column=1, padx=5, pady=5)

        # Buttons
        tk.Button(self.root, text="Add Task", command=self.add_task).grid(row=6, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Mark Completed", command=self.mark_completed).grid(row=6, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Delete Task", command=self.delete_task).grid(row=6, column=2, padx=5, pady=5)
        tk.Button(self.root, text="Save", command=self.save_tasks).grid(row=8, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Load", command=self.load_tasks).grid(row=8, column=1, padx=5, pady=5)

        # Filters
        tk.Label(self.root, text="Filter Priority").grid(row=10, column=0, padx=5, pady=5)
        self.filter_priority = ttk.Combobox(self.root, values=["All", "High", "Medium", "Low"], width=10)
        self.filter_priority.set("All")
        self.filter_priority.grid(row=10, column=1, padx=5, pady=5)

        tk.Label(self.root, text="Filter Status").grid(row=10, column=2, padx=5, pady=5)
        self.filter_status = ttk.Combobox(self.root, values=["All", "Pending", "Completed"], width=10)
        self.filter_status.set("All")
        self.filter_status.grid(row=10, column=3, padx=5, pady=5)

        tk.Button(self.root, text="Apply Filters", command=self.filter_tasks).grid(row=10, column=4, padx=5, pady=5)

        # Date Filters
        tk.Button(self.root, text="Due Today", command=self.filter_today).grid(row=12, column=0, padx=5, pady=5)
        tk.Button(self.root, text="Due This Week", command=self.filter_week).grid(row=12, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Show All", command=self.refresh_table).grid(row=12, column=2, padx=5, pady=5)

        # Task Table
        self.tree = ttk.Treeview(self.root, columns=self.task_data.columns, show='headings')
        for col in self.task_data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.grid(row=14, column=0, columnspan=5, padx=10, pady=10)

        self.refresh_table()

    def add_task(self):
        title = self.title_entry.get()
        due_date = self.due_date_picker.get_date().strftime('%Y-%m-%d')
        priority = self.priority_var.get()
        if not title:
            messagebox.showwarning("Missing Info", "Please enter a task title.")
            return
        self.task_data.add_task(title, due_date, priority)
        self.refresh_table()

    def refresh_table(self, filtered_df=None):
        self.tree.delete(*self.tree.get_children())
        df = filtered_df if filtered_df is not None else self.task_data.tasks_df
        today = datetime.today().date()

        for index, row in df.iterrows():
            due = datetime.strptime(row['Due Date'], '%Y-%m-%d').date()
            tag = 'overdue' if due < today and row['Status'] != 'Completed' else ''
            self.tree.insert('', 'end', iid=index, values=list(row), tags=(tag,))
        self.tree.tag_configure('overdue', background='lightcoral')

    def save_tasks(self):
        self.task_data.save_tasks()
        messagebox.showinfo("Saved", "Tasks saved to tasks.csv")

    def load_tasks(self):
        self.task_data.load_tasks()
        self.refresh_table()

    def mark_completed(self):
        selected = self.tree.selection()
        if selected:
            self.task_data.mark_completed(selected)
            self.refresh_table()

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            self.task_data.delete_task(selected)
            self.refresh_table()

    def filter_tasks(self):
        priority = self.filter_priority.get()
        status = self.filter_status.get()
        df = self.task_data.filter_tasks(priority, status)
        self.refresh_table(df)

    def filter_today(self):
        df = self.task_data.filter_today()
        self.refresh_table(df)

    def filter_week(self):
        df = self.task_data.filter_week()
        self.refresh_table(df)
