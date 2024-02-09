from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}


try:
    data = pandas.read_csv("data/to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    # Each column's value as a list
    to_learn = data.to_dict(orient="records")



# ---------------------------- Create New Flashcards ------------------------------- #
def next_card():
    global current_card, flip_timer
    # The time counts down in the background. Otherwise, the card would flip
    # right away if you are on a new card, and you want to wait 3 secs.
    # Every time we are on a new card, invalidate the timer.
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    current_word = current_card["French"]
    # Change the color of text back to black
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_word, fill="black")
    # Flip back to the front of the card after clicking the buttons
    canvas.itemconfig(card_background, image=card_front_img)
    # We need to flip card every single time we go to the next card
    flip_timer = window.after(3000, func=flip_card)


# ---------------------------- FLIP THE CARD MECHANISM ------------------------------- #
"""Changing the card to show the English word for the current card,
change the image to card_back from card_front, and also change the color
of the text as well"""


def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")
    """Photo Images should not be created inside a function. 
    Otherwise, it would not work. """
    canvas.itemconfig(card_background, image=card_back_img)


# ---------------------------- SAVE PROGRESS ------------------------------- #
def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# window.after(): execute a command after time delay
flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)

check_button_img = PhotoImage(file="images/right.png")
check_button = Button(image=check_button_img, highlightthickness=0, command=is_known)
check_button.grid(row=1, column=1)

unknown_button_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_button_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

# Call this function once we have created the UI before we get to our mainloop()
next_card()

window.mainloop()
