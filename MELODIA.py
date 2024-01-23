from tkinter import *
from PIL import ImageTk, Image

#colors
co1 = "#ffffff" #white
co2 = "#f2d7ee" #pale pink
co3 = "#c8cacc" #
co4 = "#82a3a1" #pale green

window = Tk()
window.title ("Melodia")
window.geometry('352x255')
window.configure(background=co1)
window.resizable(width=False, height=False)

#frames
left_frame = Frame(window, width=150, height=150, bg=co3)
left_frame.grid(row=0, column=0, padx=1, pady=1)

right_frame = Frame(window, width=250, height=150, bg=co1)
right_frame.grid(row=0, column=1, padx=0)

down_frame = Frame(window, width=400, height=100, bg=co4)
down_frame.grid(row=1, column=0, columnspan=3, padx=0, pady=1)

#right frame
listbox = Listbox(right_frame,selectmode=SINGLE, font=("Arial 9 bold"), width=22, bg=co2, fg=co1)
listbox.grid(row=0, column=0)

scroll = Scrollbar(right_frame)
scroll.grid(row=0, column=1)

listbox.config(yscrollcommand=scroll.set)
scroll.config(command=listbox.yview)

#Images
##img_1 = Image.open('')
##img_1 = img_1.resize((130, 130))
##img_1 = ImageTk.PhotoImage(img_1)
##app_image = Label(left_frame, height=130, image=img_1, padx=10)
##app_image.place(x=24, y=15)

running_song = Label(down_frame, font=("Ivy 10"), width=44, height=1, padx=10, bg=co1, fg=co3, anchor=NW)
running_song.place(x=0, y=1)

img_2 = Image.open('Icons/rewind.png')
img_2 = img_2.resize((45, 45))
img_2 = ImageTk.PhotoImage(img_2)
prev_image = Button(down_frame, width=40, height=40, image=img_2, padx=10, font=("Ivy 10"), borderwidth=0)
prev_image.place(x=10+28, y=35)

img_3 = Image.open('Icons/play.png')
img_3 = img_3.resize((45, 45))
img_3 = ImageTk.PhotoImage(img_3)
play_image = Button(down_frame, width=40, height=40, image=img_3, padx=10, font=("Ivy 10"), borderwidth=0)
play_image.place(x=56+28, y=35)

img_4 = Image.open('Icons/pause.png')
img_4 = img_4.resize((45, 45))
img_4 = ImageTk.PhotoImage(img_4)
pause_image = Button(down_frame, width=40, height=40, image=img_4, padx=10, font=("Ivy 10"), borderwidth=0)
pause_image.place(x=102+28, y=35)

img_5 = Image.open('Icons/fastforward.png')
img_5 = img_5.resize((45, 45))
img_5 = ImageTk.PhotoImage(img_5)
fastfor_image = Button(down_frame, width=40, height=40, image=img_5, padx=10, font=("Ivy 10"), borderwidth=0)
fastfor_image.place(x=148+28, y=35)

img_6 = Image.open('Icons/stop.png')
img_6 = img_6.resize((45, 45))
img_6 = ImageTk.PhotoImage(img_6)
stop_image = Button(down_frame, width=40, height=40, image=img_6, padx=10, font=("Ivy 10"), borderwidth=0)
stop_image.place(x=194+28, y=35)

#x=240+28




window.mainloop()








