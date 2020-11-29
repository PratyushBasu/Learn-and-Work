
import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

text_contents = dict()


def check_for_changes():
    current = get_text_widget()
    content = current.get("1.0", "end-1c")
    name = notebook.tab("current")["text"]

    if hash(content) != text_contents[str(current)]:
        if name[-1] != "*":
            notebook.tab("current", text=name + "*")
    elif name[-1] == "*":
        notebook.tab("current", text=name[:-1])


def get_text_widget():
    tab_widget = notebook.nametowidget(notebook.select())              # tab name
    text_widget = tab_widget.winfo_children()[0]                       # gets the text_area children of notebook 
    return text_widget


def get_current_tab():
    current_tab = notebook.select()
    return current_tab


def close_current_tab():
    # It seemed to me, that the problem emerges, because we are trying to close a tab from 
    # the notebook while giving (with the get_text_widget( )) a subset of the tab to the 
    # forget method (which needs a tab ID) -> root - notebook - container (Frame) - text_area and Scrollbar
    # Because the Container(Frame) is the actual tab, it needs to be selected to get closed.
    
    # current = get_text_widget()
    current = get_current_tab()
    if current_tab_unsaved() and not confirm_close():
        return

    if len(notebook.tabs()) == 1:
        create_file()
    notebook.forget(current)


def current_tab_unsaved():
    text_widget = get_text_widget()
    content = text_widget.get("1.0", "end-1c")
    return hash(content) != text_contents[str(text_widget)]


def confirm_close():
    return messagebox.askyesnocancel(
            message="You have unsaved changes. Are you sure you want to close?",
            icon="question",
            title="Unsaved Changes"
        )


def confirm_quit():
    unsaved = False

    for tab in notebook.tabs():
        tab_widget = notebook.nametowidget(tab)
        text_widget = tab_widget.winfo_children()[0]
        content = text_widget.get("1.0", "end-1c")

        if hash(content) != text_contents[str(text_widget)]:
            unsaved = True
            break

    if unsaved and not confirm_close():
            return

    root.destroy()


def create_file(content="", title="Untitled"):
    container = ttk.Frame(notebook)
    container.pack()

    text_area = tk.Text(container)
    text_area.insert("end", content)
    text_area.pack(side="left", fill="both", expand=True)

    notebook.add(container, text=title)
    notebook.select(container)

    text_contents[str(text_area)] = hash(content)               # hash of the contents
    #https://blog.tecladocode.com/tkinter-scrollable-frames/
    text_scroll = ttk.Scrollbar(container, orient="vertical", command=text_area.yview)
    text_scroll.pack(side="right", fill="y")
    text_area["yscrollcommand"] = text_scroll.set


def open_file():
    file_path = filedialog.askopenfilename()

    try:
        filename = os.path.basename(file_path)

        with open(file_path) as file:
            content = file.read().strip()

    except (AttributeError, FileNotFoundError):
        print("Open operation cancelled")
        return

    create_file(content, filename)


def save_file():
    file_path = filedialog.asksaveasfilename()

    try:
        filename = os.path.basename(file_path)
        text_widget = get_text_widget()
        content = text_widget.get("1.0", "end - 1c")        # start = 1st line, before first char to end = end_of_content - 1 char (last char is newline, hence omitting)

        with open(file_path, "w") as file:
            file.write(content)

    except (AttributeError, FileNotFoundError, FileExistsError):
        print("Save operation cancelled")
        return 

    notebook.tab("current", text = filename)                # tab_id = current (current tab); tab/file name will be replaced with filename
    tex_contents[str(text_widget)] = hash(content)          # hash of the contents


def show_about_info():
    messagebox.showinfo(
        title="About",
        message="Pratyush's Text Editor is a simple tab enabled text editor to learn about Tkinter"
    )


root = tk.Tk()
root.title("Pratyush's Text Editor")
root.option_add("*tearOff", False)                #  change the behavior of certain elements in different OS. Read Docs

main = ttk.Frame(root)
main.pack(fill="both", expand=True, padx=(1), pady=(4, 0))

menubar = tk.Menu(root)
root.config(menu=menubar)

file_menu = tk.Menu(menubar)
help_menu = tk.Menu(menubar)

menubar.add_cascade(menu=file_menu, label="File")
menubar.add_cascade(menu=help_menu, label="Help")

# Command / functions
file_menu.add_command(label="New", command=create_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open...", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Close Tab", command=close_current_tab, accelerator="Ctrl+W")
file_menu.add_command(label="Exit", command=confirm_quit)

help_menu.add_command(label="About", command=show_about_info)

notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

create_file()
# create_file()
# create_file()       # last one will be active for inputting texts when multiple function calls are done

# bind the shortcuts / special key presses as long as those are active the tkinter window
# https://stackoverflow.com/questions/16082243/how-to-bind-ctrl-in-python-tkinter

root.bind("<KeyPress>", lambda event: check_for_changes())
root.bind("<Control-n>", lambda event: create_file())
root.bind("<Control-o>", lambda event: open_file())
root.bind("<Control-s>", lambda event: save_file())
root.bind("<Control-w>", lambda event: close_current_tab())

root.mainloop()
