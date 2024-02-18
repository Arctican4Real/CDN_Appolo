# Song search API wrapper
import deezer
# Access to Web browser
import webbrowser
# To conver JSON files
import json
# To open URLs
import requests
# To download form youtube
from pytube import YouTube
# To search youtube
from pytube import Search
# To convert MP4 to MP3
from moviepy.editor import *
# To make folders
import shutil
# To download images
import urllib
# Accessing API password
import os
from dotenv import load_dotenv

# Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *

# Library for adding cover art to mp3
import eyed3
from eyed3.id3.frames import ImageFrame


# Get the App id and app secret
try:
    load_dotenv()
    app_id = os.environ["APP_ID"]
    app_secret = os.environ["APP_SECRET"]
except KeyError:
    print("FATAL ERROR :")
    print("Uh Oh! You don't have an API key, so I can't access Deezer!")
    print("Did you get a env file with API keys")
    raise SystemExit(0)

# Log into deezer with our app id (username) and password(app secret)
client = deezer.Client(
    app_id=app_id,
    app_secret=app_secret,
    # This is so results are in English only
    headers={"Accept-Language": "en"},
)

# This is a function to turn MP4 files into just audio MP3 files
def mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()


# This function modifies the mp3 to add album cover art
def addAlbumCover(audio, image, title, albumName, artist):
    audiofile = eyed3.load(audio)
    if audiofile.tag == None:
        audiofile.initTag()

    audiofile.tag.images.set(3, open(image, "rb").read(), "image/jpeg")

    audiofile.tag.save()

    audiofile.tag.title = title
    audiofile.tag.album = albumName
    audiofile.tag.album_artist = artist

    audiofile.tag.save(version=eyed3.id3.ID3_V2_3)


def download_button_clicked():
    status_bar.config(text=f"Finding Track...")
    ws.update_idletasks()

    global deezerTrack

    # Get currently selected song
    chosenIndex = results_listbox.curselection()[0]
    chosenTrack = deezerTrack[chosenIndex]

    # This is the song name and artist name, replacing spaces with underscores, and replace the /
    songName = chosenTrack.title_short.replace(" ", "_").replace("/", "-")
    artistName = chosenTrack.artist.name.replace(" ", "_").replace("/", "-")
    # This is the song name and artist name, replacing spaces and slashes with underscores
    songName = chosenTrack.title_short.replace(" ", "_").replace("/", "_")
    artistName = chosenTrack.artist.name.replace(" ", "_").replace("/", "_")

    # Search for the Artist + Song Name + "Audio" on youtube with pytube
    # Example - "Avicii Waiting for love audio" is searched
    searchList = Search(songName + artistName + " audio")
    # Get the first video from search result
    firstResult = str(searchList.results[0])

    status_bar.config(text=f"Getting Song...")
    ws.update_idletasks()

    # These two lines get the video id, and uses that to make the link
    # Basically, get the link
    vidID = firstResult.split("=")[1].replace(">", "")
    finalLink = "https://www.youtube.com/watch?v=" + vidID

    # This is a path to the folder where our song will be saved
    # It names the folder the title of the song, replacing spaces with underscores
    # Example - "Waiting_for_love"
    path = "./music/"  # + str(chosenTrack["title"]).replace(" ", "_")

    # Make the folder
    # os.mkdir(path)
    status_bar.config(text=f"Downloading song...")
    ws.update_idletasks()

    # Use the link we found before to download the video at lowest resolution (we only need audio) to the folder
    target = YouTube(finalLink)

    # This downloads the MP4 file inside the folder we made
    target.streams.filter(file_extension="mp4").first().download(
        path, filename=songName + ".mp4"
    )

    status_bar.config(text=f"Changing files to MP3...")
    ws.update_idletasks()
    # This will convert our MP4 to MP3 using that function
    mp4_to_mp3(f"{path}/{songName}.mp4", f"{path}/{artistName}-{songName}.mp3")

    # Delete the original file to save on space
    os.remove(f"{path}/{songName}.mp4")

    # These two lines get the cover art of the album from the API, and download it to our folder
    coverImg = chosenTrack.album.cover_big

    status_bar.config(text=f"Getting cover image...")
    ws.update_idletasks()
    # This will save the cover image as "./Downloads/ARTISTNAME-SONGNAME-COVER.jpg"
    # Example - ./Downloads/Avicii-Waiting_for_love-cover.jpg
    urllib.request.urlretrieve(
        coverImg, f"{path}/albumCover/{artistName}-{songName}-cover.jpg"
    )

    # Change the cover art of the mp3
    audio = f"{path}/{artistName}-{songName}.mp3"
    image = f"{path}/albumCover/{artistName}-{songName}-cover.jpg"
    addAlbumCover(
        audio,
        image,
        chosenTrack.title_short,
        chosenTrack.album.title,
        chosenTrack.artist.name,
    )

    status_bar.config(text=f'Downloading Complete! Click "Reload Tracks" on main menu')


