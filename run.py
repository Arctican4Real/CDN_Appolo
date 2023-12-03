from tkinter import *
import pygame
from PIL import ImageTk, Image
import os

bgBlack = "#171D1C"
fgWhite = "#EFE9F4"
AccentBlue = "#3695F5"

screen = Tk()
screen.title("Melodia")
screen.configure(bg=bgBlack)

# Works for windows

# screen.iconbitmap("./sources/icon.ico")

# Works for linux
img = PhotoImage(file="./sources/icon.gif")

screen.tk.call("wm", "iconphoto", screen._w, img)
screen.iconphoto(True, img)

screen.resizable(0, 0)

pygame.mixer.init()

screen.geometry("330x500")

playBtnImg = PhotoImage(file="./sources/ctrlbtn/play.png")
pauseBtnImg = PhotoImage(file="./sources/ctrlbtn/pause.png")
stopBtnImg = PhotoImage(file="./sources/ctrlbtn/stop.png")
frontBtnImg = PhotoImage(file="./sources/ctrlbtn/front.png")
backBtnImg = PhotoImage(file="./sources/ctrlbtn/back.png")

global playState
playState = 0


def changeCover(trackNum):
    global curCover

    albumCover = tracks[trackNum]
    albumCover = albumCover.replace(".mp3", "")
    albumCover = f"./music/albumCover/{albumCover}-cover.jpg"

    curCover = Image.open(albumCover)
    curCover = curCover.resize((250, 250), Image.ANTIALIAS)
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
        pygame.mixer.music.pause()
        print("Play pressed first time")

        track = trackBox.get(ACTIVE)

        track = track.replace(" ", "_")
        track = f"./music/{track}.mp3"
        trackIndex = tracks.index(track.replace("./music/", ""))

        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops=0)
        playstate = 1

        changeCover(trackIndex)

    if playState == 1:
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
        nextTrack = trackBox.size() - 1
    elif curTrack == (trackBox.size() - 1) and move == 1:
        nextTrack = 0
    else:
        nextTrack = trackBox.curselection()[0] + move

    print("Current song is number", nextTrack)
    playTrack = trackBox.get(nextTrack)
    playTrack = playTrack.replace(" ", "_")
    playTrack = f"./music/{playTrack}.mp3"

    trackBox.selection_clear(0, END)
    trackBox.activate(nextTrack)
    trackBox.selection_set(nextTrack, last=None)

    changeCover(nextTrack)

    playState = 0
    mainBtnFunc(0)


trackBox = Listbox(
    screen,
    bg="#171D1C",
    fg=fgWhite,
    width=30,
    height=5,
    borderwidth=0,
    highlightthickness=0,
    selectbackground=AccentBlue,
    selectborderwidth=0,
)
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
    trackBox.insert("end", name)

albumCover = tracks[0]
albumCover = albumCover.replace(".mp3", "")
albumCover = f"./music/albumCover/{albumCover}-cover.jpg"

global curCover

curCover = Image.open(albumCover)
curCover = curCover.resize((250, 250), Image.ANTIALIAS)
curCover = ImageTk.PhotoImage(curCover)

curCoverLabel = Label(image=curCover, borderwidth=0, highlightthickness=0)
curCoverLabel.pack(pady=20)

trackBox.pack()

btnDiv = Frame(screen, bg=bgBlack, pady=10, bd=0)
btnDiv.pack()

mainBtn = Button(
    btnDiv,
    image=playBtnImg,
    borderwidth=0,
    command=lambda: mainBtnFunc(playState),
    bg=bgBlack,
    highlightthickness=0,
    bd=0,
)
stopBtn = Button(
    btnDiv,
    image=stopBtnImg,
    borderwidth=0,
    command=stop,
    bg=bgBlack,
    highlightthickness=0,
    bd=0,
)
backBtn = Button(
    btnDiv,
    image=backBtnImg,
    borderwidth=0,
    command=lambda: nextTrack(-1),
    bg=bgBlack,
    highlightthickness=0,
    bd=0,
)
frontBtn = Button(
    btnDiv,
    image=frontBtnImg,
    borderwidth=0,
    command=lambda: nextTrack(1),
    bg=bgBlack,
    highlightthickness=0,
    bd=0,
)

backBtn.grid(row=0, column=0, padx=20)
mainBtn.grid(row=0, column=1, padx=20)
frontBtn.grid(row=0, column=2, padx=20)

stopBtn.grid(row=1, column=1, pady=10)

screen.mainloop()
