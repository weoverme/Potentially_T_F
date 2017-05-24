"""
Application will be the main driver of all activity.
Any screen which appears will always be loaded up from this module.
"""

from tkinter import *
from tkinter.ttk import *

from Main.twitterWrapper import TwitterWrapper
from Main.myClassifier import MyClassifier

class Application(Frame):

    def __init__(self, master=None):

        self.master = master
        Frame.__init__(self, self.master)
        self.master.minsize(600, 600)
        self.master.maxsize(700, 700)
        self.master.title("Potentially T/F")
        self.create_widgets()

        # concerned with managing the back end
        self.tab_holder = {}
        self.clf = MyClassifier(load_clf=True)


    def create_widgets(self):
        self.create_main_frame()
        self.create_add_user_frame()
        self.create_notebook_frame()
        self.create_description_frame()

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
        self.notebook = Notebook(self.main_frame, width=580, height=350, padding=5)
        self.notebook.pack()

    def add_notebook_tab(self):
        username = self.get_username_callback()
        """
        self.tab_holder[username] = []


        # create a TwitterWrapper for this username
        self.tab_holder[username].append(TwitterWrapper(username, 20))

        # For each tweet saved by the twitter wrapper,
        # create a Box which gives the user the options to verify
        # or to say that it is in fact verifiable or not
        tw = self.tab_holder[username][0] # access the TwitterWrapper object

        all_tw_ids = sorted(tw.all_tweets, reverse=True) # all tweet_ids


        tweet_frames = []
        for tw_id in all_tw_ids:
            tw_text = tw.all_tweets[tw_id]
            tw_frame = Frame(tab_frame, borderwidth=1, width=460, height=100)
            tw_frame.pack(fill='x', side='left', padx=2, pady=1)

            # text part of the frame
            tw_frame_text = Label(tw_frame)
#            tw_frame_text['text'] = tw_text

            try:
                tw_frame_text['text'] = tw_text
                tw_frame_text.pack(side='left', fill='x')
                input("Press enter")
            except TclError:
                print(tw_text)







            tweet_frames.append(tw_frame)


        self.tab_holder[username].append(tweet_frames)
        """

        # cannot have a tab with empty username
        if username != "@":

            tab_frame = Frame(self.notebook)

            self.tab_holder[username] = TwitterWrapper(username, 20)
            self.notebook.add(tab_frame, text=username)

            tweet_listbox = Listbox(tab_frame, width=100, height=22, selectmode=SINGLE) # width=X-chars, height=Y-lines
            #tweet_listbox.pack()
            self.add_tweets_to_listbox(username, tweet_listbox)
            tweet_listbox.pack()

    def add_tweets_to_listbox(self, username, listbox):
        user_tweet_ids = sorted(self.tab_holder[username].all_tweets.keys(), reverse=True)

        for tw_id in user_tweet_ids:
            tw_text = self.tab_holder[username].all_tweets[tw_id]
            # append to end of listbox
            try:
                listbox.insert(END, tw_text)
            except TclError:
                print(tw_text)
                pass

    def create_description_frame(self):
        self.desc_frame = LabelFrame(self.main_frame, text="Tweet Description")
        self.desc_frame.configure(borderwidth=1)
        self.desc_frame.pack()

        self.desc_text = Label(self.desc_frame)
        self.desc_text.pack()
        self.update_desc_contents("text")

    def update_desc_contents(self, new_text):
        self.desc_text['text'] = new_text
        self.desc_text.pack()

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

