import tkinter as tk
from task_data import TaskData
from task_gui import TaskGUI
from task_notifications import TaskNotifications

def main():
    root = tk.Tk()
    task_data = TaskData()
    gui = TaskGUI(root, task_data)
    notifications = TaskNotifications(task_data, root)
    notifications.schedule_notifications()
    root.mainloop()

if __name__ == "__main__":
    main()
