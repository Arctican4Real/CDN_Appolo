#import necessary libraries
from tkinter import *
from PIL import ImageTk, Image
import tkinter.ttk as ttk
from tkinter import messagebox

# Define color constants
bgMain = "#171D1C"
bgSec = "#252D2D"
fgMain = "#F9F9ED"
accent = "#3695F5"

#Create the main tkinter screen
screen = Tk()
screen.title("Melodia")
screen.configure(bg=bgMain)

# Import and display program icon
img = PhotoImage(file="./sources/icon.gif")
screen.tk.call("wm", "iconphoto", screen._w, img)
screen.iconphoto(True, img)

# Set window properties
# screen.resizable(0, 0)
# Default 330x550
screen.geometry("510x470")

# Load control button images
global playBtnImg, pauseBtnImg, stopBtnImg, frontBtnImg, backBtnImg
playBtnImg = PhotoImage(file="./sources/ctrlbtn/playBtnImgBlue.png")
pauseBtnImg = PhotoImage(file="./sources/ctrlbtn/pauseBtnImgBlue.png")
stopBtnImg = PhotoImage(file="./sources/ctrlbtn/stopBtnImgBlue.png")
frontBtnImg = PhotoImage(file="./sources/ctrlbtn/frontBtnImgBlue.png")
backBtnImg = PhotoImage(file="./sources/ctrlbtn/backBtnImgBlue.png")

###CODE HERE###

# Code for main menu bar
settings = Menu(screen, bg=bgSec, fg=fgMain, bd=0)
screen.config(menu=settings)

# Code for download button on menu bar
downloadMenu = Menu(settings, bg=bgMain, fg=fgMain, bd=0)

# Placeholder download button
# settings.add_cascade(label="Download",menu=downloadMenu)
settings.add_command(label="Download")

# Code for themes button on menu bar
themeMenu = Menu(settings, bg=bgMain, fg=fgMain, bd=0, tearoff="off")
settings.add_cascade(label="Theme", menu=themeMenu)
# themeMenu.add_command(label="Magma", command=lambda: changeColor("RED"))
# themeMenu.add_command(label="Lush", command=lambda: changeColor("GREEN"))
# themeMenu.add_command(label="Moonlit", command=lambda: changeColor("BLUE"))
# themeMenu.add_command(label="Nebula", command=lambda: changeColor("PURPLE"))

# Button to reload the tracks
settings.add_command(label="Reload")

# Frames
left_frame = Frame(screen, bg=bgMain)
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

right_frame = Frame(screen, bg=bgMain)
right_frame.grid(row=0, column=1, padx=10, pady=(10,20), sticky="nsew")

down_frame = Frame(screen, bg=bgMain, height=50, width=490)
down_frame.grid(row=1, column=0, padx=10, pady=0,columnspan=3)

btnDiv = Frame(screen, bg=bgMain,height=50,width=490)
btnDiv.grid(row=2,column=0,padx=10,pady=10,columnspan=3)

# Create a listbox to display tracks
trackBox = Listbox(
    right_frame,
    bg=bgSec,
    fg=fgMain,
    # width =20, 
    # height=17,
    borderwidth=0,
    highlightthickness=0,
    selectbackground=accent,
    selectborderwidth=0,
)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)
trackBox.grid(row=0,column=0,sticky="nsew")

# Defualt to the first track in the listbox
trackBox.activate(0)
trackBox.selection_set(0)

#Scroll wheel for track box
scroll = Scrollbar(right_frame, width=10)
scroll.grid(row=0,column=1,sticky="ns")

#Functionality of the scroll bar
trackBox.config(yscrollcommand=scroll.set)
scroll.config(command=trackBox.yview)

c=0
for i in range(100):
	trackBox.insert("end", f"name{c}")
	c+=1

#Cover art
global curCover
curCover = Image.open("./sources/template.png")
curCover = curCover.resize((250, 250), Image.LANCZOS)
curCover = ImageTk.PhotoImage(curCover)

curCoverLabel = Label(left_frame,image=curCover, borderwidth=0, highlightthickness=4, highlightbackground=bgSec)
curCoverLabel.grid(pady=10,column=0,row=0)


# Display the song duration
durLabel = Label(
    left_frame,
    text="00:00",
    borderwidth=0,
    highlightthickness=0,
    bd=0,
    bg=bgMain,
    fg=fgMain,
    width=20,
    height=1,
    font=("Arial", 16),
)

durLabel.grid(row=2,column=0, columnspan=1,pady=10)

# Slider for song duration
slider = ttk.Scale(
    down_frame,
    from_=0,
    to=100,
    orient=HORIZONTAL,
    value=0,
    length=470,
    #command=slide,
)
slider.pack(pady=10,ipadx=10)

# Display the current song name
curTitle = Label(left_frame, text="Late Nights - Wallow", bd=1, bg=accent, fg=bgMain)
curTitle.grid(row=1,column=0, ipady=0, pady=0,sticky="ew")

#Buttons

# Create control buttons
mainBtn = Button(
    btnDiv,
    image=playBtnImg,
    borderwidth=0,
    #command=lambda: mainBtnFunc(playState),
    bg=bgMain,
    highlightthickness=0,
    bd=0,
)
stopBtn = Button(
    btnDiv,
    image=stopBtnImg,
    borderwidth=0,
    #command=stop,
    bg=bgMain,
    highlightthickness=0,
    bd=0,
)
backBtn = Button(
    btnDiv,
    image=backBtnImg,
    borderwidth=0,
    #command=lambda: nextTrack(-1),
    bg=bgMain,
    highlightthickness=0,
    bd=0,
)
frontBtn = Button(
    btnDiv,
    image=frontBtnImg,
    borderwidth=0,
    #command=lambda: nextTrack(1),
    bg=bgMain,
    highlightthickness=0,
    bd=0,
)

# Grid layout for control buttons
backBtn.grid(row=0, column=0, padx=(60,60), pady=(0,10))
mainBtn.grid(row=0, column=1, padx=(0,60), pady=(0,10))
stopBtn.grid(row=0, column=2, padx=(0,60), pady=(0,10))
frontBtn.grid(row=0, column=3, padx=(0,60), pady=(0,10))

#initiate
screen.mainloop()