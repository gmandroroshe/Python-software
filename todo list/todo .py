import tkinter as tk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
import time

def add_task():
    task = task_entry.get()
    if task:
        time = simpledialog.askstring("Set Time", "Enter the time (HH:MM) for the task (optional):")
        if time:
            try:
                # Validate the time format
                datetime.strptime(time, "%H:%M")
                task_with_time = f"{task} - {time}"
                listbox.insert(tk.END, task_with_time)
                task_times[task_with_time] = time
            except ValueError:
                messagebox.showwarning("Warning", "Invalid time format. Please use HH:MM format.")
        else:
            listbox.insert(tk.END, task)
        task_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Warning", "Please enter a task.")

def remove_task():
    try:
        selected_index = listbox.curselection()[0]
        task_with_time = listbox.get(selected_index)
        listbox.delete(selected_index)
        if task_with_time in task_times:
            del task_times[task_with_time]
    except IndexError:
        messagebox.showwarning("Warning", "Please select a task to remove.")

def update_time():
    current_time = datetime.now().strftime("%H:%M")
    task_keys = list(task_times.keys())  # Create a copy of the dictionary keys
    for task_with_time in task_keys:
        task, time = task_with_time.split(" - ")
        current_task_time = datetime.strptime(time, "%H:%M")
        remaining_time = current_task_time - datetime.strptime(current_time, "%H:%M")
        if remaining_time.total_seconds() <= 0:
            messagebox.showinfo("Notification", f"Time's up for task: {task}")
            listbox.delete(tk.ANCHOR)
            del task_times[task_with_time]
        else:
            new_time = (datetime.min + remaining_time).time()
            task_with_time = f"{task} - {new_time.strftime('%H:%M')}"
            listbox.delete(0, tk.END)
            listbox.insert(tk.END, task_with_time)
            task_times[task_with_time] = time
    root.after(1000, update_time)


# Create the main application window
root = tk.Tk()
root.title("To-Do List")

# Create a frame for input and buttons
input_frame = tk.Frame(root)
input_frame.pack(pady=10)

# Create an entry field for task input
task_entry = tk.Entry(input_frame, width=35)
task_entry.pack(side=tk.LEFT, padx=(0, 5))

# Create a button to add tasks
add_button = tk.Button(input_frame, text="Add Task", width=10, command=add_task)
add_button.pack(side=tk.LEFT, padx=(0, 5))

# Create a button to remove tasks
remove_button = tk.Button(input_frame, text="Remove Task", width=10, command=remove_task)
remove_button.pack(side=tk.LEFT, padx=(0, 5))

# Create a frame for the to-do list
list_frame = tk.Frame(root)
list_frame.pack(padx=10, pady=5)

# Create a listbox to display tasks
listbox = tk.Listbox(list_frame, width=50, height=15)
listbox.pack(side=tk.LEFT, fill=tk.BOTH)

# Create a scrollbar for the listbox
scrollbar = tk.Scrollbar(list_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.BOTH)

# Connect the listbox to the scrollbar
listbox.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

# Dictionary to store task names and their corresponding times
task_times = {}

# Schedule the update_time function to run periodically
root.after(1000, update_time)

# Run the main event loop
root.mainloop()
