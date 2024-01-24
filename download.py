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

#Tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter.ttk import *


# Get the App id and app secret
try :
    load_dotenv()
    app_id=os.environ["APP_ID"]
    app_secret=os.environ["APP_SECRET"]
except KeyError:
    print("FATAL ERROR :")
    print("Uh Oh! You don't have an API key, so I can't access Deezer!")
    print("Did you copy passcode.py into the main folder?")
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

def submit_button_clicked():
    #status_bar.config(text=f"Working")

    # Ask for artist
    artist = modify.get()

    #Error handling for empty
    if len(artist) == 0:
        return

    # Use deezer to search for this artist
    deezerArtist = client.search_artists(artist)[0]

    #status_bar.config(text=f"Showing songs by {deezerArtist.name} ...")
    

    # Get the top tracks from the API (returns JSON format list)
    topTracks = deezerArtist.tracklist
    topTracksSearch = requests.get(topTracks, headers={"Accept-Language": "en"})

    # Convert that JSON file to Python Dictionary so we can work with it
    global topTracksSearchJson
    topTracksSearchJson = json.loads(topTracksSearch.text)

    if len(topTracksSearchJson)==0:
        messagebox.showerror(
            "No Songs!",
            "Looks like this artist doesn't exist in our registry :(",
        )

    #Clear listbox
    results_listbox.delete(0,'end')
    #Enter into
    for entry in topTracksSearchJson["data"]:
        # This line prints the title
        results_listbox.insert("end",entry["title"])


def download_button_clicked():
    #status_bar.config(text=f"Downloading...")

    global topTracksSearchJson
    # Ask the user which tracks they want, and select it
    index = results_listbox.curselection() 
    if not topTracksSearchJson and not index:
        return

    chosenTrack = topTracksSearchJson["data"][index[0]] 

    # Search for the Artist + Song Name + "Audio" on youtube with pytube
    # Example - "Avicii Waiting for love audio" is searched
    searchList = Search(
        str(chosenTrack["title"] + str(chosenTrack["artist"]["name"])) + " audio"
    )
    # Get the first video from search result
    firstResult = str(searchList.results[0])

    # These two lines get the video id, and uses that to make the link
    # Basically, get the link
    vidID = firstResult.split("=")[1].replace(">", "")
    finalLink = "https://www.youtube.com/watch?v=" + vidID

    # This is a path to the folder where our song will be saved
    # It names the folder the title of the song, replacing spaces with underscores
    # Example - "Waiting_for_love"
    path = "./music/" #+ str(chosenTrack["title"]).replace(" ", "_")

    # This is the song name and artist name, replacing spaces with underscores
    songName = str(chosenTrack["title"]).replace(" ", "_")
    artistName = str(chosenTrack["artist"]["name"]).replace(" ", "_")

    # Make the folder
    # os.mkdir(path)

    #status_bar.config(text=f"Downloading song...")

    # Use the link we found before to download the video at lowest resolution (we only need audio) to the folder
    target = YouTube(finalLink)

    #status_bar.config(text=f"Converting to MP3")
    # This downloads the MP4 file inside the folder we made
    target.streams.filter(file_extension="mp4").first().download(
        path, filename=songName + ".mp4"
    )

    # This will convert our MP4 to MP3 using that function
    mp4_to_mp3(f"{path}/{songName}.mp4", f"{path}/{artistName}-{songName}.mp3")

    # Delete the original file to save on space
    os.remove(f"{path}/{songName}.mp4")

    # These two lines get the cover art of the album from the API, and download it to our folder
    coverImg = chosenTrack["album"]["cover_big"]
    # This will save the cover image as "./Downloads/ARTISTNAME-SONGNAME-COVER.jpg"
    # Example - ./Downloads/Avicii-Waiting_for_love-cover.jpg
    urllib.request.urlretrieve(coverImg, f"{path}/albumCover/{artistName}-{songName}-cover.jpg")

    #status_bar.config(text=f"Downloading Complete! Click \"Reload Tracks\" on main menu")

def OnDoubleClick(event):
        item = tree.selection()[0]
        chosenTrack =item

