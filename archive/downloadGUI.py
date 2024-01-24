import tkinter as tk
from tkinter import ttk

def submit_button_clicked():
    pass

def download_button_clicked():
    pass

# Create main window
root = tk.Tk()
root.title("Search and Retrieve Application")

# Text entry box and Submit button in the same row
entry_label = tk.Label(root, text="Type artist name")
entry_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)

entry = tk.Entry(root)
entry.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

submit_button = tk.Button(root, text="Submit", command=submit_button_clicked)
submit_button.grid(row=0, column=2, pady=10, padx=10, sticky=tk.W)

# Listbox with scrollbar
results_listbox = tk.Listbox(root, selectmode=tk.SINGLE)
results_listbox.insert(0, "Result 1")
results_listbox.insert(1, "Result 2")
results_listbox.insert(2, "Result 3")
results_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W+tk.E)

scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=results_listbox.yview)
scrollbar.grid(row=1, column=2, pady=10, padx=10, sticky=tk.W+tk.N+tk.S)
results_listbox.config(yscrollcommand=scrollbar.set)

# Download button
download_button = tk.Button(root, text="Download", command=download_button_clicked)
download_button.grid(row=2, column=0, columnspan=3, pady=10, padx=10)

# Run the application
root.mainloop()
