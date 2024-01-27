# Melodia
| ![Sample Image](./sources/icon.ico?raw=true "Sample Image")  | **Python based music player app.** |

## Project Description

This project aims to create a feature-rich music playing application that effectively serves as an offline mp3 player, providing users with a wide range of functionalities.The application will enable users to:
- Search and save music
- Have all features of a general MP3 player (pause, play, skip, autoplay, etc.)
- Play, Create and Edit Playlists
- Interact with the app through a mordern UI

![Sample Image](./sources/preview2.png?raw=true "Sample Image")

*Caption: Application with "Moonlit" Theme*

*Cover Art and Tracks belong to original creators*

### Specifications

To search for music, the [Deezer API](https://developers.deezer.com/) is currently being used.

To source the music, the application will directly download songs from YouTube with [pytube](https://github.com/pytube/pytube) and store them as MP3 files on the user's device.

A database system will be implemented to help with keeping track of all the songs, as well as a playlist system

The initial release will be a desktop application, with potential plans for future expansion to the Android platform.

*While an account system is not currently required, it may be implemented if we have time.* 

## ! IMPORTANT NOTE !
- The TrackSearchDownload script will not work unless you have a valid [Deezer API](https://developers.deezer.com/) key
- Please register for one, and create a ".env" file, with your own keys as variables.
- You may use ".env_sample" as a template (rename to .env afterwards)

## Current Progress

### Working On
- Button to access music folder
- Autoplay and Loop buttons

### Planned Features
- Change to a more reliable music search API key
- Create database and store more information about the Tracks
- Implement Playlists
- Implement Shuffle Play
- Add option to search both tracks or album
- Connect music GUI to Download feature
- Add secret features
- Autoplay, Themes, Loops

## Contributors
- Adeeb Rahman
- Shubham Sharma
- Nazia Kaesh

## Disclaimer
Usage Disclaimer for Melodia Music Player:

By utilizing the Melodia Music Player ("the App"), you expressly agree to the following terms:

1. *Educational/Learning Purpose:* Melodia is exclusively intended for educational and learning purposes, promoting the development of users' programming skills within the project's framework.

2. *Legal Use Requirement:* The App, equipped with downloading capabilities, is designed for lawful purposes only. Users are obligated to adhere to relevant laws and regulations in their jurisdiction. Any illicit use, including unauthorized downloading, is strictly prohibited.

3. *No Accountability for Legal Issues:* The developers of Melodia disclaim any responsibility for legal issues stemming from the App's use. Users are individually responsible for ensuring compliance with local laws and regulations.

4. *Media Ownership:* All media content played or downloaded through Melodia remains the property of its original creators. The developers assert no rights over the media and assume no responsibility for its legality or appropriateness.

Your usage of Melodia implies acknowledgment and acceptance of these terms. The developers retain the right to modify the terms at any time. Users are advised to periodically review this disclaimer for updates.
