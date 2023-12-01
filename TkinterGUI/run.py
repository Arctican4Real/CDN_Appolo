from tkinter import *
import pygame
import os

screen = Tk()
screen.title("Melodia")

#Works for windows
#screen.iconbitmap("")

#Works for linux
img = PhotoImage(file='./sources/icon.gif')
screen.tk.call('wm', 'iconphoto', screen._w, img)
screen.iconphoto(True, img)
screen.resizable(0,0)

pygame.mixer.init()

screen.geometry("310x400")

playBtnImg = PhotoImage(file="./sources/ctrlbtn/play.png")
pauseBtnImg = PhotoImage(file="./sources/ctrlbtn/pause.png")
stopBtnImg = PhotoImage(file="./sources/ctrlbtn/stop.png")
frontBtnImg = PhotoImage(file="./sources/ctrlbtn/front.png")
backBtnImg = PhotoImage(file="./sources/ctrlbtn/back.png")

global playState
playState = 0

# def play():
#     print("Play pressed")
#     pygame.mixer.music.load("./music/music.mp3")
#     pygame.mixer.music.play(loops=0)


def stop():
    print("Stop pressed")
    pygame.mixer.music.stop()

    global playState
    playState = 0

    mainBtn.configure(image=playBtnImg)
    mainBtn.photo = playBtnImg

def mainBtnFunc(mainQuery):
    global playState
    mainQuery = playState

    if playState == 0:
        print("Play pressed first time")

        track = trackBox.get(ACTIVE)
        track = track.replace(" ", "_")
        track = f"./music/{track}.mp3"

        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops=0)
        playstate = 1

    if playState == 1 :
        pygame.mixer.music.pause()
        print("Paused")
        playState = 2

        mainBtn.configure(image=playBtnImg)
        mainBtn.photo = playBtnImg
        
    else:
        pygame.mixer.music.unpause()
        print("Unpaused")
        playState = 1

        mainBtn.configure(image=pauseBtnImg)
        mainBtn.photo = pauseBtnImg

def nextTrack(move):
    global playState

    curTrack = trackBox.curselection()[0]

    if curTrack == 0 and move == -1:
        nextTrack = trackBox.size()-1
    elif curTrack == (trackBox.size()-1) and move == 1:
        nextTrack = 0
    else:
        nextTrack = trackBox.curselection()[0]+move


    print("Current song is number", nextTrack)
    playTrack = trackBox.get(nextTrack)
    playTrack = playTrack.replace(" ", "_")
    playTrack = f"./music/{playTrack}.mp3"

    trackBox.selection_clear(0, END)
    trackBox.activate(nextTrack)
    trackBox.selection_set(nextTrack,last=None)

    playState = 0
    mainBtnFunc(0)

# def prevTrack():
#     nextTrack = trackBox.curselection()[0]-move
#     # print("Current song is number", nextTrack)
#     playTrack = trackBox.get(nextTrack)
#     playTrack = playTrack.replace(" ", "_")
#     playTrack = f"./music/{playTrack}.mp3"

#     trackBox.selection_clear(0, END)
#     trackBox.activate(nextTrack)
#     trackBox.selection_set(nextTrack,last=None)

#     mainBtnFunc(0)

trackBox = Listbox(screen, bg="white",fg="blue",width=30)
trackBox.pack(pady=50)
trackBox.activate(0)


for name in os.listdir("./music"):
    name = name.replace(".mp3", "")
    name = name.replace("_", " ")
    trackBox.insert('end', name)

btnDiv = Frame(screen)
btnDiv.pack()

mainBtn = Button(btnDiv, image=playBtnImg , borderwidth=0, command=lambda:mainBtnFunc(playState))
stopBtn = Button(btnDiv, image=stopBtnImg , borderwidth=0, command=stop)
backBtn = Button(btnDiv, image=backBtnImg , borderwidth=0, command=lambda:nextTrack(-1))
frontBtn = Button(btnDiv, image=frontBtnImg , borderwidth=0, command=lambda:nextTrack(1))

backBtn.grid(row=0,column=0, padx=20)
mainBtn.grid(row=0,column=1, padx=20)
frontBtn.grid(row=0,column=2, padx=20)

stopBtn.grid(row=1,column=1, pady=10)

# pauseBtn = Button(btnDiv, image=pauseBtnImg , borderwidth=0,command=lambda:mainBtn(mainQuery)) 
# pauseBtn.grid(row=0,column=2, padx=10)



#playbtn = Button(screen, text="Play",font=("./sources/Roboto-Black.ttf", 32), command=play)
#playbtn.pack(pady=20)

#stopbtn = Button(screen, text="Stop",font=("./sources/Roboto-Black.ttf", 32), command=stop)
#stopbtn.pack(pady=20)

screen.mainloop()
