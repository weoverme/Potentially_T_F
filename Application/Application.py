"""
Application will be the main driver of all activity.
Any screen which appears will always be loaded up from this module.
"""

from tkinter import *
from tkinter.ttk import *
from Application.twitter_observer import TwitterObserver as TwitterObserver
from Application.all_exceptions import *


class Application(Frame):

    def __init__(self, master=NONE):
        self.master = master
        Frame.__init__(self, self.master)
        self.master.minsize(500, 600)
        self.master.maxsize(500, 700)
        self.master.title("Potentially T/F")
        self.create_widgets()
        self.observers = {}

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
        self.notebook.enable_traversal()

    def add_notebook_tab(self):
        username = self.get_username_callback()
        # Checking for twitter handle type
        if (username is not "@") and (username is not "") and (username[0] is "@"):
            # instantiate Frame
            fr = Frame(self.notebook)

            # Add frame to notebook
            self.notebook.add(fr, text=username)

            # Create new TwitterObserver for the current username

            tab_index = self.find_tab_index(username)
            self.add_twitter_observer(username, tab_index)
            print(self.observers)
        else:
            self.no_username_callback()

    def find_tab_index(self, username):
        all_tab_names = [self.notebook.tab(i, option="text") for i in self.notebook.tabs()]
        for j in range(0, len(all_tab_names)-1, 1):
            if all_tab_names[j] == username:
                return j
            else:
                pass
        print(TabNotFoundError(username).message)

    def add_twitter_observer(self, username, tab_index):
        """
        Create a Twitter Observer for the newly made notebook tab, at tab_index, into the application's
        'observer' dictionary.
        The dictionary entry is in the form of {username : TwitterObserver, tab
        :param username: twitter handle
        :param tab_index: index of tab in the notebook
        :return:
        """
        self.observers[username] = [TwitterObserver(username), tab_index]

    def no_username_callback(self):
        print("No username entered! Please enter a valid username.")

    def username_already_exists_callback(self):
        print("Username already exists! Please enter a new username.")

    def get_username_callback(self):
        val = self.username_ent.get()
        self.username_ent.delete(0, END)
        self.username_ent.insert(END, "@")
        return val

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()
