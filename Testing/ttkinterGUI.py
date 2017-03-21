from tkinter import *
from tkinter.ttk import *


# All functions
def add_notebook_tab(frame_dic, username, notebook):
    frame_dic[username] = Frame(notebook)
    notebook.add(frame_dic[username], text=username)

# Root
root = Tk()
root.minsize(500, 600)
root.maxsize(500, 700)
root.title("Potentially T/F")

#   Main Frame
main_frame = Frame(root)
main_frame.pack(expand='YES', fill='both')

#        Notebook
notebook = Notebook(main_frame)
notebook.pack(expand='yes', fill='both')

notebook_frames = {}
add_notebook_tab(notebook_frames, "@BarackObama", notebook)
add_notebook_tab(notebook_frames, "@realDonaldTrump", notebook)
notebook.pack()



root.mainloop()