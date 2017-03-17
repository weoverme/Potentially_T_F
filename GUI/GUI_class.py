"""
GUI Code for Potentially T/F

Extensions will be made from this module, into other more specific and detailed GUI modules.

Author: Ray Cho
Date: 4 March 2017

"""

import tkinter as tk
from Application import twitter_observer as twO


class MainGUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title("Potentially T/F")
        self.master.minsize(500, 700)
        self.master.maxsize(800, 800)
        self.title_label()

    def title_label(self):
        self.title = tk.Label(self)
        self.title["text"] = "Potentially T/F"
        self.title["command"] = None
        self.title.pack(side="top")


class InitialGUI(MainGUI):
    def __init__(self):
        MainGUI.__init__(self, master=None)
        self.twitter_observer = None
        self.get_tweets_button()
        self.credits_widget()

    def get_tweets_button(self):
        self.get_tweets = tk.Button(self)
        self.get_tweets["text"] = "Get Tweets!"
        self.get_tweets["command"] = self.get_tweets_from()#get_credentials()
        self.get_tweets.pack(side="bottom")

    def credits_widget(self):
        self.credits = tk.Label(self)
        self.credits["text"] = "Credits to Young Rae Cho, Monash University Computer Science Project for Semester 1 2017"
        self.credits.pack(side="bottom")



class DefaultGUI(MainGUI):

    def __init__(self):
        MainGUI.__init__(self, master=None)


