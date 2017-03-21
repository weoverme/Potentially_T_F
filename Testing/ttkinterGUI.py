from tkinter import *
from tkinter.ttk import *


# All functions
def add_notebook_tab():
    username = get_username_callback()
#    frame_dic[username] = Frame(notebook)
    notebook.add(Frame(notebook), text=username)


def get_username_callback():
    val = username_ent.get()
    username_ent.delete(0, END)
    username_ent.insert(END, "@")
    return val

# Root
root = Tk()
root.minsize(500, 600)
root.maxsize(500, 700)
root.title("Potentially T/F")

#   Main Frame
main_frame = Frame(root)
main_frame.pack(expand='YES', fill='both')


# 'Add User' Section
add_user_frame = Frame(main_frame)
add_user_frame.pack()
username_label = Label(add_user_frame)
username_label["text"] = "Enter a Twitter Handle Here:"
username_label.pack(side='left', fill='x')

username_ent = Entry(add_user_frame)
username_ent.insert(0, "@")
username_ent.pack(side='left', expand='YES', fill='x')
get_username_button = Button(add_user_frame, text="Add!", command=add_notebook_tab)
get_username_button.pack(side='left')

#        Notebook
notebook = Notebook(main_frame)
notebook.pack(expand='yes', fill='both')

notebook_frames = {}
notebook.pack()


root.mainloop()


