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

# Custom file that has passcode for API
from passcode import *

# Log into deezer with our app id (username) and password(app secret)
client = deezer.Client(
    app_id=app_id,
    app_secret=app_secret,
    # This is so results are in English only
    headers={"Accept-Language": "en"},
)

# Ask for artist
artist = input("Which artist? : ")

# Use deezer to search for this artist
deezerArtist = client.search_artists(artist)[0]

print(f"Looking for songs by {deezerArtist.name} ...")

print()
print()

# Get the top tracks from the API (returns JSON format list)
topTracks = deezerArtist.tracklist
print(topTracks)
topTracksSearch = requests.get(topTracks, headers={"Accept-Language": "en"})

# Convert that JSON file to Python Dictionary so we can work with it
topTracksSearchJson = json.loads(topTracksSearch.text)


# Print the title of the first 20 songs from that list (list gives total 50 songs)
counter = 0
print("Here are the top 20 songs, please select one : ")

for entry in topTracksSearchJson["data"]:
    if counter >= 20:
        break

    print(str(counter + 1), end=" : ")
    # This line prints the title
    print(entry["title"])
    counter += 1

# Ask the user which tracks they want, and select it
chosenTrack = int(input("Which song? : ")) - 1
chosenTrack = topTracksSearchJson["data"][chosenTrack]

print(f"You have chosen {chosenTrack['title']}")

# Search for the Artist + Song Name + "Audio" on youtube with pytube
# Example - "Avicii Waiting for love audio" is searched
searchList = Search(
    str(chosenTrack["title"] + str(chosenTrack["artist"]["name"])) + "audio"
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
path = "./Downloads/" + str(chosenTrack["title"]).replace(" ", "_")

# This is the song name and artist name, replacing spaces with underscores
songName = str(chosenTrack["title"]).replace(" ", "_")
artistName = str(chosenTrack["artist"]["name"]).replace(" ", "_")

# Make the folder
os.mkdir(path)

print("Downlading song...")

# Use the link we found before to download the video at lowest resolution (we only need audio) to the folder
target = YouTube(finalLink)

# This downloads the MP4 file inside the folder we made
target.streams.filter(file_extension="mp4").first().download(
    path, filename=songName + ".mp4"
)
print("Done!")

# This is a function to turn MP4 files into just audio MP3 files
def mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()


# This will convert our MP4 to MP3 using that function
mp4_to_mp3(f"{path}/{songName}.mp4", f"{path}/{artistName}-{songName}.mp3")

# Delete the original file to save on space
os.remove(f"{path}/{songName}.mp4")

# These two lines get the cover art of the album from the API, and download it to our folder
coverImg = chosenTrack["album"]["cover_big"]
# This will save the cover image as "./Downloads/ARTISTNAME-SONGNAME-COVER.jpg"
# Example - ./Downloads/Avicii-Waiting_for_love-cover.jpg
urllib.request.urlretrieve(coverImg, f"{path}/{artistName}-{songName}-cover.jpg")

print("Downloading complete!")

# This asks the user if they want to play the song
playQue = input("Play song? (y/n) : ").lower()
if playQue == "y":
    # If yes, we use their web browser (chrome, firefox, edge etc.) to play the mp3 file
    webbrowser.open(f"{path}/{artistName}-{songName}.mp3")
else:
    pass
