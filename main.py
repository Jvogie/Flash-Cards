from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

#---------------------------------------------------------------------------------------------------
random_choice={}
word_dict={}

try:
    word_data_frame= pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    word_dict=original_data.to_dict(orient="records")
else:
    word_dict= word_data_frame.to_dict(orient="records")


def next_card():
    global random_choice, flip_timer
    window.after_cancel(flip_timer)
    random_choice = random.choice(word_dict)
    canvas.itemconfig(current_image, image=card_front)
    canvas.itemconfig(language_title, text= "French", fill="black")
    canvas.itemconfig(word_to_learn, text = random_choice['French'], fill = "black")
    flip_timer=window.after(3000, func=card_flip)


def card_flip():

    canvas.itemconfig(current_image, image=card_back)
    canvas.itemconfig(language_title, text="English", fill="white")
    canvas.itemconfig(word_to_learn, text=random_choice['English'], fill="white")

def is_known():
    word_dict.remove(random_choice)
    data=pandas.DataFrame(word_dict)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()
#---------------------------------------UI Interface--------------------------------------------------

#window
window =Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func= card_flip)

#Flashcard / canvas
canvas=Canvas( width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
current_image = canvas.create_image(400, 263, image=card_front)

language_title=canvas.create_text(400, 150, text="Title", font=("Ariel", 40, "italic"))
word_to_learn=canvas.create_text(400, 263, text="word", font=("Ariel", 60, "bold"))

canvas.grid(column=0, row=0, columnspan=2)

#right/ check mark button
right= PhotoImage(file="images/right.png")
right_button=Button(image=right, highlightthickness=0, bg=BACKGROUND_COLOR, command= is_known)
right_button.grid(column=1, row=1)

#wrong/ X button
wrong= PhotoImage(file="images/wrong.png")
wrong_button=Button(image=wrong, highlightthickness=0, bg=BACKGROUND_COLOR, command= next_card)
wrong_button.grid(column=0, row=1)

next_card()

window.mainloop()