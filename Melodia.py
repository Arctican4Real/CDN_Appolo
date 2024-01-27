# Import necessary libraries
from tkinter import *
import pygame
from PIL import ImageTk, Image
import os
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
from tkinter import messagebox
import download
import webbrowser
from sys import platform
import random

# Define color constants
bgMain = "#1A1C26"
bgSec = "#2D2E39"
fgMain = "#F4F4F2"
accent = "#3498DB"


global USER_OS
OS_LINUX=1
OS_MAC=2
OS_WIN=3
#Identify operating system
if platform == "linux":
    USER_OS = OS_LINUX
elif platform == "darwin":
    USER_OS = OS_MAC
elif platform == "win32":
    USER_OS = OS_WIN

#Create the main tkinter screen
screen = Tk()
screen.title("Melodia")
screen.configure(bg=bgMain)

#Modify the width of ttk slider (its too fat)
s = ttk.Style()
s.configure("Horizontal.TScale",sliderthickness=12)

# Import and display program icon
img = PhotoImage(file="./sources/icon.gif")
screen.tk.call("wm", "iconphoto", screen._w, img)
screen.iconphoto(True, img)

# Set window properties
screen.resizable(0, 0)
# Default 330x550
screen.geometry("510x470")

# Load control button images
global playBtnImg, pauseBtnImg, stopBtnImg, frontBtnImg, backBtnImg, shuffleBtnImg
playBtnImg = PhotoImage(file="./sources/ctrlbtn/playBtnImgBlue.png")
pauseBtnImg = PhotoImage(file="./sources/ctrlbtn/pauseBtnImgBlue.png")
stopBtnImg = PhotoImage(file="./sources/ctrlbtn/stopBtnImgBlue.png")
frontBtnImg = PhotoImage(file="./sources/ctrlbtn/frontBtnImgBlue.png")
backBtnImg = PhotoImage(file="./sources/ctrlbtn/backBtnImgBlue.png")
shuffleBtnImg = PhotoImage(file="./sources/ctrlbtn/shuffleBtnImgBlue.png")

#Shuffle button greyed out
global shuffleBtnImgGray
shuffleBtnImgGray = PhotoImage(file="./sources/ctrlbtn/shuffleBtnImgGray.png")


# Initialize global variable for play state, as well as what play state means
global playState
SONG_NOT_PLAYING = 0
SONG_IS_PLAYING = 1
SONG_IS_PAUSED = 2

# Initially, we dont want teh song to be playing
playState = SONG_NOT_PLAYING

#Global variable for shuffle
global shuffleState
shuffleState = False

# Initialize the Pygame mixer
pygame.mixer.init()

# Various functions used in the program
# Function to change song duration (and auto play)
def changeDur():
    global tracks
    global playState

    # If the song is stopped, dont do all this
    if playState == SONG_NOT_PLAYING:
        return

    # Grab current time, edit the duration text (as integer)
    currentDur = pygame.mixer.music.get_pos() / 1000

    # Sometimes there is a error when song is played, so fix it
    if currentDur < 0:
        currentDur = 0

    # Convert it into proper format
    convCurrentDur = time.strftime("%M:%S", time.gmtime(currentDur))

    # Getting the total time
    songLen = songLengthGrabber()

    # Convert again
    convTotLen = time.strftime("%M:%S", time.gmtime(songLen))

    # Small bug where current dur is not responsive of the first second
    currentDur += 1

    # Change the position and size of slider
    slider.config(to_=songLen, value=int(slider.get()))

    # If the song has finished playing
    if int(slider.get()) == int(songLen):
        # Show that the song is complete
        durLabel.config(text=f"{convTotLen} / {convTotLen}")
        
        #if shuffle mode is on, go to a random song
        if shuffleState:
            randSelect()
        else:
        #Otherwise, move on to the next song
            nextTrack(1)

    # Else, if its paused, we dont want to do anything
    elif playState == SONG_IS_PAUSED:
        pass

    # If the slider hasnt moved
    elif int(slider.get()) == int(currentDur):
        # Change text
        durLabel.config(text=f"{convCurrentDur} / {convTotLen}")
        # Change the position of the slider to the current position
        slider.config(to_=songLengthGrabber(), value=int(currentDur))

    else:
        # We need the position of the slider in time format
        sliderConv = time.strftime("%M:%S", time.gmtime(int(slider.get())))

        durLabel.config(text=f"{sliderConv} / {convTotLen}")

        # Manually move the slider
        slider.config(value=(slider.get() + 1))

    # Run this again and again after 1 second
    global secLoop
    secLoop = screen.after(1000, changeDur)


