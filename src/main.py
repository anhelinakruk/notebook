import tkinter as tk
from tkinter import Menu, ttk, simpledialog, messagebox
from ui import  delete_note, load_notes, filter_notes_by_tag, search_notes, add_note_if_allowed
from file_ops import open_file, save_file

root = tk.Tk()
root.title("Notes App")
root.geometry("500x450")

style = ttk.Style()
style.configure("TNotebook.Tab", font=("TkDefaultFont", 14, "bold"))

notebook = ttk.Notebook(root, style="TNotebook")
notebook.pack(padx=10, pady=0, fill=tk.BOTH, expand=True)

load_notes(notebook)

button_frame = ttk.Frame(root)
button_frame.pack(fill=tk.X, padx=0, pady=10)

new_button = ttk.Button(button_frame, text="New Note", command=lambda: add_note_if_allowed(notebook))
new_button.pack(side=tk.LEFT, padx=10, pady=0)

delete_button = ttk.Button(button_frame, text="Delete", command=lambda: delete_note(notebook))
delete_button.pack(side=tk.LEFT, padx=5, pady=0)

filter_button = ttk.Button(button_frame, text="Filter by Tag", command=lambda: filter_by_tag())
filter_button.pack(side=tk.LEFT, padx=5, pady=0)

search_button = ttk.Button(button_frame, text="Search Notes", command=lambda: search_for_notes())
search_button.pack(side=tk.LEFT, padx=5, pady=0)

main_menu = Menu(root)
root.config(menu=main_menu)

file_menu = Menu(main_menu, tearoff=0)
main_menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=lambda: open_file(notebook))
file_menu.add_command(label='Save', command=lambda: save_file(notebook))

def filter_by_tag():
    tag = simpledialog.askstring("Filter Notes", "Enter tag to filter by:")
    if tag:
        filtered_notes = filter_notes_by_tag(tag)
        messagebox.showinfo("Filtered Notes", "\n".join(filtered_notes))

def search_for_notes():
    query = simpledialog.askstring("Search Notes", "Enter search query:")
    if query:
        results = search_notes(query)
        messagebox.showinfo("Search Results", "\n".join(results))

root.mainloop()
