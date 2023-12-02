from tkinter import *
import pygame
from PIL import ImageTk,Image
import os

screen = Tk()
screen.title("Melodia")

#Works for windows
#screen.iconbitmap("")

#Works for linux
img = PhotoImage(file='./sources/icon.gif')
screen.tk.call('wm', 'iconphoto', screen._w, img)
screen.iconphoto(True, img)
#screen.resizable(0,0)

pygame.mixer.init()

screen.geometry("440x600")

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

def changeCover(trackNum):
    # albumCover = trackBox.get(ACTIVE)
    # albumCover = albumCover.replace(" ", "_")
    # albumCover = albumCover.replace(".mp3", "")
    # albumCover = f"./music/albumCover/{albumCover}-cover.jpg"
    # #print(f"ALBUM COVER FILE NAME : {albumCover}")

    # curCover = Image.open(albumCover)
    # curCover = curCover.resize((300,300), Image.ANTIALIAS)
    # curCover = ImageTk.PhotoImage(curCover)

    # curCoverLabel.configure(image=curCover) 

    #####
    global curCover

    albumCover = tracks[trackNum]
    albumCover = albumCover.replace(".mp3", "")
    albumCover = f"./music/albumCover/{albumCover}-cover.jpg"


    curCover = Image.open(albumCover)
    curCover = curCover.resize((300,300), Image.ANTIALIAS)
    curCover = ImageTk.PhotoImage(curCover)

    curCoverLabel.configure(image=curCover)

def stop():
    print("Stop pressed")
    pygame.mixer.music.stop()

    global playState
    playState = 0

    mainBtn.configure(image=playBtnImg)
    mainBtn.photo = playBtnImg

def mainBtnFunc(mainQuery):
    global playState
    global tracks
    mainQuery = playState

    if playState == 0:
        print("Play pressed first time")

        track = trackBox.get(ACTIVE)

        track = track.replace(" ", "_")
        track = f"./music/{track}.mp3"
        trackIndex = tracks.index(track.replace("./music/", ""))


        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops=0)
        playstate = 1

        changeCover(trackIndex)


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

    changeCover(nextTrack)  

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
trackBox.activate(0)

global tracks
tracks = []

for name in os.listdir("./music"):
    if name in [".gitignore", "albumCover"]:
        continue
    tracks.append(name)


tracks = sorted(tracks)

for name in tracks:
    name = name.replace(".mp3", "")
    name = name.replace("_", " ")
    trackBox.insert('end', name)

albumCover = tracks[0]
albumCover = albumCover.replace(".mp3", "")
albumCover = f"./music/albumCover/{albumCover}-cover.jpg"

global curCover

curCover = Image.open(albumCover)
curCover = curCover.resize((300,300), Image.ANTIALIAS)
curCover = ImageTk.PhotoImage(curCover)

curCoverLabel = Label(image=curCover)
curCoverLabel.pack(pady=20)

trackBox.pack()

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