# Get length of song length
def songLengthGrabber():
    # Get file path of currently playing song
    track = trackBox.get(ACTIVE)
    track = getSongPath(track)

    # Read song length with mutagen
    songMutagen = MP3(track)
    songLength = songMutagen.info.length
    # Convert to proper format
    return songLength


# Function to change name of track
def changeName():
    currentPlaying = trackBox.get(ACTIVE)
    name = getSongName(currentPlaying)
    # If song name is longer than 32 chars, shorten it
    if len(name) > 32:
        name = name[:32] + "..."

    curTitle.configure(text=name)


# Function to stop the music
def stop():
    global playState

    #If the song is already stopped, we error handle
    if playState == SONG_NOT_PLAYING:
        return
    # Check to see if folder is empty
    if emptyFolder:
        messagebox.showerror(
            "Error: No Songs!",
            "Looks like you don't have any songs downloaded! Please download some",
        )
        return

    global secLoop

    # Stop the song in mixer
    pygame.mixer.music.stop()

    # Cancel the currently playing job
    screen.after_cancel(secLoop)

    # Change playState
    playState = SONG_NOT_PLAYING

    # Change all GUI elements
    mainBtn.configure(image=playBtnImg)
    mainBtn.photo = playBtnImg
    slider.config(value=0)
    durLabel.config(text=f"00:00")

#Functionality for shuffle button
def shuffleBtnFunc():
    global shuffleState

    #If shuffle True, set shuffle false
    if shuffleState:
        shuffleState = False
        shuffleBtn.config(image=shuffleBtnImgGray)
        #print("Shuffle Off")
    
    #If shuffle False, set shuffle ture
    else:
        shuffleState = True
        shuffleBtn.config(image=shuffleBtnImg)
        #print("Shuffle On")

#Random list box selector
def randSelect() :
    global playState
    #Get a random index value for the listbox
    #Make this not the same as current selection
    rand = random.randint(0,trackBox.size()-1)
    while rand == trackBox.curselection()[0]:
        rand = random.randint(0,trackBox.size()-1)
    #Clear current selection
    trackBox.selection_clear(0, END)
    #Set selection to our random one
    trackBox.selection_set(rand) # Set the index
    #Activate the random one
    trackBox.activate(rand)

    # Get the name of the next track, modify for file path, and update listbox selection
    playTrack = trackBox.get(rand)
    playTrack = getSongPath(playTrack)

    # Change the album cover based on the selected track
    changeCover(rand)

    # Change the current title name, current play time
    changeName()
    durLabel.config(text=f"00:00")

    #Set slider back to zero
    slider.config(value=0)

    # Cancel the currently playing job
    screen.after_cancel(secLoop)

    # Reset play state and simulate a button click to start playing the new track
    playState = 0
    mainBtnFunc(0)


# A function that controls teh working of the main play button
def mainBtnFunc(mainQuery):
    # Check to see if folder is empty
    if emptyFolder:
        messagebox.showerror(
            "Error: No Songs!",
            "Looks like you don't have any songs downloaded! Please download some",
        )
        return

    global playState, tracks

    # Copy the current play state to the local variable mainQuery
    mainQuery = playState

    # If the play state is 0 (initial or stopped)
    if playState == SONG_NOT_PLAYING:
        # Pause the music (if playing), #print a message, and get the selected track
        pygame.mixer.music.pause()
        # print("Play pressed first time")
        track = trackBox.get(ACTIVE)

        # Modify track name for file path and find its index in the tracks list
        track = getSongPath(track)
        trackIndex = tracks.index(track.replace("./music/", ""))

        #Send slider to 0
        slider.config(value=0)

        # Load and play the selected track, update play state, and change album cover
        pygame.mixer.music.load(track)
        pygame.mixer.music.play(loops=0)
        playState = SONG_IS_PLAYING
        changeCover(trackIndex)

        mainBtn.configure(image=pauseBtnImg)
        mainBtn.photo = pauseBtnImg

        # Change the current title name
        changeName()

        # Run the song duration fucntion when first played
        changeDur()

    # If the play state is 1 (playing)
    elif playState == SONG_IS_PLAYING:
        # Pause the music,
        # print a message, update play state, and change button image
        pygame.mixer.music.pause()
        playState = SONG_IS_PAUSED
        mainBtn.configure(image=playBtnImg)
        mainBtn.photo = playBtnImg

    # If the play state is 2 (paused)
    elif playState == SONG_IS_PAUSED:
        # Unpause the music, #print a message, update play state, and change button image
        pygame.mixer.music.unpause()
        playState = SONG_IS_PLAYING
        mainBtn.configure(image=pauseBtnImg)
        mainBtn.photo = pauseBtnImg


