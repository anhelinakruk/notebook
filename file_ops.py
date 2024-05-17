from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from ui import create_note_tab

def save_file(notebook):
    ask_save = asksaveasfilename(defaultextension=".txt",
                                 filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if ask_save:
        current_tab = notebook.select()
        text_widget = notebook.nametowidget(current_tab).winfo_children()[3]  # Get the content Text widget
        content = text_widget.get("1.0", tk.END)
        with open(ask_save, "w") as f:
            f.write(content)

def open_file(notebook):
    ask_open = askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if ask_open:
        with open(ask_open, 'r') as f:
            content = f.read()
            create_note_tab(notebook, "Opened Note", content)
