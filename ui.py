import tkinter as tk
from tkinter import ttk, messagebox
import json
from notes import notes

def create_note_tab(notebook, title="New Note", content="", editable=True):
    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text=title)

    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=10, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=40)
    title_entry.grid(row=0, column=1, padx=10, pady=10)
    title_entry.insert(0, title)

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=10, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=10, pady=10)
    content_entry.insert(tk.END, content)

    save_button = ttk.Button(note_frame, text="Save", style="secondary.TButton")
    save_button.grid(row=2, column=1, padx=10, pady=10)

    edit_button = ttk.Button(note_frame, text="Edit", style="secondary.TButton")
    edit_button.grid(row=2, column=1, padx=10, pady=10)
    edit_button.grid_remove()

    def save_note():
        nonlocal editable
        title = title_entry.get()
        content = content_entry.get("1.0", tk.END).strip()

        notes[title] = content

        with open("notes.json", "w") as f:
            json.dump(notes, f)

        notebook.tab(notebook.select(), text=title)

        title_entry.grid_remove()
        title_static = ttk.Label(note_frame, text=title, font=("TkDefaultFont", 14, "bold"))
        title_static.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        content_entry.config(state=tk.DISABLED)
        save_button.grid_remove()
        edit_button.grid()

    def edit_note():
        title_static = note_frame.grid_slaves(row=0, column=1)[0]
        title_static.grid_remove()
        title_entry.grid()
        content_entry.config(state=tk.NORMAL)
        save_button.grid()
        edit_button.grid_remove()

    save_button.config(command=save_note)
    edit_button.config(command=edit_note)

    if not editable:
        save_note()

def add_note(notebook):
    create_note_tab(notebook)

def delete_note(notebook):
    current_tab = notebook.index(notebook.select())
    note_title = notebook.tab(current_tab, "text")

    confirm = messagebox.askyesno("Delete Note", f"Are you sure you want to delete {note_title}?")
    if confirm:
        notebook.forget(current_tab)
        notes.pop(note_title, None)

        with open("notes.json", "w") as f:
            json.dump(notes, f)

def load_notes(notebook):
    try:
        with open("notes.json", "r") as f:
            saved_notes = json.load(f)
        for title, content in saved_notes.items():
            create_note_tab(notebook, title, content, editable=False)
    except FileNotFoundError:
        pass
