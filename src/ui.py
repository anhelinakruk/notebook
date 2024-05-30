import tkinter as tk
from tkinter import ttk, messagebox
import json
import re
import os

notes = {}
auto_tags = {"shopping", "books", "todo", "IT"}

def search_auto_tags(title):
    found_tags = []
    for auto_tag in auto_tags:
        if re.search(auto_tag, title, re.IGNORECASE):
            found_tags.append(auto_tag)
    return found_tags

def filter_notes_by_tag(tag):
    return list(filter(lambda title: tag in notes[title]['tags'], notes.keys()))

def count_notes():
    return len(notes)

def is_valid_title(title):
    return len(title) >= 3 and re.match("^[A-Za-z0-9/ ]*$", title)

def create_note_tab(notebook, title="New Note", content="", tags=None, editable=True):
    if tags is None:
        tags = []

    note_frame = ttk.Frame(notebook, padding=10)
    notebook.add(note_frame, text=title)

    title_label = ttk.Label(note_frame, text="Title:")
    title_label.grid(row=0, column=0, padx=5, pady=10, sticky="W")

    title_entry = ttk.Entry(note_frame, width=30)
    title_entry.grid(row=0, column=1, padx=5, pady=10, sticky="W")
    title_entry.insert(0, title)

    title_static = ttk.Label(note_frame, text=title, font=("TkDefaultFont", 14, "bold"))
    title_static.grid(row=0, column=1, padx=5, pady=10, sticky="W")

    content_label = ttk.Label(note_frame, text="Content:")
    content_label.grid(row=1, column=0, padx=5, pady=10, sticky="W")

    content_entry = tk.Text(note_frame, width=40, height=10)
    content_entry.grid(row=1, column=1, padx=5, pady=10, sticky="W")
    content_entry.insert(tk.END, content)

    tags_label = ttk.Label(note_frame, text="Tags:")
    tags_label.grid(row=2, column=0, padx=5, pady=10, sticky="W")

    tags_entry = ttk.Entry(note_frame, width=30)
    tags_entry.grid(row=2, column=1, padx=5, pady=10, sticky="W")
    tags_entry.insert(0, ", ".join(tags))

    tags_static = ttk.Label(note_frame, text=", ".join(tags))
    tags_static.grid(row=2, column=1, padx=5, pady=10, sticky="W")

    save_button = ttk.Button(note_frame, text="Save", style="secondary.TButton")
    save_button.grid(row=3, column=0, padx=5, pady=10, sticky="W")

    edit_button = ttk.Button(note_frame, text="Edit", style="secondary.TButton")
    edit_button.grid(row=3, column=0, padx=5, pady=10, sticky="W")
    edit_button.grid_remove()

    def save_note():
        nonlocal editable
        title = title_entry.get()
        if not is_valid_title(title):
            messagebox.showerror("Invalid Title", "Title must be at least 3 characters long and contain only letters and numbers.")
            return

        content = content_entry.get("1.0", tk.END).strip()
        tags = tags_entry.get().split(", ")

        auto_generated_tags = search_auto_tags(title)
        tags = list(filter(None, tags))

        # Remove duplicate tags
        all_tags = list(set(tags + auto_generated_tags))

        notes[title] = {"content": content, "tags": all_tags}

        with open("notes.json", "w") as f:
            json.dump(notes, f, indent=4)

        notebook.tab(notebook.select(), text=title)

        title_entry.grid_remove()
        title_static.config(text=title)
        title_static.grid(row=0, column=1, padx=10, pady=10, sticky="W")

        content_entry.config(state=tk.DISABLED)
        tags_entry.grid_remove()
        tags_static.config(text=", ".join(all_tags))
        tags_static.grid(row=2, column=1, padx=10, pady=10, sticky="W")

        save_button.grid_remove()
        edit_button.grid(row=3, column=0, padx=5, pady=10, sticky="W")

    def edit_note():
        tags_static.grid_remove()
        tags_entry.grid(row=2, column=1, padx=10, pady=10, sticky="W")

        content_entry.config(state=tk.NORMAL)
        save_button.grid(row=3, column=0, padx=5, pady=10, sticky="W")
        edit_button.grid_remove()

    save_button.config(command=save_note)
    edit_button.config(command=edit_note)

    if not editable:
        save_note()
    else:
        title_static.grid_remove()

def add_note_if_allowed(notebook):
    if count_notes() >= 5:
        messagebox.showwarning("Limit Reached", "Too many notes")
    else:
        add_note(notebook)

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
            json.dump(notes, f, indent=4)

def load_notes(notebook):
    try:
        with open("notes.json", "r") as f:
            saved_notes = json.load(f)
        for title, note in saved_notes.items():
            create_note_tab(notebook, title, note['content'], note['tags'], editable=False)
    except FileNotFoundError:
        pass

def search_notes(query):
    results = [title for title, note in notes.items() if query.lower() in title.lower() or query.lower() in note['content'].lower()]
    return results

def export_notes_by_tag(tag):
    filtered_notes = filter_notes_by_tag(tag)
    if not filtered_notes:
        messagebox.showinfo("Export Notes", f"No notes found with tag: {tag}")
        return

    export_dir = os.path.join(os.getcwd(), 'exported_notes', tag)
    os.makedirs(export_dir, exist_ok=True)

    for note_title in filtered_notes:
        note_content = notes[note_title]['content']
        file_path = os.path.join(export_dir, f"{note_title}.txt")
        with open(file_path, 'w') as file:
            file.write(note_content)
    
    messagebox.showinfo("Export Notes", f"Exported {len(filtered_notes)} notes to {export_dir}")
