To use:
1: run sudo apt install yt-dlp
2: run pip install playwright
3: run: yt-dlp --write-thumbnail --convert-thumbnails png --write-description --no-write-playlist-metafiles --recode-video mp4 <playlist url>
4: With Firefox (not sure what other browsers do this) go to the playlist on YouTube, scroll to the bottom (or at least make sure however much you want to include is loaded), then hit ctrl-S or right click to save as. In the file type, change "Web Page, complete" or "Web Page, HTML only" to "Text Files". Then change "<Playlist Name> - YouTube.html" to
"<Playlist Name> - YouTube.txt" (the file name doesn't matter but I think it does have to be a .txt)
5: Run the program. Enter Odysee login info. If it hangs while waiting for email confirmation, just go login and complete it with whatever email you use.
6: The where would you like to start/end are what part of the playlist it starts and ends at. Use it to resume if it crashes part-way through.
7: When it asks "Where is your song playlist file?", enter the full address of the file you downloaded in step 4, including the filename with .txt (See example_playlist.txt)
8: When it asks "What is the folder that your video, thumbnail,and description files located?", give it the path to the directory where you downloaded stuff in step 3.

Thumbnail Grabber:
I'm not entirely sure why, but yt-dlp seems to be a little inconsistent. E.G. while trying to get the thumbnail for for "The Decemberists - This Is Why We Fight", it repeatedly gave me a "thumbnail" which was just a frame from the video instead of the actual thumbnail. Thumbnail Grabber serves as a workaround to this by invoking https://www.youtubethumbnaildownloader.com/
With that in mind, it's not stable and only works on videos with high-res thumbnails. Use at your own risk. I will work on it some more later.

ToDo:
- Make a version with statically linked dependencies.
- Add a way to invoke yt-dlp during runtime.
- Make a version with more code abstracted into methods/functions and said methods/functions in different files.
- Maybe add a GUI.
- Maybe make a (Peek-in-Your-)Windows &/or Crapple version.
- (If anybody has a better idea for a license, let me know. I just picked the one that seemed good ¯\_(ツ)_/¯)
