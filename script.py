"""
Script File for Poster Bot
Contains all text templates and messages (HTML format)
"""

# Start Message Template
AMANBOTZ_START_MESSAGE = """
<b>🎬 Welcome to Poster Bot!</b>

<i>Hey {first_name}! I'm your personal movie poster assistant.</i>

━━━━━━━━━━━━━━━━━━━━━
🎥 <b>What can I do?</b>
• Search any movie/series poster
• Get detailed movie information
• Auto-post new releases

━━━━━━━━━━━━━━━━━━━━━
📌 <b>Quick Start:</b>
Just send me a movie name and I'll fetch the poster for you!

<b>🎬 Featured Movie:</b>
<code>{movie_title}</code> ({movie_year})
⭐ Rating: {movie_rating}/10
━━━━━━━━━━━━━━━━━━━━━

<i>Use /help to see all commands</i>
"""

# Help Message Template
AMANBOTZ_HELP_MESSAGE = """
<b>📚 Help Menu</b>

━━━━━━━━━━━━━━━━━━━━━
<b>🔍 Search Commands</b>
• Just send a movie/series name to search
• I'll send you the poster with details

━━━━━━━━━━━━━━━━━━━━━
<b>📋 Available Commands</b>

<b>👤 User Commands:</b>
• <code>/start</code> - Start the bot
• <code>/help</code> - Show this help menu

━━━━━━━━━━━━━━━━━━━━━
<b>💡 Tips:</b>
• Send movie name for instant poster
• Include year for better results
• Example: <code>Inception 2010</code>

━━━━━━━━━━━━━━━━━━━━━
<i>Made with ❤️ by @AmanBotz</i>
"""

# Admin Help Message
AMANBOTZ_ADMIN_HELP = """
<b>👑 Admin Commands</b>

━━━━━━━━━━━━━━━━━━━━━
<b>👤 User Management:</b>
• <code>/ban [user_id]</code> - Ban a user
• <code>/unban [user_id]</code> - Unban a user

<b>👥 Admin Management:</b>
• <code>/addadmin [user_id]</code> - Add new admin
• <code>/removeadmin [user_id]</code> - Remove admin
• <code>/admins</code> - List all admins

<b>📢 Broadcast:</b>
• <code>/broadcast</code> - Reply to a message to broadcast

<b>⚙️ Settings:</b>
• <code>/setchannel [channel_id]</code> - Set auto-post channel
• <code>/toggleauto</code> - Enable/Disable auto-posting
• <code>/settings</code> - View current settings

<b>📊 Statistics:</b>
• <code>/stats</code> - View bot statistics
━━━━━━━━━━━━━━━━━━━━━
"""

# Movie Details Template (OMDB)
AMANBOTZ_MOVIE_DETAILS_OMDB = """
<b>🎬 {title}</b> ({year})

━━━━━━━━━━━━━━━━━━━━━
📅 <b>Released:</b> {released}
⏱ <b>Runtime:</b> {runtime}
🎭 <b>Genre:</b> {genre}
🌍 <b>Language:</b> {language}
🏆 <b>Awards:</b> {awards}

━━━━━━━━━━━━━━━━━━━━━
🎬 <b>Director:</b> {director}
🎭 <b>Cast:</b> {actors}

━━━━━━━━━━━━━━━━━━━━━
📝 <b>Plot:</b>
<i>{plot}</i>

━━━━━━━━━━━━━━━━━━━━━
⭐ <b>IMDb Rating:</b> {imdb_rating}/10
💰 <b>Box Office:</b> {box_office}

🔗 <a href="https://www.imdb.com/title/{imdb_id}">View on IMDb</a>
"""

# Movie Details Template (TMDB)
AMANBOTZ_MOVIE_DETAILS_TMDB = """
<b>🎬 {title}</b> ({year})

━━━━━━━━━━━━━━━━━━━━━
📅 <b>Released:</b> {released}
⏱ <b>Runtime:</b> {runtime}
🎭 <b>Genre:</b> {genre}
🌍 <b>Language:</b> {language}

━━━━━━━━━━━━━━━━━━━━━
📝 <b>Plot:</b>
<i>{plot}</i>

━━━━━━━━━━━━━━━━━━━━━
⭐ <b>Rating:</b> {rating}/10
💵 <b>Budget:</b> {budget}
💰 <b>Revenue:</b> {revenue}
"""

