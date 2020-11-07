from tkinter import *

master = Tk()
master.title("Master Vocabulary")

# White canvas
canvas = Canvas(master, width=800, height=600)
canvas.pack()
canvas.create_rectangle(150, 30, 750, 550, fill="white")

# Add word button
button_add_word = Button(master, text="Add Word")
button_add_word.pack()
button_add_word.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.1, relx=0.01, rely=0.05)

# Classify button
button_classify = Button(master, text="Classify")
button_classify.pack()
button_classify.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.1, relx=0.01, rely=0.11)

# Study button
button_study = Button(master, text="Study")
button_study.pack()
button_study.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.1, relx=0.01, rely=0.17)

# Src language
LANGUAGE = [
    "English",
    "Hebrew",
    "Italian"
]
src_language = StringVar(master)
src_language.set(LANGUAGE[0])  # default value
src_language_menu = OptionMenu(master, src_language, *LANGUAGE)
src_language_menu.pack()
src_language_menu.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.1, relx=0.058, rely=0.755)
src_language_lbl = Label(master, text="From")
src_language_lbl.pack()
src_language_lbl.place(bordermode=OUTSIDE, relx=0.01, rely=0.765)

# Dst language
dst_language = StringVar(master)
dst_language.set(LANGUAGE[1])  # default value
dst_language_menu = OptionMenu(master, dst_language, *LANGUAGE)
dst_language_menu.pack()
dst_language_menu.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.1, relx=0.058, rely=0.81)
dst_language_lbl = Label(master, text="To")
dst_language_lbl.pack()
dst_language_lbl.place(bordermode=OUTSIDE, relx=0.01, rely=0.815)

# Practice quantity
BATCH = [
    "10",
    "20",
    "30"
]
batch = StringVar(master)
batch.set(BATCH[0])  # default value
batch_menu = OptionMenu(master, batch, *BATCH)
batch_menu.pack()
batch_menu.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.06, relx=0.058, rely=0.865)
batch_lbl = Label(master, text="Batch")
batch_lbl.pack()
batch_lbl.place(bordermode=OUTSIDE, relx=0.01, rely=0.87)

mainloop()
