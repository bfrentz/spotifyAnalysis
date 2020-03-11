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
results = sp.playlist(playlistID)

# DEBUG
# Print playlist information
#print(json.dumps(results, indent=4))
print(results.keys())