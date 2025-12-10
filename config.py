import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
AMANBOTZ_BOT_TOKEN = os.environ.get("AMANBOTZ_BOT_TOKEN", "")
AMANBOTZ_API_ID = int(os.environ.get("AMANBOTZ_API_ID", "0"))
AMANBOTZ_API_HASH = os.environ.get("AMANBOTZ_API_HASH", "")

# MongoDB Configuration
AMANBOTZ_MONGODB_URI = os.environ.get("AMANBOTZ_MONGODB_URI", "")
AMANBOTZ_DB_NAME = os.environ.get("AMANBOTZ_DB_NAME", "amanbotz_poster_bot")

# API Keys (Optional - at least one required)
AMANBOTZ_TMDB_API = os.environ.get("AMANBOTZ_TMDB_API", "")
AMANBOTZ_OMDB_API = os.environ.get("AMANBOTZ_OMDB_API", "")

# Owner Configuration
AMANBOTZ_OWNER_ID = int(os.environ.get("AMANBOTZ_OWNER_ID", "0"))
AMANBOTZ_LOG_CHANNEL = int(os.environ.get("AMANBOTZ_LOG_CHANNEL", "0"))

# Auto Post Channel (can be changed via bot)
AMANBOTZ_AUTO_POST_CHANNEL = int(os.environ.get("AMANBOTZ_AUTO_POST_CHANNEL", "0"))

# Check if at least one API is configured
def check_api_config():
    """Check if at least one movie API is configured"""
    if not AMANBOTZ_TMDB_API and not AMANBOTZ_OMDB_API:
        raise ValueError("At least one API key (TMDB or OMDB) must be provided!")
    return True

# Determine which API to use
def get_available_api():
    """Return which API is available"""
    apis = []
    if AMANBOTZ_OMDB_API:
        apis.append("omdb")
    if AMANBOTZ_TMDB_API:
        apis.append("tmdb")
    return apis

# Bot Info
AMANBOTZ_BOT_NAME = os.environ.get("AMANBOTZ_BOT_NAME", "Poster Bot")
AMANBOTZ_BOT_USERNAME = os.environ.get("AMANBOTZ_BOT_USERNAME", "")

# Scheduler Interval (in hours)
AMANBOTZ_CHECK_INTERVAL = int(os.environ.get("AMANBOTZ_CHECK_INTERVAL", "6"))