# Function to play the next or previous track
def nextTrack(move):
    # Check to see if folder is empty
    if emptyFolder:
        messagebox.showerror(
            "Error: No Songs!",
            "Looks like you don't have any songs downloaded! Please download some",
        )
        return
    try:
        # Get the index of the currently selected track in the listbox
        curTrack = trackBox.curselection()[0]
    except IndexError:
        messagebox.showerror(
            "Error: Select a song!", "You have to click on the track you want to play"
        )
        return

    # Stop the currently playing song
    stop()

    # If shuffle is on, just move to a shuffled song
    if shuffleState:
        randSelect()
        return

    global playState

    # Calculate the index of the next track based on the movement direction
    if curTrack == 0 and move == -1:
        nextTrack = trackBox.size() - 1
    elif curTrack == (trackBox.size() - 1) and move == 1:
        nextTrack = 0
    else:
        nextTrack = trackBox.curselection()[0] + move

    # Get the name of the next track, modify for file path, and update listbox selection
    playTrack = trackBox.get(nextTrack)
    playTrack = getSongPath(playTrack)

    trackBox.selection_clear(0, END)
    trackBox.activate(nextTrack)
    trackBox.selection_set(nextTrack, last=None)

    # Change the album cover based on the selected track
    changeCover(nextTrack)

    # Reset play state and simulate a button click to start playing the new track
    playState = 0
    mainBtnFunc(0)

    # Change the current title name
    changeName()


# Function to change the album cover image based on the selected track
def changeCover(trackNum):
    global curCover
    albumCover = tracks[trackNum].replace(".mp3", "")
    albumCover = f"./music/albumCover/{albumCover}-cover.jpg"
    curCover = Image.open(albumCover)
    curCover = curCover.resize((250, 250), Image.LANCZOS)
    curCover = ImageTk.PhotoImage(curCover)
    curCoverLabel.configure(image=curCover)

#Function to delete a song
def delSong():
    #Stop currently playing song
    stop()

    #Get path for song and cover
    curSelect = trackBox.curselection()
    if not curSelect:
        messagebox.showerror(
            "Select Song!",
            "You must select the song to delete it"
            )
        return

    selected = trackBox.get(curSelect[0])
    selectedPath = getSongPath(selected)

    selectedCoverPath = selectedPath.replace("./music/" , "").replace(".mp3", "")
    selectedCoverPath = f"./music/albumCover/{selectedCoverPath}-cover.jpg"

    #Delete cover, then image
    os.remove(selectedCoverPath)
    os.remove(selectedPath)

    #Change album cover
    curCover = Image.open("./sources/template.png")
    curCover = curCover.resize((250, 250), Image.LANCZOS)
    curCover = ImageTk.PhotoImage(curCover)
    curCoverLabel.configure(image=curCover)

    #Reload track list
    reloadTracks()


# Function to get song name
def getSongName(path):
    name = path.replace(".mp3", "")
    name = name.replace("_", " ")

    return name


# Function to get song path
def getSongPath(name):
    name = name.replace(" ", "_")
    path = f"./music/{name}.mp3"
    return path


# Function to get song album path
def getSongCov(name):
    path = name.replace(".mp3", "")
    path = path.replace(" ", "_")
    path = f"./music/albumCover/{path}-cover.jpg"
    return path


