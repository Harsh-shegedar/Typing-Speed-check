import csv
import os
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfile, asksaveasfile
import PIL
from PIL import Image, ImageTk, ImageDraw, ImageFont
import random

user_words = []
showed_words = []
words_data = []
wpm_count = 0
cpm_count = 0
display = ""
BACKGROUND = "#B1DDC6"


def start_timer():
    if window.time_id is not None:
        window.after_cancel(window.time_id)
    count_down(60)


def count_down(count):
    if count > 0:
        window.time_id = window.after(1000, count_down, count-1)
    else:
        window.time_id =None
    if count < 10:
        count = f"0{count}"
    if count == "00":
        compare()
        restart_button["state"] = "normal"
        window.bind("<Return>", start)
    timer_text.config(text=f"{count}")


def user_type(event):
    user_words.append(entry_box.get().title().strip())
    entry_box.delete(0, "end")
    if len(user_words) % 8 == 0:
        random_words()

#Import words list
with open("words.csv") as file:
    data = csv.reader(file)
    for row in data:
        words_data.append(''.join(row))



def compare():
    global cpm_count, wpm_count
    entry_box.config(state="disabled")
    for i in user_words:
        if i in showed_words:
            wpm_count += 1
            cpm_count += len(i)
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    print(f"user typed: {user_words}")
    print(f"display words: {showed_words}")


def random_words():
    global display
    display = ""
    for i in range(8):
        display_word = random.choice(words_data)
        showed_words.append(display_word)
        display += (display_word + " ")
    canvas.itemconfig(word_show, text=display)


def restart():
    global showed_words, user_words, wpm_count, cpm_count
    showed_words = []
    user_words = []
    wpm_count = 0
    cpm_count = 0
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    entry_box.config(state="normal")
    start_timer()
    random_words()




def start(event):
    global showed_words, user_words, wpm_count, cpm_count
    showed_words = []
    user_words = []
    wpm_count = 0
    cpm_count = 0
    wpm_value.config(text=wpm_count)
    cpm_value.config(text=cpm_count)
    entry_box.config(state="normal")
    start_timer()
    random_words()
    window.unbind("<Return>")








window = Tk()
window.title("Typing Speed Check")
window.config(padx=50, pady=50, bg=BACKGROUND)
window.time_id = None

canvas = Canvas(window, width=400, height=263, bg=BACKGROUND, bd=0)
card_img = PhotoImage(file="./card.png")
restart_btn = PhotoImage(file="./reload.png")


canvas.create_image(200, 132, image=card_img)
word_show = canvas.create_text(200, 132, text="press the space bar after each word\n\n-press enter to start-", font=("Courier", 14, "bold"), fill="white", justify="center", width=250)
canvas.grid(row=1, column=1, columnspan=6)

cpm_label = Label(text="Corrected CPM: ", font=("Arial", 14), bg=BACKGROUND)
cpm_label.grid(row=3, column=1, pady=20)
cpm_value = Label(text="?", font=("Arial", 14), bg=BACKGROUND)
cpm_value.grid(row=3, column=2)

wpm_label = Label(text="WPM: ", font=("Arial", 14), bg=BACKGROUND)
wpm_label.grid(row=4, column=1, pady=20)
wpm_value = Label(text="?", font=("Arial", 14), bg=BACKGROUND)
wpm_value.grid(row=4, column=2)

timer_label = Label(text="time left: ", font=("Arial", 14), bg=BACKGROUND)
timer_label.grid(row=5, column=1, pady=20)
timer_text = Label(text="60", font=("Arial", 14), bg=BACKGROUND)
timer_text.grid(row=5, column=2)

entry_box = Entry(window, bg="white", bd=0, font=("Arial", 14), justify="center", width=30)
entry_box.focus()
entry_box.grid(row=2, column=1, columnspan=6)
window.bind("<space>", user_type)
window.bind("<Return>", start)

restart_button = Button(image=restart_btn, bg=BACKGROUND, highlightthickness=0, bd=0, command=restart)
restart_button.grid(row=6, column=3)







window.mainloop()