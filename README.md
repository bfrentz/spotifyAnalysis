# spotifyAnalysis
A repository for scripts that I've written for analyzing spotify data with spotipy python library. To use, [install spotipy and follow the setup instructions.](https://spotipy.readthedocs.io/en/2.9.0/)

* `artistTracks.py` takes a command line argument about a particular artist and collects the data about that artist. This includes all of the albums and tracks, as well as the respective song's features as designated by spotify (i.e. dancability, energy, instrumentalness, loudness, tempo, popularity, etc.). The script outputs this information to a csv file in an output directory for further analysis/work. Can also be used by running the `runArtists.sh` script, which reads all artists from the text file and runs the script for each. The text file of all artists is contained in `./data/artists/artists.txt.`

* `playlistData.py` takes a command line argument for a particular playlist ID (URI) from spotify and collects all data about the tracks comprising that playlist. The script outputs this information to a csv file in the output directory. Can also be used by running the `runPlaylists.sh` script, which reads all the playlist ID's from a text file and runs the script for each. The text file of all playlists is contained in `./data/playlists/playlists.txt.`

* `playlistAnalyzer.ipnb` is a jupyter notebook that is used to test some analysis concepts and (obviously) analyze playlist data. Still a work in progress.

* `userPlaylists.py` is an interactive script that takes a user's information and outputs information about their playlists to the terminal.


