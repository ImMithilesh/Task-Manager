from plyer import notification
from datetime import datetime

class TaskNotifications:
    def __init__(self, task_data, root):
        self.task_data = task_data
        self.root = root

    def check_notifications(self):
        due_today = self.task_data.get_due_today_tasks()
        overdue = self.task_data.get_overdue_tasks()

        if due_today:
            notification.notify(title="Tasks Due Today", message="\n".join(due_today), timeout=10)

        if overdue:
            notification.notify(title="Overdue Tasks", message="\n".join(overdue), timeout=10)

    def schedule_notifications(self):
        self.check_notifications()
        self.root.after(600000, self.schedule_notifications)  # every 10 minutes
