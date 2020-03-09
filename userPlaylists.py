# Show's a users playlists in terminal and their respective contents as decied via prompt
# Needs to be authenticated via oauth

import sys
import spotipy
import spotipy.util as util

# showTracks function to print the track names inside the playlist
def showTracks(results):
	for i, item in enumerate(results['items']):
		track = item['track']
		print(
			"  %d %32.32s %s" % (i, track['artists'][0]['name'], track['name']))



# Main implementation
if __name__ == '__main__':
	# Get username
	if len(sys.argv) > 1:
		username = sys.argv[1]
	else:
		#print('Whoops, need to provide your username 	when calling this function!')
		#print('\nUsage: python3 userPlaylists.py [	username]')
		#sys.exit()
		print('Using default username for Bryce Frentz')
		username = '128455376'

	# Get oauth token
	# Follow instructions to authenticate for account
	token = util.prompt_for_user_token(username)

	# Successful authorization
	if token:
		# Spotify instance
		sp = spotipy.Spotify(auth=token)

		# Get user playlists
		playlists = sp.user_playlists(username)
		# DEBUG
		#print(playlists['items'])#.keys())
		
		# Print playlists
		for playlist in playlists['items']:
			print(playlist['name'])

		listContents = True
		examine = True
		while examine:
			prompt = input('\nWould you like to see the contents of one of these playlists? (0 = No, 1 = Yes)\n')

			if prompt == '1':
				# Get Name
				plName = input('\nWhat playlist?\n')

				for playlist in playlists['items']:
					if playlist['name'] == plName:
						print('\n'+playlist['name']+':\n')
						print('    total tracks: ', playlist['tracks']['total'])
						results = sp.playlist(playlist['id'], fields='tracks,next')
						tracks = results['tracks']
						showTracks(tracks)
						while tracks['next']:
							tracks = sp.next(tracks)
							showTracks(tracks)

			elif prompt == '0':
				examine = False

			else:
				#print('DEBUG: ' + prompt)
				#print('DEBUG: type: ', type(prompt))
				print('Not a valid response. Try again.\n')


		print('\nThank you, have a nice day.\n')
		sys.exit()





	# Unsuccessful authorization and exit
	else:
		print('Can\'t get token for that username.')
		sys.exit()





	
	