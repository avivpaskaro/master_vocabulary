from tkinter import *

master = Tk()
master.title("Master Vocabulary")

# White canvas
canvas = Canvas(master, width=800, height=600)
canvas.pack()
canvas.create_rectangle(150, 30, 750, 550, fill="white")

# Back button
button_back = Button(master, text="Back")
button_back.pack()
button_back.place(bordermode=OUTSIDE, relheight=0.05, relwidth=0.1, relx=0.01, rely=0.86)

mainloop()