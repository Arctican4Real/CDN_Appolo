# Melodia

**Python based music player app.**

## Project Description

This project aims to create a feature-rich music streaming application that effectively serves as an offline mp3 player, providing users with a wide range of functionalities.The application will enable users to:
- Search and save music
- Have all features of a general MP3 player (pause, play, skip, autoplay, etc.)
- Play, Create and Edit Playlists
- Interact with the app through a mordern UI

![Sample Image](./sources/sample.png?raw=true "Sample Image")
*Application with "Nebula" Theme*

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
By accessing and using the Melodia Music Player ("the App"), you agree to the following terms:

- **Educational/Learning Purposes Only**: Melodia is intended for educational and learning purposes, including the developers' own learning experiences. Users are encouraged to explore and develop their programming skills within the context of this project.

- **Legal Use Only**: The App is designed for legal purposes only. Users must abide by applicable laws and regulations in their jurisdiction when using the App. Any illegal use is strictly prohibited.

- **No Responsibility for Legal Issues**: The developers of Melodia are not responsible for any legal issues arising from the use of the App. Users are solely responsible for ensuring their compliance with local laws and regulations.

- **Media Ownership**: All media content played through Melodia belongs to their original creators. The developers of Melodia do not claim any rights over the media and assume no responsibility for the legality or appropriateness of the content.

By using Melodia, you acknowledge and accept these terms. The developers reserve the right to modify the terms of use at any time. Users are advised to review this disclaimer periodically for any updates.
