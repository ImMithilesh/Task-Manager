import pandas as pd
from datetime import datetime, timedelta

class TaskData:
    def __init__(self):
        self.columns = ['Title', 'Due Date', 'Priority', 'Status']
        self.tasks_df = pd.DataFrame(columns=self.columns)

    def add_task(self, title, due_date, priority):
        new_task = pd.DataFrame([[title, due_date, priority, 'Pending']], columns=self.columns)
        self.tasks_df = pd.concat([self.tasks_df, new_task], ignore_index=True)

    def save_tasks(self, filepath='tasks.csv'):
        self.tasks_df.to_csv(filepath, index=False)

    def load_tasks(self, filepath='tasks.csv'):
        try:
            self.tasks_df = pd.read_csv(filepath)
        except FileNotFoundError:
            pass  # Start with empty if file doesn't exist

    def mark_completed(self, indices):
        for i in indices:
            self.tasks_df.at[int(i), 'Status'] = 'Completed'

    def delete_task(self, indices):
        self.tasks_df = self.tasks_df.drop([int(i) for i in indices]).reset_index(drop=True)

    def filter_tasks(self, priority=None, status=None):
        df = self.tasks_df.copy()
        if priority and priority != "All":
            df = df[df['Priority'] == priority]
        if status and status != "All":
            df = df[df['Status'] == status]
        return df

    def filter_today(self):
        today = datetime.today().date().strftime('%Y-%m-%d')
        return self.tasks_df[self.tasks_df['Due Date'] == today]

    def filter_week(self):
        today = datetime.today().date()
        end_week = today + timedelta(days=7)
        df = self.tasks_df.copy()
        df['Due Date'] = pd.to_datetime(df['Due Date']).dt.date
        return df[(df['Due Date'] >= today) & (df['Due Date'] <= end_week)]

    def get_overdue_tasks(self):
        today = datetime.today().date()
        overdue = []
        for _, row in self.tasks_df.iterrows():
            due_date = datetime.strptime(row['Due Date'], '%Y-%m-%d').date()
            if row['Status'] != 'Completed' and due_date < today:
                overdue.append(row['Title'])
        return overdue

    def get_due_today_tasks(self):
        today = datetime.today().date()
        due_today = []
        for _, row in self.tasks_df.iterrows():
            due_date = datetime.strptime(row['Due Date'], '%Y-%m-%d').date()
            if row['Status'] != 'Completed' and due_date == today:
                due_today.append(row['Title'])
        return due_today
