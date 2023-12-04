"""
DISCLAIMER:
The following script displays all available fonts in the Tkinter system.
It is included in this file for easier viewing and changing of fonts in the GUI.
This code is NOT made by our group, but kindly shared by "Peque" on Stack Overflow.
This code serves no function to the main program, it is for simply viewing fonts.
"""

from tkinter import *
from tkinter import font

root = Tk()
root.title('Font Families')
fonts=list(font.families())
fonts.sort()

def populate(frame):
    '''Put in the fonts'''
    listnumber = 1
    for item in fonts:
        label = "listlabel" + str(listnumber)
        label = Label(frame,text=item,font=(item, 16)).pack()
        listnumber += 1

def onFrameConfigure(canvas):
    '''Reset the scroll region to encompass the inner frame'''
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(root, borderwidth=0, background="#ffffff")
frame = Frame(canvas, background="#ffffff")
vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)

vsb.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)
canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

populate(frame)

root.mainloop()