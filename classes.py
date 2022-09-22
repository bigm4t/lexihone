import functions as fn
from pandas import read_csv
from tkinter import Label, Entry, Button, END

font=("Arial", 25)
bg_color = "#31363b"
f_color = "#ffffff"

class Topic:
    def __init__(self, f_name):
        self.f_name = f_name
        self.words = read_csv(self.f_name,sep='\t',encoding='UTF-16')#,engine='python')
        self.score = self.words["Score"].sum()

    def pick_word(self):
        """
        :returns: word index in data frame (int)
        """
        w_idx = self.words.sample(weights=self.words["Score"]).index[0]
        return w_idx

    def update_score(self, w_idx, flag):

        if flag == 'correct':
            factor = 1/1.05
        elif flag == 'wrong':
            factor = 1.05
        elif flag == 'hint':
            factor = 1.02
        elif flag == 'solution':
            factor =  1.1

        self.words.at[w_idx,"Score"] = self.words.loc[w_idx,"Score"]*factor
        self.score = self.words["Score"].sum()

    def save_to_file(self):
        self.words.to_csv(self.f_name, sep='\t', index=False, encoding='UTF-16')

class Backend:
    def __init__(self, f_names):

        self.topics = [Topic(f_name) for f_name in f_names]
        self.curr_topic = fn.topic_picker(self.topics)
        self.curr_w_idx = self.curr_topic.pick_word()

    def get_en_word(self):
        return self.curr_topic.words.loc[self.curr_w_idx, "Source"]

    def get_sng(self):
        return self.curr_topic.words.loc[self.curr_w_idx, "Target"]

    def get_plr(self):
        return self.curr_topic.words.loc[self.curr_w_idx, "Target (plural)"]

    def sng_check(self, guess):

        if guess == self.get_sng():
            flag = "correct"
        else:
            flag = "wrong"

        self.curr_topic.update_score(self.curr_w_idx, flag)
        return flag

    def sng_hint(self):
        sng = self.get_sng()
        self.curr_topic.update_score(self.curr_w_idx, "hint")
        return sng[:5]

    def sng_sol(self):
        sol_word = self.get_sng()
        self.curr_topic.update_score(self.curr_w_idx, "solution")

        return sol_word

    def sng_sound(self):
        fn.read_word(self.get_sng())

    def plr_check(self, guess):
        sol = self.get_plr()

        if guess == sol:
            flag = "correct"
        else:
            flag = "wrong"

        self.curr_topic.update_score(self.curr_w_idx, flag)
        return flag

    def plr_hint(self):
        plr = self.get_plr()
        self.curr_topic.update_score(self.curr_w_idx, "hint")
        return "-"+plr[-2:]

    def plr_sol(self):
        sol_word = self.get_plr()
        self.curr_topic.update_score(self.curr_w_idx, "solution")

        return sol_word

    def plr_sound(self):
        fn.read_word(self.get_plr())

    def next(self):
        self.curr_topic.save_to_file()
        self.curr_topic = fn.topic_picker(self.topics)
        self.curr_w_idx = self.curr_topic.pick_word()
        next_word = self.get_en_word()
        return next_word

    def has_plural(self):
        #True if curr_word has plural
        plr = self.curr_topic.words.loc[self.curr_w_idx,"Target (plural)"]
        return type(plr) is str

