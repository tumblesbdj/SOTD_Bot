
# Discord Bot with Spotify Integration

This is a Discord bot that listens for Spotify track links in a specific Discord channel and adds them to a Spotify playlist. The bot also has the ability to scan the entire channel history for Spotify links and add any tracks that are not already in the playlist.

## Features

- Automatically add Spotify tracks from a specific Discord channel to a specified Spotify playlist.
- Prevents duplicate tracks from being added to the playlist.
- Reacts to messages with a custom emoji after successfully adding a track.
- Option to scan the entire channel history for Spotify tracks and add them to the playlist.

## Prerequisites

- Python 3.6 or higher
- A Discord bot token
- A Spotify Developer account and an application created in the Spotify Developer Dashboard

## Setup

### Step 1: Clone the Repository

```bash
git clone <your-repository-url>
cd <your-repository-directory>
```

### Step 2: Install Dependencies

Install the required Python libraries:

```bash
pip install discord.py spotipy
```

### Step 3: Set Up Spotify and Discord Credentials

1. **Spotify Developer Account**:
   - Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications).
   - Create a new application.
   - Get your `Client ID` and `Client Secret`.
   - Add `http://localhost:8080/` as a redirect URI in your Spotify application settings.

2. **Discord Bot**:
   - Go to the [Discord Developer Portal](https://discord.com/developers/applications).
   - Create a new application and add a bot.
   - Get your bot's token.

3. **Create a `keys.txt` File**:
   - Create a file named `keys.txt` in the root directory of the project.
   - Add your credentials in the following order:
     ```
     <DISCORD_TOKEN>
     <SPOTIFY_CLIENT_ID>
     <SPOTIFY_CLIENT_SECRET>
     <SPOTIFY_PLAYLIST_ID>
     <DISCORD_CHANNEL_ID>
     ```

### Step 4: Run the Bot

```bash
python <your-bot-script>.py
```

### Step 5: Authorize the Spotify Application

- When you run the bot, it will output an authorization URL. Open this URL in your browser to authorize the application.
- After authorization, the bot will start working.

### Usage

#### Adding Tracks from Incoming Messages

- The bot will listen for Spotify track links in the specified Discord channel.
- When a valid track link is detected, the bot will add the track to the specified Spotify playlist and react to the message with the custom emoji.

#### Adding Tracks from Channel History

- When the bot starts, it will ask you if you want to process the entire message history in the specified Discord channel.
- Reply "yes" to scan all previous messages in the channel and add any Spotify tracks that aren't already in the playlist.

### Customization

- **Custom Emoji**: Change the `REACT_EMOJI` variable in the script to use a different emoji.
- **Redirect URI**: Adjust the `REDIRECT_URI` variable if you're using a different environment.

### Troubleshooting

- **Invalid Redirect URI**: Make sure the redirect URI set in the Spotify Developer Dashboard matches the one in your code.
- **Rate Limits**: Be mindful of Discord and Spotify API rate limits, especially when processing large volumes of messages.
