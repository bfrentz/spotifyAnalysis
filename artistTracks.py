# Script for extracting information about a given artists music from spotify
# User changes artist input
# Pulls data from spotify's api, including track metadata and features 
# (like popularity, energy, danceability, tempo, etc...)
# Converts information to a dataframe and saves as a csv file

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import numpy as np
import pandas as pd
import sys

# Function for extracting songs from a given album uri ID
def albumSongs(uri):
    album = uri           # assign album uri to a given name                                       
    spotifyAlbums[album] = {}                      # dictionary (and subsequent key values) for the specific album with given uri
    spotifyAlbums[album]['album'] = []
    spotifyAlbums[album]['track_number'] = []
    spotifyAlbums[album]['id'] = []
    spotifyAlbums[album]['name'] = []
    spotifyAlbums[album]['uri'] = []

    # Pull data on album tracks
    tracks = sp.album_tracks(album)

    # Loop over tracks and append info
    for n in range(len(tracks['items'])):
        spotifyAlbums[album]['album'].append(albumNames[albumCount])
        spotifyAlbums[album]['track_number'].append(tracks['items'][n]['track_number'])
        spotifyAlbums[album]['id'].append(tracks['items'][n]['id'])
        spotifyAlbums[album]['name'].append(tracks['items'][n]['name'])
        spotifyAlbums[album]['uri'].append(tracks['items'][n]['uri'])


# Function to grab the audio features for all tracks
def audioFeatures(album):

	# Add new key values for features
    spotifyAlbums[album]['acousticness'] = []
    spotifyAlbums[album]['danceability'] = []
    spotifyAlbums[album]['energy'] = []
    spotifyAlbums[album]['instrumentalness'] = []
    spotifyAlbums[album]['liveness'] = []
    spotifyAlbums[album]['loudness'] = []
    spotifyAlbums[album]['speechiness'] = []
    spotifyAlbums[album]['tempo'] = []
    spotifyAlbums[album]['valence'] = []
    spotifyAlbums[album]['popularity'] = []

    # counter
    trackCount = 0
    for track in spotifyAlbums[album]['uri']:

    	# pulls audio features for track
        features = sp.audio_features(track)

        # Appends said features to the relevant key value
        spotifyAlbums[album]['acousticness'].append(features[0]['acousticness'])
        spotifyAlbums[album]['danceability'].append(features[0]['danceability'])
        spotifyAlbums[album]['energy'].append(features[0]['energy'])
        spotifyAlbums[album]['instrumentalness'].append(features[0]['instrumentalness'])
        spotifyAlbums[album]['liveness'].append(features[0]['liveness'])
        spotifyAlbums[album]['loudness'].append(features[0]['loudness'])
        spotifyAlbums[album]['speechiness'].append(features[0]['speechiness'])
        spotifyAlbums[album]['tempo'].append(features[0]['tempo'])
        spotifyAlbums[album]['valence'].append(features[0]['valence'])

        # popularity is stored in a different spot
        pop = sp.track(track)
        spotifyAlbums[album]['popularity'].append(pop['popularity'])

        # increment, duh
        trackCount+=1



# Accessing spotify
# Use your own credentials!
#client_id = ""
#client_secret = ""
#client_credentials_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret)
# Or set with environment variables and grab here (probably safer):
# SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET
client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


# Chosen artist
# Takes all system arguments for names with spaces
name = ' '.join(sys.argv[1:])
result = sp.search(name)

# Extracting albums
# URI is a spotify internal id (basically)
artist_uri = result['tracks']['items'][0]['artists'][0]['uri']
sp_albums = sp.artist_albums(artist_uri, album_type='album')

# Store the artist's albums' names' and uri's in separate lists
albumNames = []
albumURIs = []
for i in range(len(sp_albums['items'])):
    albumNames.append(sp_albums['items'][i]['name'])
    albumURIs.append(sp_albums['items'][i]['uri'])



# Get the songs from the albums
spotifyAlbums = {}
albumCount = 0
for i in albumURIs:
    albumSongs(i)
    print('Album ' + str(albumNames[albumCount]) + '\'s songs have been added to spotifyAlbums dictionary.')
    albumCount +=1

# output spacing
print()


# Extract audio features by looping through albums
# Introduce a random delay to avoid sending too many requests to apotify's api
requestCount = 0
startTime = time.time()
sleepMin = 3
sleepMax = 7
for i in spotifyAlbums:
    audioFeatures(i)
    requestCount+=1
    if requestCount % 5 == 0:
        print(str(requestCount) + ' albums completed.')
        time.sleep(np.random.uniform(sleepMin, sleepMax))
        print('Loop #: {}'.format(requestCount))
        print('Elapsed time: {} seconds'.format(time.time() - startTime))

# Declare dictionary for conversion to eventual dataframe
dataDict = {}
dataDict['album'] = []
dataDict['track_number'] = []
dataDict['id'] = []
dataDict['name'] = []
dataDict['uri'] = []
dataDict['acousticness'] = []
dataDict['danceability'] = []
dataDict['energy'] = []
dataDict['instrumentalness'] = []
dataDict['liveness'] = []
dataDict['loudness'] = []
dataDict['speechiness'] = []
dataDict['tempo'] = []
dataDict['valence'] = []
dataDict['popularity'] = []

# Add data to dictionary which will be turned into dataframe
for album in spotifyAlbums:
    for feature in spotifyAlbums[album]:
        dataDict[feature].extend(spotifyAlbums[album][feature])

# DEBUG
#print(len(dataDict['album']))

# Save as pandas dataframe
df = pd.DataFrame.from_dict(dataDict)

# Remove Duplicates
#print(len(df))
dfFinal = df.sort_values('popularity', ascending=False).drop_duplicates('name').sort_index()
#print(len(dfFinal))


# Save to csv
artist = '_'.join(sys.argv[1:])
outputFileName = './output/' + artist + '_data.csv'
dfFinal.to_csv(outputFileName)
print()
print('Information about ' + name + '\'s music output to ' + outputFileName + '.')
print()


