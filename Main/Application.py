"""
Application will be the main driver of all activity.
Any screen which appears will always be loaded up from this module.
"""

from tkinter import *
from tkinter.ttk import *

from Main.twitterWrapper import TwitterWrapper
from Main.myClassifier import MyClassifier
from nltk import *

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

        # cannot have a tab with empty username
        if username != "@":

            tab_frame = Frame(self.notebook)
            self.notebook.add(tab_frame, text=username)

            # make TwitterWrapper
            tWrapper = TwitterWrapper(username, 20)

            # Create listbox in tab_frame
            tweet_listbox = Listbox(tab_frame, width=100, height=20, selectmode=SINGLE) # width=X-chars, height=Y-lines
            tweet_listbox.pack()

            # create referencing points
            self.tab_holder[username] = [tWrapper, tweet_listbox]  # list holds TwitterWrapper, tweet_listbox

            self.update_listbox_tweets(username, tweet_listbox)

            refresh_button = Button(tab_frame, text="Refresh", command=self.update_tweets)
            refresh_button.pack()
            # set up bindings

            tweet_listbox.bind("<<ListboxSelect>>", self.update_desc_contents)

    def update_listbox_tweets(self, username, listbox):
        user_tweet_ids = sorted(self.tab_holder[username][0].all_tweets.keys(), reverse=True)

        for tw_id in user_tweet_ids:
            tw_text = self.tab_holder[username][0].all_tweets[tw_id]
            # append to end of listbox
            try:
                listbox.insert(END, tw_text)
            except TclError:
                # remove the emojis out of BMP range
                tw_text = tw_text.encode(encoding='cp1251', errors='ignore').decode(encoding='cp1251')

                # encode text in UTF-8, just in case its not
                tw_text = tw_text.encode(encoding='utf-8').decode(encoding='utf-8')
                listbox.insert(END, tw_text)

    def update_tweets(self):
        """
        Updates tweets for current tab's username
        :return:
        """
        # get current tab
        curr_tab_index = self.notebook.index(tab_id=CURRENT)
        curr_tab = self.notebook.tabs()[curr_tab_index]

        # get username
        username = self.notebook.tab(CURRENT, 'text')

        # get listbox
        tw_listbox = self.tab_holder[username][1]

        # update the tweets
        self.update_listbox_tweets(username, tw_listbox)

    def create_description_frame(self):
        self.desc_frame = LabelFrame(self.main_frame, text="Tweet Description")
        self.desc_frame.configure(borderwidth=1)
        self.desc_frame.pack()

        self.desc_text_line1 = Label(self.desc_frame) # max width will be 90 characters
        self.desc_text_line1.pack()
        self.desc_text_line2 = Label(self.desc_frame) # max width will be 50 characters
        self.desc_text_line2.pack()


    def update_desc_contents(self, event):
        # get current tab
        curr_tab_index = self.notebook.index(tab_id=CURRENT)
        curr_tab = self.notebook.tabs()[curr_tab_index]

        # get username
        username = self.notebook.tab(CURRENT, 'text')

        # get listbox
        tw_listbox = self.tab_holder[username][1]

        # get index of current selection
        curr_index = tw_listbox.curselection()

        # get value of current selection
        new_text = tw_listbox.get(curr_index)
        print(len(new_text))
        # update text in description_frame
        if len(new_text) > 100:
            new_text_list = word_tokenize(new_text)
            n_words = len(new_text_list)
            self.desc_text_line1['text'] = ' '.join(new_text_list[0:(n_words//2)])
            self.desc_text_line2['text'] = ' '.join(new_text_list[((n_words // 2) + 1):])
        else:
            self.desc_text_line1['text'] = new_text
#        self.desc_text_line1.pack()

    def get_username_callback(self):
        val = self.username_ent.get()
        self.username_ent.delete(0, END)
        self.username_ent.insert(END, "@")
        return val

#####################
# TODO:

if __name__ == '__main__':
    root = Tk()
    app = Application(root)
    app.mainloop()