# slider function
def slide(pos):

    if playState != SONG_IS_PLAYING:
        pass
    else:
        track = trackBox.get(ACTIVE)
        track = getSongPath(track)
        # # Load and play the selected track, update play state, and change album cover
        pygame.mixer.music.load(track)

        curPos = slider.get()
        pygame.mixer.music.play(loops=0, start=int(curPos))
        slider.config(value=curPos)

#Open folder
def openFolder():
    print(USER_OS)
    if USER_OS==OS_LINUX:
        os.system('xdg-open "%s"' % "./music/")
    elif USER_OS==OS_WIN:
        os.startfile('.\\music')
    elif USER_OS==OS_MAC:
        pass

# Function to change color scheme
def changeColor(scheme):
    global playState
    # Change the color pallette
    # Col is for changing file path to button icons
    if scheme == "BLUE":
        bgMain = "#1A1C26"
        bgSec = "#2D2E39"
        fgMain = "#F4F4F2"
        accent = "#3498DB"
        col = "Blue"

    elif scheme == "GREEN":
        bgMain = "#19231A"
        bgSec = "#2E392A"
        fgMain = "#F2F8F2"
        accent = "#4CAF50"
        col = "Green"

    elif scheme == "RED":
        bgMain = "#1C161A"
        bgSec = "#2E2629"
        fgMain = "#EDF3FA"
        accent = "#F53C36"
        col = "Red"

    elif scheme == "PURPLE":
        bgMain = "#16181C"
        bgSec = "#27262E"
        fgMain = "#EEFAED"
        accent = "#8F36F5"
        col = "Purple"        

    # Change elements that use the background color
    for i in bgMainBgList:
        i.configure(bg=bgMain)

    # Change elements that use the foreground color
    for i in fgMainFgList:
        i.configure(fg=fgMain)

    # Change elements that use the secondary background color
    for i in bgSecBgList:
        i.configure(bg=bgSec)

    # Change elements that use the accent color
    # (not in a loop because we have to change different things)
    trackBox.configure(selectbackground=accent)
    curTitle.configure(bg=accent)

    #Change cur cover border color
    curCoverLabel.config(highlightbackground=bgSec)

    # Change the file we're using for the images (it will now default to these)
    global playBtnImg, pauseBtnImg, stopBtnImg, frontBtnImg, backBtnImg, shuffleBtnImg

    playBtnImg = PhotoImage(file=f"./sources/ctrlbtn/playBtnImg{col}.png")
    pauseBtnImg = PhotoImage(file=f"./sources/ctrlbtn/pauseBtnImg{col}.png")
    stopBtnImg = PhotoImage(file=f"./sources/ctrlbtn/stopBtnImg{col}.png")
    frontBtnImg = PhotoImage(file=f"./sources/ctrlbtn/frontBtnImg{col}.png")
    backBtnImg = PhotoImage(file=f"./sources/ctrlbtn/backBtnImg{col}.png")
    shuffleBtnImg = PhotoImage(file=f"./sources/ctrlbtn/shuffleBtnImg{col}.png")

    # Change the button images

    #If song is playing, pause button image should be used
    if playState == SONG_IS_PLAYING:
        mainBtn.configure(image=pauseBtnImg)
        #Stop Garbage collection
        mainBtn.photo = pauseBtnImg
    else:
        #Otherwise use play button
        mainBtn.configure(image=playBtnImg)
        #Stop Garbage collection
        mainBtn.photo = playBtnImg

    #if shuffle is on, change the image
    if shuffleState:
        shuffleBtn.configure(image=shuffleBtnImg)
        #Stop Garbage collection
        shuffleBtn.photo = shuffleBtnImg

    stopBtn.configure(image=stopBtnImg)
    frontBtn.configure(image=frontBtnImg)
    backBtn.configure(image=backBtnImg)

    # Stop garbage collection (if this code is not here,
    # the loaded images are deleted before they are used)
    mainBtn.photo = playBtnImg
    stopBtn.photo = stopBtnImg
    frontBtn.photo = frontBtnImg
    backBtn.photo = backBtnImg

    # Change this to new default
    defaultColor = open("./config/COLOR.txt", "r+")
    # Erase the file
    defaultColor.truncate(0)
    # Write new default
    defaultColor.write(scheme)
    defaultColor.close()