#This is the code for our new window
def downloadSong(main):
    #Generate scheme
    defaultColor = open("./config/COLOR.txt", "rt")
    scheme = defaultColor.read()
    defaultColor.close()

    if scheme == "BLUE":
        bgMain = "#171D1C"
        bgSec = "#252D2D"
        fgMain = "#F9F9ED"
        accent = "#3695F5"
        col = "Blue"

    elif scheme == "GREEN":
        bgMain = "#1B1C16"
        bgSec = "#2B2E26"
        fgMain = "#FAEDF6"
        accent = "#56F536"
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
    ws = tk.Toplevel(main)
    ws.title("Search and Retrieve Application")
    # Set the geometry of the main window (width x height)
    # ws.geometry("690x690")
    ws.configure(bg=bgMain)
    artist=" "

    # Create a StringVar to hold the text input value
    text = tk.StringVar()

    # Create a frame to hold other widgets
    Frm = tk.Frame(ws)

    # Configure the column weights of the main window to manage space distribution
    ws.columnconfigure(0, weight=1)
    ws.columnconfigure(1, weight=1)
    ws.columnconfigure(2, weight=1)
    # Create a label for the search input

    search_label = tk.Label(ws,text="Artist Name:  ", bg=bgMain,fg=fgMain,)
    # Place the search label in the grid layout
    search_label.grid(column=0, row=2, padx=5, pady=5)

    # Text entry box and Submit button in the same row
    global modify
    modify = tk.Label(ws, text="Type artist name",
        borderwidth=0,
        bg=bgMain,
        fg=fgMain,
        highlightthickness=0,
        bd=0,)
    modify.grid(row=0, column=0, pady=10, padx=10, sticky=tk.E)

    # Create an entry widget for text input, linked to the text StringVar
    modify = tk.Entry(ws, textvariable=text,bg=bgMain, fg=fgMain)
    # Place the entry widget in the grid layout and set focus
    modify.grid(column=1, row=2, padx=5, pady=5)
    modify.focus()

    # Create a label to display output
    output_label = tk.Label(text=" ")
    # Place the output label in the grid layout
    output_label.grid(column=0, row=3)

    # # Define the function to be called when the search button is pressed
    # def find():
    #                 output_label.config(text=text.get())
    #                 search_label = tk.Label(text="Artist Name:  ")
    #                 output_label.config(text=" ")
    #                 # Remove any previous 'found' tag from the output label
        
    # Create a button that will call the find function when pressed
    buttn = tk.Button(ws, text='Search', bd='5', command=submit_button_clicked)
    # Place the button in the grid layout
    buttn.grid(column=2, row=2, padx=5, pady=5)
    columns = ('Song_Name', 'Artist')


    # Download button
    download_button = tk.Button(
        ws, text="Download", command=download_button_clicked,
        borderwidth=0,
        bg=accent,
        fg=bgMain,
        highlightthickness=0,
        bd=0,)
    download_button.grid(row=0, column=3, columnspan=3, pady=10, padx=10)
    # tree = ttk.Treeview(ws, columns=columns, show='headings')
    # tree.heading('Song_Name', text='Song Name')
    # tree.heading('Artist', text='Artist')
    global results_listbox
    results_listbox = tk.Listbox(
        ws, 
        selectmode=tk.SINGLE,
        bg=bgSec,
        fg=fgMain,
        borderwidth=0,
        highlightthickness=0,
        selectbackground=accent,
        selectborderwidth=0)
    results_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W+tk.E)

    scrollbar = tk.Scrollbar(ws, orient=tk.VERTICAL, command=results_listbox.yview)
    scrollbar.grid(row=1, column=2, pady=10, padx=10, sticky=tk.W+tk.N+tk.S)
    results_listbox.config(yscrollcommand=scrollbar.set)
    contacts=[]

    # results_listbox.bind("<Double-1>", submit_button_clicked)
    #for key in json.loads["data"]:
    #                contacts.append((f'{key}', f'{artist}'))
    # tree.bind("<Double-1>", OnDoubleClick)
    # tree.grid(column=2, row=3, padx=5, pady=5)

    # Start the main loop of the application
    ws.mainloop()

    # global modify
    # modify = tk.Entry(newWindow, borderwidth=0,bg=bgSec,fg=fgMain)
    # modify.grid(row=0, column=1, pady=10, padx=10, sticky=tk.W)

    # submit_button = tk.Button(newWindow, text="Submit", command=submit_button_clicked,
    #     borderwidth=0,
    #     bg=accent,
    #     fg=bgMain,
    #     highlightthickness=0,
    #     bd=0,)
    # submit_button.grid(row=0, column=2, pady=10, padx=10, sticky=tk.W)

    # # Listbox with scrollbar
    # global results_listbox
    # results_listbox = tk.Listbox(
    #     newWindow, 
    #     selectmode=tk.SINGLE,
    #     bg=bgSec,
    #     fg=fgMain,
    #     borderwidth=0,
    #     highlightthickness=0,
    #     selectbackground=accent,
    #     selectborderwidth=0)
    # results_listbox.grid(row=1, column=0, columnspan=2, pady=10, padx=10, sticky=tk.W+tk.E)

    # scrollbar = tk.Scrollbar(newWindow, orient=tk.VERTICAL, command=results_listbox.yview)
    # scrollbar.grid(row=1, column=2, pady=10, padx=10, sticky=tk.W+tk.N+tk.S)
    # results_listbox.config(yscrollcommand=scrollbar.set)

    # # Status bar at the bottom
    # global status_bar
    # status_bar = tk.Label(newWindow, text="Download Something!", bd=1, relief=tk.SUNKEN, anchor=tk.W, borderwidth=0, fg=fgMain, bg=bgSec)
    # status_bar.grid(row=3, column=0, columnspan=3, sticky=tk.W+tk.E, padx=5,pady=5)

    # # Run the application
    # newWindow.mainloop()