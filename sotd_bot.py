import discord
import spotipy
from spotipy.oauth2 import SpotifyOAuth


# Read the keys from the keys.txt file
with open('keys.txt', 'r') as f:
    keys = f.read().splitlines()

DISCORD_TOKEN = keys[0]          # First line is the Discord token
SPOTIFY_CLIENT_ID = keys[1]      # Second line is the Spotify Client ID
SPOTIFY_CLIENT_SECRET = keys[2]  # Third line is the Spotify Client Secret
PLAYLIST_ID = str(keys[3])       # Fourth line is the Spotify Playlist ID
CHANNEL_ID = keys[4]             # Fifth line is the Discord Channel ID

REACT_EMOJI = '🤖'  # Custom emoji to react to successful track additions
REDIRECT_URI = 'http://localhost:8080/'  # Spotify redirect URI with a port

# Initialize SpotifyOAuth and get the authorization URL
sp_oauth = SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID,
                        client_secret=SPOTIFY_CLIENT_SECRET,
                        redirect_uri=REDIRECT_URI,
                        scope="playlist-modify-public")

auth_url = sp_oauth.get_authorize_url()
print(f"Please navigate to the following URL to authorize the application: {auth_url}")

# Initialize Spotify client (will fail if not yet authorized)
sp = spotipy.Spotify(auth_manager=sp_oauth)

# Initialize Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

async def add_tracks_from_history(channel):
    # Get current playlist tracks to check for duplicates
    playlist_tracks = sp.playlist_tracks(PLAYLIST_ID)
    existing_track_ids = {item['track']['id'] for item in playlist_tracks['items']}

    async for message in channel.history(limit=None):  # Fetch all message history
        if 'https://open.spotify.com/track/' in message.content:
            track_url = message.content.split('?')[0]
            track_id = track_url.split('/')[-1]
            
            if track_id not in existing_track_ids:
                print(f"Adding track: {track_url}")
                
                try:
                    # Add the track to the Spotify playlist
                    sp.playlist_add_items(PLAYLIST_ID, [track_url])

                    # React with a custom emoji
                    await message.add_reaction(REACT_EMOJI)

                    # Add the new track ID to the set of existing tracks
                    existing_track_ids.add(track_id)

                except Exception as e:
                    print(f'Failed to add track: {str(e)}')
            else:
                print(f"Track {track_url} is already in the playlist, skipping...")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    channel = client.get_channel(CHANNEL_ID)

    # Ask for confirmation before processing the entire channel history
    confirmation = input("ARE YOU SURE YOU WANT TO GO THROUGH EVERY MESSAGE IN THIS CHANNEL (REPLY YES IF YES): ")
    if confirmation.strip().lower() == 'yes':
        print("Processing the entire channel history...")
        await add_tracks_from_history(channel)
        print("Finished processing the channel history.")
    else:
        print("Skipped processing the channel history.")

@client.event
async def on_message(message):
    # Check if the message is in the specified channel
    if message.channel.id == CHANNEL_ID and 'https://open.spotify.com/track/' in message.content:
        print(f"Adding track: {message.content}")
        
        try:
            # Extract the Spotify track URL (remove any URL parameters)
            track_url = message.content.split('?')[0]
            
            # Add the track to the Spotify playlist
            sp.playlist_add_items(PLAYLIST_ID, [track_url])
            await message.add_reaction(REACT_EMOJI)

        except Exception as e:
            print(f'Failed to add track: {str(e)}')

# Run the bot
client.run(DISCORD_TOKEN)
