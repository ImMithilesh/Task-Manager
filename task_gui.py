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
        self.root.resizable(True, True)
        self.root.configure(bg='#f0f0f0')  # Light gray background

        # Center the window
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        style = ttk.Style()
        style.theme_use('clam')  # Modern theme

        # Configure styles
        style.configure("TLabel", font=('Arial', 10), background='#f0f0f0')
        style.configure("TButton", font=('Arial', 10, 'bold'), padding=5, relief='raised')
        style.map("TButton", background=[('active', '#e0e0e0')])

        # Custom button styles with colors
        style.configure("Blue.TButton", background='#007bff', foreground='white')
        style.map("Blue.TButton", background=[('active', '#0056b3')])

        style.configure("Green.TButton", background='#28a745', foreground='white')
        style.map("Green.TButton", background=[('active', '#1e7e34')])

        style.configure("Red.TButton", background='#dc3545', foreground='white')
        style.map("Red.TButton", background=[('active', '#bd2130')])

        style.configure("Gray.TButton", background='#6c757d', foreground='white')
        style.map("Gray.TButton", background=[('active', '#545b62')])

        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background='#007bff', foreground='white')
        style.configure("Treeview", font=('Arial', 10), rowheight=30, background='white')
        style.map("Treeview", background=[('selected', '#cce7ff')])

        # Frames for organization
        input_frame = ttk.Frame(self.root, padding=10, style='TFrame')
        input_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        button_frame = ttk.Frame(self.root, padding=10, style='TFrame')
        button_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=5)

        filter_frame = ttk.Frame(self.root, padding=10, style='TFrame')
        filter_frame.grid(row=2, column=0, sticky='ew', padx=10, pady=5)

        table_frame = ttk.Frame(self.root, padding=10, style='TFrame')
        table_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)

        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Input Fields in input_frame
        ttk.Label(input_frame, text="Title:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.title_entry = ttk.Entry(input_frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Due Date:").grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.due_date_picker = DateEntry(input_frame, width=27, background='#007bff', foreground='white', borderwidth=2)
        self.due_date_picker.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Priority:").grid(row=2, column=0, sticky='w', padx=5, pady=5)
        self.priority_var = tk.StringVar(value="Medium")
        self.priority_menu = ttk.Combobox(input_frame, textvariable=self.priority_var, values=["High", "Medium", "Low"], width=27)
        self.priority_menu.grid(row=2, column=1, padx=5, pady=5)

        # Buttons in button_frame
        ttk.Button(button_frame, text="Add Task", command=self.add_task, style='Blue.TButton').grid(row=0, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Mark Completed", command=self.mark_completed, style='Green.TButton').grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task, style='Red.TButton').grid(row=0, column=2, padx=5, pady=5)
        ttk.Button(button_frame, text="Save", command=self.save_tasks, style='Green.TButton').grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(button_frame, text="Load", command=self.load_tasks, style='Gray.TButton').grid(row=1, column=1, padx=5, pady=5)

        # Filters in filter_frame
        ttk.Label(filter_frame, text="Filter Priority:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.filter_priority = ttk.Combobox(filter_frame, values=["All", "High", "Medium", "Low"], width=10)
        self.filter_priority.set("All")
        self.filter_priority.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(filter_frame, text="Filter Status:").grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.filter_status = ttk.Combobox(filter_frame, values=["All", "Pending", "Completed"], width=10)
        self.filter_status.set("All")
        self.filter_status.grid(row=0, column=3, padx=5, pady=5)

        ttk.Button(filter_frame, text="Apply Filters", command=self.filter_tasks, style='Blue.TButton').grid(row=0, column=4, padx=5, pady=5)

        # Date Filters
        ttk.Button(filter_frame, text="Due Today", command=self.filter_today, style='Gray.TButton').grid(row=1, column=0, padx=5, pady=5)
        ttk.Button(filter_frame, text="Due This Week", command=self.filter_week, style='Gray.TButton').grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(filter_frame, text="Show All", command=self.refresh_table, style='Gray.TButton').grid(row=1, column=2, padx=5, pady=5)

        # Task Table in table_frame
        self.tree = ttk.Treeview(table_frame, columns=self.task_data.columns, show='headings')
        for col in self.task_data.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(fill='both', expand=True)

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
