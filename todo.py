import tkinter as tk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        
        self.task_list = []

        # Add Task Entry
        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=10)

        # Add Buttons
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack(pady=5)

        self.delete_button = tk.Button(root, text="Delete Selected", command=self.delete_task)
        self.delete_button.pack(pady=5)

        # Display Tasks
        self.listbox = tk.Listbox(root, width=50, height=15, selectmode=tk.SINGLE)
        self.listbox.pack(pady=10)

    def add_task(self):
        task = self.entry.get().strip()
        if task:
            self.task_list.append(task)
            self.update_listbox()
            self.entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task cannot be empty!")

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            task_index = selected[0]
            self.task_list.pop(task_index)
            self.update_listbox()
        else:
            messagebox.showwarning("Warning", "No task selected!")

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        for task in self.task_list:
            self.listbox.insert(tk.END, task)

# Create the main window
if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
