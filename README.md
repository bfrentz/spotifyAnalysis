# spotifyAnalysis
A repository for scripts that I've written for analyzing spotify data with spotipy python library
To use, [install spotipy and follow the setup instructions.](https://spotipy.readthedocs.io/en/2.9.0/)

* artistTracks.py takes a command line argument about a particular artist and collects the data about that artist. This includes all of the albums and tracks, as well as the respective song's features as designated by spotify (i.e. dancability, energy, instrumentalness, loudness, tempo, popularity, etc.) It outputs this information to a csv file in an output directory for further analysis/work.
