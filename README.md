# Telegram Poster Bot

A feature-rich Telegram bot for fetching and posting movie/web series posters from TMDB and OMDB APIs.

## Features

- 🎬 **Movie Search**: Search for any movie/series and get the poster with detailed information
- 📢 **Auto-Post**: Automatically fetch and post new releases to a channel (24/7)
- 👑 **Admin Management**: Add/remove admins with owner-only commands
- 🚫 **Ban System**: Ban/unban users from using the bot
- 📊 **Statistics**: View bot usage statistics
- 📤 **Broadcast**: Send messages to all bot users
- ⚙️ **Settings**: Manage bot settings directly from Telegram

## Setup

### 1. Get Required Credentials

- **Telegram Bot Token**: Create a bot via [@BotFather](https://t.me/BotFather)
- **API ID & Hash**: Get from [my.telegram.org](https://my.telegram.org)
- **MongoDB URI**: Create a free cluster at [MongoDB Atlas](https://www.mongodb.com/atlas)
- **OMDB API Key**: Get from [OMDB API](http://www.omdbapi.com/apikey.aspx)
- **TMDB API Key** (Optional): Get from [TMDB](https://www.themoviedb.org/settings/api)

### 2. Configure Environment Variables

Copy `.env.template` to `.env` and fill in your values:

```env
AMANBOTZ_BOT_TOKEN=your_bot_token
AMANBOTZ_API_ID=your_api_id
AMANBOTZ_API_HASH=your_api_hash
AMANBOTZ_MONGODB_URI=your_mongodb_uri
AMANBOTZ_OWNER_ID=your_user_id
AMANBOTZ_OMDB_API=your_omdb_key
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Bot

```bash
python amanbotz.py
```

## Deployment on Northflank/Heroku

1. Create a new service on Northflank
2. Connect your GitHub repository
3. Set the build command: `pip install -r requirements.txt`
4. Set the start command: `python amanbotz.py`
5. Add all environment variables
6. Deploy!

## Commands

### User Commands
| Command | Description |
|---------|-------------|
| `/start` | Start the bot |
| `/help` | Show help menu |
| `[movie name]` | Search for a movie |

### Owner Commands
| Command | Description |
|---------|-------------|
| `/stats` | View bot statistics |
| `/broadcast` | Broadcast message to all users |
| `/ban [user_id]` | Ban a user |
| `/unban [user_id]` | Unban a user |
| `/addadmin [user_id]` | Add an admin |
| `/removeadmin [user_id]` | Remove an admin |
| `/admins` | List all admins |
| `/setchannel [channel_id]` | Set auto-post channel |
| `/toggleauto` | Toggle auto-posting |
| `/settings` | View current settings |

## License

MIT License - Feel free to use and modify!

## Developer

Made with ❤️ by [@AmanBotz](https://t.me/AmanBotz)