class UI:
    def __init__(self,root, f_names):

        self.be = Backend(f_names)

        self.root = root

        self.en_label = Label(self.root, text=self.be.get_en_word(), font=("Arial", 45), fg=f_color, bg=bg_color, width=40, fill=None)
        self.en_label.grid(row = 0, column = 0, columnspan = 7, sticky="nwes", pady=5)

        self.sng_label = Label(self.root, text="Singular", font=font, fg=f_color, bg=bg_color, width=40)
        self.sng_label.grid(row = 1, column = 0,columnspan = 3, sticky="nwes", pady=5)

        self.plr_label = Label(self.root, text="Plural", font=font, fg=f_color, bg=bg_color, width=40)
        self.plr_label.grid(row = 1, column = 4,columnspan = 3,sticky="nwes", pady=5)

        self.sng_box = Entry(self.root, font=font, fg=f_color,bg=bg_color)
        self.sng_box.bind('<Return>',self.sng_box_action)
        self.sng_box.grid(row = 2, column = 0,columnspan = 3, pady=5)
        #
        self.plr_box = Entry(self.root, font=font, fg=f_color,bg=bg_color)
        self.plr_box.bind('<Return>',self.plr_box_action)
        self.plr_box.grid(row = 2, column = 4,columnspan = 3, pady=5)
        #
        self.sng_ans_label = Label(self.root, text="", font=font, fg=f_color,bg=bg_color, width=40)
        self.sng_ans_label.grid(row = 3, column = 0,columnspan = 3, sticky="nwes", pady=5)

        self.plr_ans_label = Label(self.root, text="", font=font, fg=f_color,bg=bg_color, width=40)
        self.plr_ans_label.grid(row = 3, column = 4,columnspan = 3, sticky="nwes", pady=5)

        self.sng_hint_but = Button(self.root, text="Hint", fg=f_color, bg=bg_color, command=self.sng_hint_action, font=font,width=10)
        self.sng_hint_but.grid(row = 4, column=0,padx=20, pady=5)
        self.sng_sol_but = Button(self.root, text="Solution",command=self.sng_sol_action, font=font, fg=f_color, bg=bg_color, width=10)
        self.sng_sol_but.grid(row = 4, column=1, padx=20, pady=5)
        self.sng_sound_but = Button(self.root, text="Play",command=self.sng_sound_action, font=font, fg=f_color, bg=bg_color, width=10, state="disabled")
        self.sng_sound_but.grid(row = 4, column=2, padx=20, pady=5)

        self.spacer = Label(self.root, text="",width=20)
        self.spacer.grid(row=4, column=3)

        self.plr_hint_but = Button(self.root, text="Hint",command=self.plr_hint_action, font=font, fg=f_color, width=10,bg=bg_color)
        self.plr_hint_but.grid(row = 4, column=4, padx=20,pady=5)
        self.plr_sol_but = Button(self.root, text="Solution",command=self.plr_sol_action, font=font, fg=f_color, bg=bg_color, width=10)
        self.plr_sol_but.grid(row = 4, column=5, padx=20, pady=5)
        self.plr_sound_but = Button(self.root, text="Play",command=self.plr_sound_action, font=font, fg=f_color, bg=bg_color, width=10, state="disabled")
        self.plr_sound_but.grid(row = 4, column=6, padx=20, pady=5)

        self.spacer.grid(row=5, column=3, pady=35)

        self.next_but = Button(self.root, text="Next",command=self.next_action, font=font, fg=f_color, bg=bg_color, width=10)
        self.next_but.grid(row = 6, column=3, sticky="s", padx=5, pady=25)

        self.signature_label = Label(self.root, text="Lexihone by bigm4t (2022)", font=("Helvetica", 10), fg="#a3a3a3",bg=bg_color, width=30)
        self.signature_label.grid(row = 7, column = 6,columnspan = 1,sticky="e", pady=5)

        if not self.be.has_plural():
            self.deactivate_plural()

    def sng_box_action(self, event):
        guess = self.sng_box.get()
        result = self.be.sng_check(guess)
        if result == "correct":
            self.sng_ans_label["text"] = "Correct!"
            self.sng_sound_but["state"]="active"
            self.sng_sol_but["state"]="disabled"
            self.sng_hint_but["state"]="disabled"
        else:
            self.sng_ans_label["text"] = "Try again"
            self.sng_box.delete(0, END)

    def sng_hint_action(self):
        hint = self.be.sng_hint()
        self.sng_box.insert(END, hint)
        self.sng_hint_but["state"] = "disabled"

    def sng_sol_action(self):
        sol = self.be.sng_sol()

        self.sng_ans_label["text"] = sol

        self.sng_hint_but["state"] = "disabled"

        self.sng_sol_but["state"] = "disabled"

        self.sng_sound_but["state"] = "active"

        self.sng_box.delete(0, END)

    def sng_sound_action(self):
        self.be.sng_sound()

    def plr_box_action(self, event):
        guess = self.plr_box.get()
        result = self.be.plr_check(guess)
        if result == "correct":
            self.plr_ans_label["text"] = "Correct!"
            self.plr_sound_but["state"]="active"
            self.plr_sol_but["state"]="disabled"
            self.plr_hint_but["state"]="disabled"
        else:
            self.plr_ans_label["text"] = "Try again"
            self.plr_box.delete(0, END)

    def plr_hint_action(self):
        hint = self.be.plr_hint()
        self.plr_box.insert(END, hint)
        self.plr_hint_but["state"] = "disabled"

    def plr_sol_action(self):
        sol = self.be.plr_sol()

        self.plr_ans_label["text"] = sol

        self.plr_hint_but["state"] = "disabled"

        self.plr_sol_but["state"] = "disabled"

        self.plr_sound_but["state"] = "active"

        self.plr_box.delete(0, END)

    def plr_sound_action(self):
        self.be.plr_sound()

    def next_action(self):
        next_word = self.be.next()

        self.en_label["text"] = next_word
        self.sng_ans_label["text"] = ""
        self.plr_ans_label["text"] = ""

        self.sng_hint_but["state"] = "active"
        self.plr_hint_but["state"] = "active"

        self.sng_sol_but["state"] = "active"
        self.plr_sol_but["state"] = "active"

        self.sng_sound_but["state"] = "disabled"
        self.plr_sound_but["state"] = "disabled"

        self.plr_box["state"]="normal"

        self.sng_box.delete(0, END)
        self.plr_box.delete(0, END)

        if not self.be.has_plural():
            self.deactivate_plural()

    def deactivate_plural(self):
        self.plr_box["state"]="disabled"
        self.plr_sound_but["state"]="disabled"
        self.plr_sol_but["state"]="disabled"
        self.plr_hint_but["state"]="disabled"