# Function to reload the track box
def reloadTracks():
    # Redefine tracks list
    global tracks
    tracks = []
    for name in os.listdir("./music"):
        if name in [".gitignore", "albumCover"]:
            continue
        tracks.append(name)
    #tracks = sorted(tracks)

    global emptyFolder
    if len(tracks) == 0:
        tracks = ["Get some songs!"]
        # This variable tracks if the directory is empty
        emptyFolder = True
    else:
        emptyFolder = False

    # Clear current trackbox
    trackBox.delete(0, "end")

    # Add everything back
    for name in tracks:
        name = name.replace(".mp3", "")
        name = name.replace("_", " ")
        trackBox.insert("end", name)

#Volume slider funtion
def volSliderFunc(x):
    vol= volSlider.get()
    pygame.mixer.music.set_volume(volSlider.get())
    #volSliderLabel.config(text=f"{int(pygame.mixer.music.get_volume()*100)}%")
    pass

#Link to github page
def openGithub():
    webbrowser.open('https://github.com/Arctican4Real/Melodia')

#Auto play capability

### UI CODE ###

# Code for main menu bar
settings = Menu(screen, bg=bgSec, fg=fgMain, bd=0)
screen.config(menu=settings)

# Code for download button on menu bar
downloadMenu = Menu(settings, bg=bgMain, fg=fgMain, bd=0,tearoff="off")
settings.add_cascade(label="Download", menu=downloadMenu)

# Button to download songs
downloadMenu.add_command(label="Get Song", command=lambda:download.downloadSong(screen))
# Button to reload the tracks
downloadMenu.add_command(label="Reload Tracks", command=reloadTracks)
# Add folder button
downloadMenu.add_command(label="Open Folder", command=openFolder)
# Delete song
downloadMenu.add_command(label="Delete Song", command=delSong)


# Code for themes button on menu bar
themeMenu = Menu(settings, bg=bgMain, fg=fgMain, bd=0, tearoff="off")
settings.add_cascade(label="Theme", menu=themeMenu)
themeMenu.add_command(label="Magma", command=lambda: changeColor("RED"))
themeMenu.add_command(label="Lush", command=lambda: changeColor("GREEN"))
themeMenu.add_command(label="Moonlit", command=lambda: changeColor("BLUE"))
themeMenu.add_command(label="Nebula", command=lambda: changeColor("PURPLE"))

#Github page link
settings.add_command(label="Github", command=openGithub)

# Frames
left_frame = Frame(screen, bg=bgMain)
left_frame.grid(row=0, column=0, padx=(10,0), pady=(10,0), sticky="nsew")

right_frame = Frame(screen, bg=bgMain)
right_frame.grid(row=0, column=1, padx=(0,10), pady=(10,0), sticky="nsew")

down_frame = Frame(screen, bg=bgMain)
down_frame.grid(row=1, column=0, padx=10, pady=0,sticky="ew",columnspan=4)

btnDiv = Frame(screen, bg=bgMain)
btnDiv.grid(row=2,column=0,padx=10,pady=10,sticky="ew",columnspan=4)

# Add weight to the rows and columns for right_frame
screen.grid_rowconfigure(0, weight=1)
screen.grid_columnconfigure(1, weight=1)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(1, weight=1)

# Create a listbox to display tracks
trackBox = Listbox(
    right_frame,
    bg=bgSec,
    fg=fgMain,
    borderwidth=0,
    highlightthickness=0,
    selectbackground=accent,
    selectborderwidth=0,
    width=30,
    activestyle="none",
    selectmode=SINGLE
)
trackBox.grid(row=0, column=0, sticky="nsew", padx=10,pady=10)

# Defualt to the first track in the listbox
trackBox.activate(0)
trackBox.selection_set(0)

# Initially load the tracks
reloadTracks()

# Load the first cover from the folder
if not emptyFolder:
    albumCover = getSongCov(trackBox.get(0))
# If the folder is empty, get default cover
else:
    albumCover = "./sources/template.png"

