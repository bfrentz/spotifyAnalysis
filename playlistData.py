# Script for extracting and saving information about a given
# spotify playlist.
#
# User changes artist input
# Pulls data from spotify's api, including track metadata and features 
# (like popularity, energy, danceability, tempo, etc...)
# Converts information to a dataframe and saves as a hdf5 file

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import numpy as np
import pandas as pd
import sys
import io
import json


# Get the id's for every song in the playlist
def getPlaylistSongs(playlist):

	# Song id's
	song_ids = []

	# How many songs?
	print('total tracks in playlist: ' + str(playlist['tracks']['total']))

	# Since we can only access 100 at a time, work around it like this by copying the data to new lists
	tracks = playlist['tracks']
	songs = tracks['items']
	while tracks['next']:
		# iterate over playlist
		tracks = sp.next(tracks)

		for item in tracks['items']:
			songs.append(item)

	# Get ids
	for i in range(len(songs)):
		# DEBUG
		#print('Added song number ', i, ' from playlist.')
		song_ids.append(songs[i]['track']['id'])

	# DEBUG
	#print(song_ids)

	return song_ids


# Accessing spotify
# Use your own credentials!
#client_id = ""
#client_secret = ""
#client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
# Or set with environment variables and grab here (probably safer):
# SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Playlist URI
playlistID = 'spotify:playlist:1M7TwHy1FRPtUh1CIEvyqS'

# Get playlist json data
results = sp.playlist(playlistID)

# DEBUG
# Print playlist information
#print(json.dumps(results, indent=4))
#print(results.keys())
#print(results['tracks']['items'][0]['track']['id'])


getPlaylistSongs(results)