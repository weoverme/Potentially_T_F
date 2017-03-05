"""
GUI Code for Potentially T/F

Author: Ray Cho
Date: 4 March 2017

"""

import tkinter as tk


class Application(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.master.title("Potentially T/F")
        self.master.minsize(500, 700)
        self.master.maxsize(800, 800)
        self.create_widgets()

root = tk.Tk()
app = Application(master=root)
app.mainloop()