# volSliderLabel = Label(
#     left_frame,
#     text="100%",
#     borderwidth=0,
#     highlightthickness=0,
#     bd=0,
#     bg=bgMain,
#     fg=fgMain,
#     width=5,
#     #height=1,
#     font=("Arial", 12),
#     )
#volSliderLabel.grid(column=0, row=4, padx=(5,0),pady=5)

# Volume control Slider
volSlider = ttk.Scale(
    left_frame,
    from_=1,
    to=0,
    orient=VERTICAL,
    value=100,
    length=290,
    command=volSliderFunc
    )
s=ttk.Style()
s.configure("Vertical.TScale",sliderthickness=10)
volSlider.grid(column=0,row=0,padx=5,pady=(10,0),rowspan=2)

#Cover art
global curCover
curCover = Image.open(albumCover)
curCover = curCover.resize((250, 250), Image.LANCZOS)
curCover = ImageTk.PhotoImage(curCover)

curCoverLabel = Label(left_frame,image=curCover, borderwidth=0, highlightthickness=4, highlightbackground=bgSec, bg=bgMain)
curCoverLabel.grid(pady=10,column=1,row=0)

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

durLabel.grid(row=2,column=1, columnspan=1,pady=10)

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
slider.grid(column=3,pady=0,ipadx=10,columnspan=4)

#Only trigger the slide event when slider stops moving
slider.bind("<ButtonRelease-1>", slide)

# Text box for song length
if not emptyFolder:
    firstTrack = getSongName(trackBox.get(0))
# Default variable if no songs
else:
    firstTrack = "Welcome to Melodia!"

# Display the current song name
curTitle = Label(left_frame, text=firstTrack, bd=1, bg=accent, fg=bgMain)
curTitle.grid(row=1,column=1, ipady=0, pady=0,sticky="ew")

#Buttons

# Create control buttons
mainBtn = Button(
    btnDiv,
    image=playBtnImg,
    borderwidth=0,
    command=lambda: mainBtnFunc(playState),
    bg=bgMain,
    highlightthickness=0,
    bd=0,
    relief=SUNKEN,
    activebackground=bgSec
)
stopBtn = Button(
    btnDiv,
    image=stopBtnImg,
    borderwidth=0,
    command=stop,
    bg=bgMain,
    highlightthickness=0,
    bd=0,
    relief=SUNKEN,
    activebackground=bgSec
)
backBtn = Button(
    btnDiv,
    image=backBtnImg,
    borderwidth=0,
    command=lambda: nextTrack(-1),
    bg=bgMain,
    highlightthickness=0,
    bd=0,
    relief=SUNKEN,
    activebackground=bgSec
)
frontBtn = Button(
    btnDiv,
    image=frontBtnImg,
    borderwidth=0,
    command=lambda: nextTrack(1),
    bg=bgMain,
    highlightthickness=0,
    bd=0,
    relief=SUNKEN,
    activebackground=bgSec
)
shuffleBtn = Button(
    btnDiv,
    image=shuffleBtnImgGray,
    borderwidth=0,
    command=shuffleBtnFunc,
    bg=bgMain,
    highlightthickness=0,
    bd=0,
    relief=SUNKEN,
    activebackground=bgSec
)

# Grid layout for control buttons
backBtn.grid(row=0, column=0, padx=(10,60), pady=(0,10))
mainBtn.grid(row=0, column=1, padx=(0,60), pady=(0,10))
stopBtn.grid(row=0, column=2, padx=(0,60), pady=(0,10))
frontBtn.grid(row=0, column=3, padx=(0,60), pady=(0,10))
shuffleBtn.grid(row=0, column=4, padx=(0,10), pady=(0,10))


# A list containing elements which use saved colors
bgMainBgList = [
    screen,
    downloadMenu,
    themeMenu,
    durLabel,
    curTitle,
    btnDiv,
    mainBtn,
    stopBtn,
    backBtn,
    frontBtn,
    shuffleBtn,
    settings,
    left_frame,
    right_frame,
    down_frame,
    btnDiv,
    #volSliderLabel
]
fgMainFgList = [trackBox, settings, downloadMenu, themeMenu, durLabel]
bgSecBgList = [settings,trackBox]

# Get the default color
defaultColor = open("./config/COLOR.txt", "rt")
changeColor(defaultColor.read())
defaultColor.close()

#initiate
screen.mainloop()