"""
GUI Code for Potentially T/F

Extensions will be made from this module, into other more specific and detailed GUI modules.

Author: Ray Cho
Date: 4 March 2017

"""

import tkinter as tk

class MainGUI(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title("Potentially T/F")
        self.master.minsize(500, 700)
        self.master.maxsize(800, 800)
        self.title_label()
        self.tweetOb =

    def make_title_label(self):
        self.title = tk.Label(self)
        self.title["text"] = "Potentially T/F"
        self.title["command"] = None
        self.title.pack(side="top")

    def make_get_tweets_button(self):
        self.get_tweets = tk.Button(self)
        self.get_tweets["text"] = "Get Tweets!"
        self.get_tweets["command"] =



a = MainGUI()