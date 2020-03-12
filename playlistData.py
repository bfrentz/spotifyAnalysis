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
	song_names = []
	song_artists = []

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
		song_names.append(songs[i]['track']['name'])
		song_artists.append(songs[i]['track']['artists'][0]['name'])

	# DEBUG
	#print(song_ids)
	contents = {}
	contents['song_id'] = song_ids
	contents['title'] = song_names
	contents['artist'] = song_artists
	return contents


# Get the audio features for a track
def audioFeatures(trackID):
	"""
	Function gets the audio features for a given track
	Descriptions of the different features can be found here:
	https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

	Inputs: spotify song ID
	Output: dictionary containing audio features:
	'acousticness'
    'danceability'
    'energy'
    'instrumentalness'
    'liveness'
    'loudness'
    'speechiness'
    'tempo'
    'valence'
    'popularity'

    """

	# Store the audio features
	features = sp.audio_features(trackID)
	#DEBUG
	#print(features)
	#print(type(features[0]['tempo']))

	# Since popularity for a track is stored in a different spot, get that
	pop = sp.track(trackID)
	features[0]['trackPopularity'] = pop['popularity']
	#DEBUG
	#print(features)

	return features


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
if len(sys.argv) > 1:
    playlistID = sys.argv[1]
else:
    #print('Whoops, need to provide your username 	when calling this function!')
    #print('\nUsage: python3 userPlaylists.py [	username]')
    #sys.exit()
    print('Using default playlist.\n')
    playlistID = 'spotify:playlist:1M7TwHy1FRPtUh1CIEvyqS'

# Get playlist json data
results = sp.playlist(playlistID)

# DEBUG
# Print playlist information
print('Playlist: ', results['name'])
#print(json.dumps(results, indent=4))
#print(results['tracks']['items'][0]['track']['artists'][0]['name'])
#print(results['tracks']['items'][0]['track']['name'])
#print(results['tracks']['items'][0]['track'].keys())

# Song ids
songs = getPlaylistSongs(results)
print()
# DEBUG
#print(songs['artist'][0])

# Get all features with audioFeatures function
# Introduce a random delay to avoid sending too many requests to spotify's api
trackFeatures = {}
requestCount = 0
startTime = time.time()
sleepMin = 3
sleepMax = 7

acousticness = []
danceability = []
duration = []
energy = []
instrumentalness = []
liveness = []
loudness = []
popularity = []
speechiness = []
tempo = []
timeSignature = []
valence = []

for songID in range(len(songs['song_id'])):

    # Get features
    singleFeatures = audioFeatures(songs['song_id'][songID])

    # append features
    acousticness.append(singleFeatures[0]['acousticness'])
    danceability.append(singleFeatures[0]['danceability'])
    duration.append(singleFeatures[0]['duration_ms'])
    energy.append(singleFeatures[0]['energy'])
    instrumentalness.append(singleFeatures[0]['instrumentalness'])
    liveness.append(singleFeatures[0]['liveness'])
    loudness.append(singleFeatures[0]['loudness'])
    popularity.append(singleFeatures[0]['trackPopularity'])
    speechiness.append(singleFeatures[0]['speechiness'])
    tempo.append(singleFeatures[0]['tempo'])
    timeSignature.append(singleFeatures[0]['time_signature'])
    valence.append(singleFeatures[0]['valence'])

    #trackFeatures.append(singleFeatures)
    requestCount += 1
    if requestCount % 5 == 0:
        print(str(requestCount) + ' songs completed.')
        time.sleep(np.random.uniform(sleepMin, sleepMax))
        print('Loop #: {}'.format(requestCount))
        print('Elapsed time: {} seconds'.format(time.time() - startTime))

# Normalized tempo
maxTempo = 0
for time in tempo:
	if time > maxTempo:
		maxTempo = time

# Create dictionary
songs['acousticness'] = acousticness
songs['danceability'] = danceability
songs['duration'] = duration
songs['energy'] = energy
songs['instrumentalness'] = instrumentalness
songs['liveness'] = liveness
songs['loudness'] = loudness
songs['popularity'] = popularity
songs['speechiness'] = speechiness
songs['tempo'] = tempo
songs['tempoNormalized'] = [x/maxTempo for x in tempo]
songs['timeSignature'] = timeSignature
songs['valence'] = valence


# DEBUG
print()
print()
#print(songs)

# Save as pandas dataframe
df = pd.DataFrame.from_dict(songs)
# DEBUG
print(df)

# Remove Duplicates
print(len(df))
#dfFinal = df.sort_values('popularity', ascending=False).drop_duplicates('title').sort_index()
#print(len(dfFinal))
#print()
#print(dfFinal)

# Write out
name = '_'.join(results['name'].split()) # replace spaces with underscores
name = name.replace(',', '') # removes commas
outputFileName = './data/playlists/' + name + '_data.csv'
df.to_csv(outputFileName)
print()
print('Information about ' + name + ' playlist\'s music output to ' + outputFileName + '.')
print()