# Auto Post Template
AMANBOTZ_AUTO_POST_MESSAGE = """
<b>🆕 New Release!</b>

<b>🎬 {title}</b>
📅 <b>Release Date:</b> {release_date}
🎭 <b>Type:</b> {type}
⭐ <b>Rating:</b> {rating}/10

━━━━━━━━━━━━━━━━━━━━━
📝 <b>Overview:</b>
<i>{overview}</i>
━━━━━━━━━━━━━━━━━━━━━
"""

# Search Results Template
AMANBOTZ_SEARCH_RESULTS = """
<b>🔍 Search Results for:</b> <code>{query}</code>

Found <b>{count}</b> results:

{results}

<i>Send the number to get poster details</i>
"""

# Stats Template
AMANBOTZ_STATS_MESSAGE = """
<b>📊 Bot Statistics</b>

━━━━━━━━━━━━━━━━━━━━━
👤 <b>Total Users:</b> {total_users}
🚫 <b>Banned Users:</b> {banned_users}
👑 <b>Total Admins:</b> {total_admins}
🎬 <b>Movies Posted:</b> {movies_posted}

━━━━━━━━━━━━━━━━━━━━━
⚙️ <b>Auto-Post:</b> {auto_status}
📢 <b>Channel:</b> {channel}
━━━━━━━━━━━━━━━━━━━━━
"""

# Settings Template
AMANBOTZ_SETTINGS_MESSAGE = """
<b>⚙️ Bot Settings</b>

━━━━━━━━━━━━━━━━━━━━━
📢 <b>Auto-Post Channel:</b> {channel}
🔄 <b>Auto-Post Status:</b> {auto_status}
⏰ <b>Check Interval:</b> Every {interval} hours
━━━━━━━━━━━━━━━━━━━━━

<i>Use commands to modify settings</i>
"""

# Broadcast Messages
AMANBOTZ_BROADCAST_START = "<b>📢 Starting Broadcast...</b>"
AMANBOTZ_BROADCAST_PROGRESS = """
<b>📢 Broadcast Progress</b>

✅ <b>Sent:</b> {sent}
❌ <b>Failed:</b> {failed}
📊 <b>Total:</b> {total}
"""
AMANBOTZ_BROADCAST_COMPLETE = """
<b>✅ Broadcast Complete!</b>

📊 <b>Results:</b>
✅ Sent: {sent}
❌ Failed: {failed}
📊 Total: {total}
"""

# Error Messages
AMANBOTZ_ERROR_BANNED = """
<b>🚫 Access Denied!</b>

<i>You have been banned from using this bot.</i>
"""

AMANBOTZ_ERROR_NO_PERMISSION = """
<b>⚠️ Permission Denied!</b>

<i>You don't have permission to use this command.</i>
"""

AMANBOTZ_ERROR_OWNER_ONLY = """
<b>👑 Owner Only!</b>

<i>This command can only be used by the bot owner.</i>
"""

AMANBOTZ_ERROR_NOT_FOUND = """
<b>❌ Not Found!</b>

<i>Could not find any results for your query.</i>
<i>Try a different search term.</i>
"""

AMANBOTZ_ERROR_API = """
<b>⚠️ API Error!</b>

<i>Something went wrong while fetching data.</i>
<i>Please try again later.</i>
"""

AMANBOTZ_ERROR_INVALID_ID = """
<b>⚠️ Invalid ID!</b>

<i>Please provide a valid user/channel ID.</i>
"""

# Success Messages
AMANBOTZ_SUCCESS_BAN = "<b>✅ User {user_id} has been banned!</b>"
AMANBOTZ_SUCCESS_UNBAN = "<b>✅ User {user_id} has been unbanned!</b>"
AMANBOTZ_SUCCESS_ADD_ADMIN = "<b>✅ User {user_id} has been added as admin!</b>"
AMANBOTZ_SUCCESS_REMOVE_ADMIN = "<b>✅ User {user_id} has been removed from admins!</b>"
AMANBOTZ_SUCCESS_SET_CHANNEL = "<b>✅ Auto-post channel set to {channel_id}!</b>"
AMANBOTZ_SUCCESS_TOGGLE_AUTO = "<b>✅ Auto-posting is now {status}!</b>"

# Admin List Template
AMANBOTZ_ADMIN_LIST = """
<b>👑 Admin List</b>

━━━━━━━━━━━━━━━━━━━━━
{admins}
━━━━━━━━━━━━━━━━━━━━━

<b>Total:</b> {count} admins
"""

# No Results
AMANBOTZ_NO_RESULTS = """
<b>🔍 No Results Found</b>

<i>Could not find any movie/series matching your query.</i>
<i>Try using a different search term or include the year.</i>

<b>Example:</b> <code>Inception 2010</code>
"""
