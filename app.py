from spot import Spot
from flask import Flask, request
from threading import Timer

HOST_IP_ADDRESS = 'localhost'
HOST_PORT = '8080'

# You may change this if you add other functiality
SCOPE = 'playlist-modify-private playlist-modify-public'

'''
Add yours here!
You can find these in your Developer Dashboard under your app's settings.
'''
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:8080/callback'

# You use this object to make your requests to the API (Spotify databases)
spot = Spot(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI)

# CAN BE NAMED ANYTHING
app = Flask('NAME ME')

def start():
    spot.authorize(SCOPE)



'''
STEPS BEGIN IN THE FOLLOWING FUNCTION
'''


# this is what will run when you authenticate the user
@app.route('/callback', methods=['POST', 'GET'])
def callback():
    code = request.args.get('code')
    credentials = spot.get_token(code)
    spot.ACCESS_TOKEN = credentials['access_token']

    print('\nAuthenticated and ready to go!\n')
    spot.close_browser()

    ''' 
    You do not need to follow these steps exactly but if you choose to
    follow them, you will need to change how it is implemented a little bit
    to work for the challenge

    Even though you won't need to change the functions we give you, you will
    need to look at how they are defined to make them work for you

    NOTE: look at the numbers and strings you give to the functions

    NOTE: To use the sample code below remmove the # at the beginning of the line

    If you want to add something new go for it!
    '''

    # Step 1: choose whether you want the user to choose an artist or specific songs
    # Step 2: regardless of which you choose, get the songs for the playlist

    # If you want to let them choose an artist:
    # artist = get_artist()
    # songs = get_artist_songs(artist, count=1)

    # If you want to let them choose specific songs
    # names = get_song_names(1)
    # songs = []
    # for i in range(1):
    #     songs.append(get_song(names[i]))

    # Step 3: add the songs to a playlist
    # make_playlist(songs, playlist_name='CHANGE ME')

    return 'Success'





'''
Functions to help your implementation!
Feel free to add more!!!
'''

# Getting user input for an artist
def get_artist():
    q1 = 'What is your favorite artist? '
    artist = input(q1)

    return artist

# Getting user input for a number of songs
def get_song_names(count):
    song_names = []

    while len(song_names) < count:
        prompt = f'Enter song name and artist #{len(song_names)+1} '
        song_names.append(input(prompt))

    return song_names

# Getting a song and returns the song's identifier
def get_song(song = 'Titi Me Pregunto Bad Bunny'):
    endpoint = 'https://api.spotify.com/v1/search?'

    # check the api documentation for the expected parameters and what they mean
    params = {
        'q':f'{song}', 
        'type':'track', 
        'limit':1
    }

    response = spot.GET(endpoint, params)

    # check that we have data
    if len(response['tracks']['items']) == 0:
        print('Failed to fetch song')

    track = response['tracks']['items'][0]
    track_uri = track['uri'] # adding tracks uses uri

    return track_uri


# Getting an artist's songs
def get_artist_songs(artist, count=10):
    song_uris = set()

    # Making request to search endpoint with specified artists and ONLY getting tracks
    endpoint = 'https://api.spotify.com/v1/search?'

    # check the api documentation for the expected parameters and what they mean
    params = {
        'q':f'{artist}',
        'type':'track', 
        'limit':{count} # this tells spotify how many songs you want from their databases
    }

    response = spot.GET(endpoint, params)

    # check that we have data
    if len(response['tracks']['items']) == 0:
        print('Failed to fetch songs')
        exit(1)

    for track in response['tracks']['items']:
        song_uris.add(track['uri'])  # adding tracks uses uri

    return song_uris


# Creating and adding songs to a playlist
def make_playlist(song_uris, playlist_name = 'a playlist'):
    # Get current user id (username) (could be hardcoded)
    endpoint = 'https://api.spotify.com/v1/me'

    response = spot.GET(endpoint, {})
    user_id = response['id']

    # Create playlist
    endpoint = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    params = {
        'name':{playlist_name}
    }

    response = spot.POST(endpoint, params)
    playlist_id = response['id']

    # Add songs to playlist
    endpoint = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    params = {
        'uris': list(song_uris)
    }

    response = spot.POST(endpoint, params)

    print('\nCheck your spotify for the new playlist!')




'''
NOTE: This is what makes it all run
'''
if __name__ == '__main__':
    Timer(1, start).start()
    app.run(host=HOST_IP_ADDRESS, port=HOST_PORT, use_reloader=True, debug=True)