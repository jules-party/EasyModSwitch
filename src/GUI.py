import tkinter
import customtkinter as ct
import ModSwitch as ms
import time

# ModSwitch Initializing
fman = ms.file_management()
fman.set_mods_folder()
folder_paths = ms.folder_paths
folder_names = ms.folder_names

# GUI Initializing
ct.set_appearance_mode(ms.data.get('appearance_mode'))
ct.set_default_color_theme(ms.data.get('color_theme'))

app = ct.CTk()
app.geometry("240x400")

def set_folder(choice):
    global folder_name
    folder_name = choice
    status_text.configure(text="Set choice to "+choice)

def submit():
    try:
        index: int = folder_names.index(folder_name)
    except NameError:
        index: int = folder_names.index(folder_names[0])

    status_text.configure(text="Copying files...")
    fman.copy_mod_files(index+1)
    status_text.configure(text="Done!")

sub_button = ct.CTkButton(master=app,
                          text="Submit",
                          command=submit)


combobox = ct.CTkComboBox(master=app,
                          state="readonly",
                          values=folder_names,
                          command=set_folder)

status_text = ct.CTkLabel(master=app,
                          text="Download Status")

sub_button.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)
#combobox.pack(pady=185, anchor=tkinter.CENTER)
combobox.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
combobox.set(folder_names[0])
status_text.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

app.mainloop()
