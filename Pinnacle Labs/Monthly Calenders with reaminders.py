import tkinter as tk
from tkinter import messagebox, simpledialog
import calendar
from datetime import datetime

class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monthly Calendar with Reminders")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.reminders = {}  # Dictionary to store reminders

        self.create_widgets()
        self.show_calendar(self.current_year, self.current_month)

    def create_widgets(self):
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack(pady=15)

        self.prev_button = tk.Button(self.header_frame, text="<", command=self.prev_month)
        self.prev_button.grid(row=0, column=0)

        self.header_label = tk.Label(self.header_frame, text="", font=("Arial", 16))
        self.header_label.grid(row=0, column=1, padx=20)

        self.next_button = tk.Button(self.header_frame, text=">", command=self.next_month)
        self.next_button.grid(row=0, column=2)

        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

    def show_calendar(self, year, month):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        self.header_label.config(text=f"{calendar.month_name[month]} {year}")

        cal = calendar.monthcalendar(year, month)
        days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day).grid(row=0, column=i)

        for week in range(len(cal)):
            for day in range(len(cal[week])):
                day_num = cal[week][day]
                if day_num != 0:
                    btn = tk.Button(self.calendar_frame, text=str(day_num), command=lambda d=day_num: self.manage_reminder(year, month, d))
                    btn.grid(row=week+1, column=day)

    def prev_month(self):
        self.current_month -= 1
        if self.current_month == 0:
            self.current_month = 12
            self.current_year -= 1
        self.show_calendar(self.current_year, self.current_month)

    def next_month(self):
        self.current_month += 1
        if self.current_month == 13:
            self.current_month = 1
            self.current_year += 1
        self.show_calendar(self.current_year, self.current_month)

    def manage_reminder(self, year, month, day):
        date_str = f"{year}-{month:02d}-{day:02d}"
        if date_str in self.reminders:
            current_reminder = self.reminders[date_str]
        else:
            current_reminder = ""
        
        reminder = simpledialog.askstring("Set Reminder", f"Reminder for {date_str}:", initialvalue=current_reminder)
        
        if reminder is not None:
            if reminder.strip() == "":
                if date_str in self.reminders:
                    del self.reminders[date_str]
            else:
                self.reminders[date_str] = reminder

        self.show_reminders()

    def show_reminders(self):
        reminder_text = "\n".join([f"{date}: {reminder}" for date, reminder in sorted(self.reminders.items())])
        messagebox.showinfo("Reminders", reminder_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()
