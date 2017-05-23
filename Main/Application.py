"""
Application will be the main driver of all activity.
Any screen which appears will always be loaded up from this module.
"""

from tkinter import *
from tkinter.ttk import *
from Main.twitterWrapper import TwitterWrapper
from Main.myClassifier import MyClassifier as myclf

class Application(Frame):

    def __init__(self, master=NONE):
        self.master = master
        Frame.__init__(self, self.master)
        self.master.minsize(500, 600)
        self.master.maxsize(500, 700)
        self.master.title("Potentially T/F")
        self.create_widgets()

        # concerned with managing the back end
        self.tw_holder = {}



######################################
    def create_widgets(self):
        self.create_main_frame()
        self.create_add_user_frame()
        self.create_notebook_frame()

    def create_main_frame(self):
        self.main_frame = Frame(self.master)
        self.main_frame.pack()

    def create_add_user_frame(self):
        self.add_user_frame = Frame(self.main_frame)
        self.add_user_frame.pack()
        self.username_label = Label(self.add_user_frame)
        self.username_label["text"] = "Enter a Twitter Handle Here:"
        self.username_label.pack(side='left', fill='x')

        self.username_ent = Entry(self.add_user_frame)
        self.username_ent.insert(0, "@")
        self.username_ent.pack(side='left', expand='YES', fill='x')
        get_username_button = Button(self.add_user_frame, text="Add!", command=self.add_notebook_tab)
        get_username_button.pack(side='left')

    def create_notebook_frame(self):
        self.notebook = Notebook(self.main_frame)
        self.notebook.pack()

    def add_notebook_tab(self):
        username = self.get_username_callback()
        #    frame_dic[username] = Frame(notebook)
        self.notebook.add(Frame(self.notebook), text=username)

        # create a TwitterWrapper for this username
        self.tw_holder[username] = TwitterWrapper(username, 20)

        # For each tweet saved by the twitter wrapper,
        # create a button which gives the user the options to verify
        # or to say that it is in fact verifiable or not


###############
    def get_username_callback(self):
        val = self.username_ent.get()
        self.username_ent.delete(0, END)
        self.username_ent.insert(END, "@")
        return val


if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()

