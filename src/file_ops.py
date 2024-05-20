from tkinter.filedialog import askopenfilename, asksaveasfilename
import tkinter as tk
from ui import create_note_tab

def save_file(notebook):
    file_path = asksaveasfilename(defaultextension=".txt",
                                  filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if not file_path:
        return

    current_tab = notebook.nametowidget(notebook.select())
    text_widget = next((child for child in current_tab.winfo_children() if isinstance(child, tk.Text)), None)
    if text_widget:
        with open(file_path, "w") as file:
            file.write(text_widget.get("1.0", tk.END))

def open_file(notebook):
    ask_open = askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if ask_open:
        with open(ask_open, 'r') as f:
            content = f.read()
            create_note_tab(notebook, "Opened Note", content)