def searchButton():
    status_bar.config(text=f"Searching...")
    ws.update_idletasks()
    # Ask for artist
    query = modify.get()

    # Error handling for empty
    if len(query) == 0:
        return

    # Use deezer to search for this artist
    global deezerTrack
    deezerTrack = client.search(query)

    # Clear listbox
    results_listbox.delete(0, "end")

    cunt = 0
    for result in deezerTrack:
        # Limiting searches to top 50 results
        if cunt >= 50:
            break
        results_listbox.insert(
            "end", str(cunt + 1) + ". " + result.title_short + "-" + result.artist.name
        )
        cunt += 1

    status_bar.config(text=f'Showing results for "{query}"')
    ws.update_idletasks()


# This is the code for our new window
def downloadSong(main):
    # Generate scheme
    defaultColor = open("./config/COLOR.txt", "rt")
    scheme = defaultColor.read()
    defaultColor.close()

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

    # Create main window
    global ws
    ws = tk.Toplevel(main)
    ws.title("Download Song")
    # Set the geometry of the main window (width x height)
    ws.geometry("510x325")
    ws.resizable(0, 0)
    ws.configure(bg=bgMain)

    # Create a StringVar to hold the text input value
    text = tk.StringVar()

    # Create a frame to hold other widgets
    Frm = tk.Frame(ws)

    # Configure the column weights of the main window to manage space distribution
    ws.columnconfigure(0, weight=1)
    ws.columnconfigure(1, weight=1)
    ws.columnconfigure(2, weight=1)
    # Create an entry widget for text input, linked to the text StringVar
    global modify
    modify = tk.Entry(
        ws,
        textvariable=text,
        bg=bgSec,
        fg=fgMain,
        bd=0,
        highlightcolor=fgMain,
        highlightthickness=1,
    )
    # Text entry box and Submit button in the same row
    modify_label = tk.Label(
        ws,
        text="Search : ",
        borderwidth=0,
        bg=bgMain,
        fg=fgMain,
        highlightthickness=0,
        bd=0,
    )
    modify_label.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)
    modify.grid(row=0, column=1, pady=10, padx=10, sticky=tk.E)
    modify.focus()

    # Create a button that will call the find function when pressed
    buttn = tk.Button(
        ws,
        text="Search",
        borderwidth=0,
        bg=accent,
        fg=bgMain,
        highlightthickness=0,
        bd=0,
        command=searchButton,
    )

    # Place the button in the grid layout
    buttn.grid(column=2, row=0, padx=5, pady=5)

    global results_listbox
    results_listbox = tk.Listbox(
        ws,
        selectmode=tk.SINGLE,
        bg=bgSec,
        fg=fgMain,
        borderwidth=0,
        highlightthickness=0,
        selectbackground=accent,
        selectborderwidth=0,
    )

    results_listbox.grid(
        row=1, column=0, columnspan=3, pady=10, padx=10, sticky=tk.W + tk.E
    )

    scrollbar = tk.Scrollbar(ws, orient=tk.VERTICAL, command=results_listbox.yview)
    scrollbar.grid(row=1, column=4, pady=10, padx=10, sticky=tk.W + tk.N + tk.S)
    results_listbox.config(yscrollcommand=scrollbar.set)
    contacts = []

    # Download button
    download_button = tk.Button(
        ws,
        text="Download",
        command=download_button_clicked,
        borderwidth=0,
        bg=accent,
        fg=bgMain,
        highlightthickness=0,
        bd=0,
    )
    download_button.grid(row=2, pady=10, columnspan=4)

    # Status bar at the bottom
    global status_bar
    status_bar = tk.Label(
        ws,
        text="Download Something!",
        bd=1,
        relief=tk.SUNKEN,
        anchor=tk.W,
        borderwidth=0,
        fg=fgMain,
        bg=bgSec,
    )
    status_bar.grid(row=3, columnspan=5, sticky="ew", padx=5, pady=5)

    ws.mainloop()