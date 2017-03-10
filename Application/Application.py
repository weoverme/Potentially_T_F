"""
Application will be the main driver of all activity.
Any screen which appears will always be loaded up from this module.
"""

from GUI import GUI_class as GUI
import tkinter as tk

class Application():

    def __init__(self):
        root = tk.Tk()
        app = GUI.MainGUI(master=root)
        app.mainloop()


