import tkinter as tk
from tkinter import Menu, ttk
from ui import create_note_tab, add_note, delete_note, load_notes
from file_ops import open_file, save_file

# Create the main window
root = tk.Tk()
root.title("Notes App")
root.geometry("500x500")

# Configure the tab font to be bold
style = ttk.Style()
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

# Create the notebook to hold the notes
notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Load saved notes
load_notes(notebook)

# Add buttons to the main window
new_button = ttk.Button(root, text="New Note", command=lambda: add_note(notebook), style="info.TButton")
new_button.pack(side=tk.LEFT, padx=10, pady=10)

delete_button = ttk.Button(root, text="Delete", command=lambda: delete_note(notebook), style="primary.TButton")
delete_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create the menu
main_menu = Menu(root)
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=lambda: open_file(notebook))
file_menu.add_command(label='Save', command=lambda: save_file(notebook))

root.mainloop()
