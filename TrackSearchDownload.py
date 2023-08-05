import deezer
import webbrowser
import json
import requests
from pytube import YouTube
from pytube import Search
from moviepy.editor import *
import shutil
import urllib
from passcode import *

client = deezer.Client(
    app_id= app_id,
    app_secret= app_secret,
    headers={"Accept-Language": "en"},
)

artist = input("Which artist? : ")


deezerArtist = client.search_artists(artist)[0]

print(f"Looking for songs by {deezerArtist.name} ...")

print()
print()

topTracks = deezerArtist.tracklist
print(topTracks)
topTracksSearch = requests.get(topTracks, headers={"Accept-Language": "en"})


topTracksSearchJson = json.loads(topTracksSearch.text)


counter = 0
print("Here are the songs, please select one : ")

for entry in topTracksSearchJson["data"]:
    print(str(counter + 1), end=" : ")
    print(entry["title"])
    counter += 1


chosenTrack = int(input("Which song? : ")) - 1
chosenTrack = topTracksSearchJson["data"][chosenTrack]

print(f"You have chosen {chosenTrack['title']}")


searchList = Search(str(chosenTrack["title"]  + str(chosenTrack["artist"]["name"])) + "audio")
firstResult = str(searchList.results[0])
vidID = firstResult.split("=")[1].replace(">", "")
finalLink = "https://www.youtube.com/watch?v=" + vidID


path = "./Downloads/" + str(chosenTrack["title"]).replace(" ", "_")

os.mkdir(path)

print("Downlading song...")
# Download the video at lowest rez to the folder
target = YouTube(finalLink)
songName = str(chosenTrack["title"]).replace(" ", "_")
artistName = str(chosenTrack["artist"]["name"]).replace(" ", "_")
target.streams.filter(file_extension="mp4").first().download(
    path, filename=songName + ".mp4"
)
print("Done!")

# Code from Stack Overflow for conversion
def mp4_to_mp3(mp4, mp3):
    mp4_without_frames = AudioFileClip(mp4)
    mp4_without_frames.write_audiofile(mp3)
    mp4_without_frames.close()


# convert
mp4_to_mp3(f"{path}/{songName}.mp4", f"{path}/{artistName}-{songName}.mp3")

# Delete the original File
os.remove(f"{path}/{songName}.mp4")
# print(chosenTrack['album']['id'])

coverImg = chosenTrack["album"]["cover_big"]
urllib.request.urlretrieve(coverImg, f"{path}/{artistName}-{songName}-cover.jpg")

print("Downloading complete!")

playQue = input("Play song? (y/n) : ").lower()
if playQue == "y" : 
    webbrowser.open(f"{path}/{artistName}-{songName}.mp3")
else : 
    pass
