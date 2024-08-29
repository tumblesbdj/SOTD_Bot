import discord
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


# Read the keys from the keys.txt file
with open('keys.txt', 'r') as f:
    keys = f.read().splitlines()

DISCORD_TOKEN = keys[0]  # First line is the Discord token
SPOTIFY_CLIENT_ID = keys[1]  # Second line is the Spotify Client ID
SPOTIFY_CLIENT_SECRET = keys[2]  # Third line is the Spotify Client Secret

# Spotify playlist details
SPOTIFY_REDIRECT_URI = 'http://localhost:8888/'  # Set your redirect URI
PLAYLIST_ID = '4YMOPVZhxMPaeL5OnfZRWz'  # Replace with your playlist ID
CHANNEL_ID = 698584841796714567  # Replace with your Discord channel ID

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())


# Initialize Discord client
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):
    print(f"Received message in channel {message.channel.id}: {message.content}")

    # Check if the message is in the specified channel
    if message.channel.id == CHANNEL_ID:
        print("Message is in the correct channel.")
        
        # Split the message content into words (separated by spaces)
        for word in message.content.split():
            if 'https://open.spotify.com/track/' in word:
                print("Spotify link detected.")
                
                # Extract the Spotify track URL (remove any URL parameters)
                track_url = word.split('?')[0]
                print(f"Track URL: {track_url}")

                try:
                    # Add the track to the Spotify playlist
                    sp.playlist_add_items(PLAYLIST_ID, [track_url])
                    await message.channel.send(f'Added track to playlist: {track_url}')
                except Exception as e:
                    await message.channel.send(f'Failed to add track: {str(e)}')
                return  # Exit after processing the first link
        print("No Spotify link found.")



# Run the bot
client.run(DISCORD_TOKEN)
