import time
import win32gui
import ctypes
import threading
import tkinter as tk
from tkinter import ttk
from datetime import datetime
import csv
import tkinter.messagebox as messagebox

# Utility Functions
def get_active_window():
    try:
        window = win32gui.GetForegroundWindow()
        return win32gui.GetWindowText(window)
    except:
        return ""

def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [("cbSize", ctypes.c_uint), ("dwTime", ctypes.c_uint)]

    lii = LASTINPUTINFO()
    lii.cbSize = ctypes.sizeof(LASTINPUTINFO)
    ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lii))
    millis = ctypes.windll.kernel32.GetTickCount() - lii.dwTime
    return millis / 1000.0  # seconds

# Tracker Logic 
class ScreenTimeTracker(threading.Thread):
    def __init__(self, log_file="app_usage_log.csv", idle_threshold=60):
        super().__init__()
        self.log_file = log_file
        self.idle_threshold = idle_threshold
        self.running = False

    def run(self):
        current_window = get_active_window()
        start_time = datetime.now()
        self.running = True

        while self.running:
            time.sleep(1)
            idle_time = get_idle_duration()
            new_window = get_active_window()

            if idle_time > self.idle_threshold or new_window != current_window:
                end_time = datetime.now()
                duration = (end_time - start_time).total_seconds()

                if idle_time < self.idle_threshold and duration > 1:
                    with open(self.log_file, "a", newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([
                            current_window,
                            start_time.strftime("%Y-%m-%d %H:%M:%S"),
                            end_time.strftime("%Y-%m-%d %H:%M:%S"),
                            round(duration, 2)
                        ])
                current_window = new_window
                start_time = datetime.now()

    def stop(self):
        self.running = False

# UI 
class ScreenTimeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screen Time Tracker")
        self.root.geometry("600x400")
        self.tracker = None

        self.start_btn = tk.Button(root, text="Start Tracking", command=self.start_tracking, bg="green", fg="white")
        self.start_btn.pack(pady=10)

        self.stop_btn = tk.Button(root, text="Stop Tracking", command=self.stop_tracking, bg="red", fg="white", state="disabled")
        self.stop_btn.pack(pady=10)

        self.view_btn = tk.Button(root, text="View Log", command=self.view_log)
        self.view_btn.pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("App", "Start", "End", "Duration"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=140)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)

    def start_tracking(self):
        self.tracker = ScreenTimeTracker()
        self.tracker.start()
        self.start_btn["state"] = "disabled"
        self.stop_btn["state"] = "normal"

    import tkinter.messagebox as messagebox

    def stop_tracking(self):
        if self.tracker:
            self.tracker.stop()
            self.tracker = None
        self.start_btn["state"] = "normal"
        self.stop_btn["state"] = "disabled"

        # Calculate total screen time
        total_seconds = 0
        entries = 0
        try:
            with open("app_usage_log.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 4:
                        try:
                            duration = float(row[3])
                            total_seconds += duration
                            entries += 1
                        except:
                            continue
        except FileNotFoundError:
            pass

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = int(total_seconds % 60)

        messagebox.showinfo(
            "Tracking Summary",
            f"🟢 Total Tracked Time: {hours}h {minutes}m {seconds}s\n📄 Entries Logged: {entries}"
        )

    def view_log(self):
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open("app_usage_log.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) == 4:
                        self.tree.insert("", "end", values=row)
        except FileNotFoundError:
            pass

# Run Application
if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenTimeApp(root)
    root.mainloop()
