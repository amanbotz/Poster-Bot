"""
Movie Search Handler
Search for movies and get posters with details
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import amanbotz_db
from api import amanbotz_api
from script import (
    AMANBOTZ_MOVIE_DETAILS_OMDB,
    AMANBOTZ_MOVIE_DETAILS_TMDB,
    AMANBOTZ_SEARCH_RESULTS,
    AMANBOTZ_NO_RESULTS,
    AMANBOTZ_ERROR_BANNED,
    AMANBOTZ_ERROR_API
)

# Store user search sessions
user_search_sessions = {}


@Client.on_message(filters.private & filters.text & ~filters.command(["start", "help", "ban", "unban", "addadmin", "removeadmin", "admins", "broadcast", "setchannel", "toggleauto", "settings", "stats"]))
async def search_movie(client: Client, message: Message):
    """Handle movie search by text message"""
    user_id = message.from_user.id
    query = message.text.strip()
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(
            AMANBOTZ_ERROR_BANNED,
            parse_mode="HTML"
        )
        return
    
    # Ignore short queries
    if len(query) < 2:
        return
    
    # Check if this is a number (selection from search results)
    if query.isdigit() and user_id in user_search_sessions:
        await handle_selection(client, message, int(query))
        return
    
    # Show searching status
    status_msg = await message.reply_text(
        "<b>🔍 Searching...</b>",
        parse_mode="HTML"
    )
    
    # Search for movie
    results = await amanbotz_api.search_movie(query)
    
    if not results or not results.get("results"):
        await status_msg.edit_text(
            AMANBOTZ_NO_RESULTS,
            parse_mode="HTML"
        )
        return
    
    source = results["source"]
    movies = results["results"][:10]  # Limit to 10 results
    
    # Store search session
    user_search_sessions[user_id] = {
        "results": movies,
        "source": source,
        "query": query
    }
    
    # Format results
    if source == "omdb":
        results_text = "\n".join([
            f"<b>{i+1}.</b> {m.get('Title', 'Unknown')} ({m.get('Year', 'N/A')})"
            for i, m in enumerate(movies)
        ])
    else:  # tmdb
        results_text = "\n".join([
            f"<b>{i+1}.</b> {m.get('title', 'Unknown')} ({m.get('release_date', 'N/A')[:4] if m.get('release_date') else 'N/A'})"
            for i, m in enumerate(movies)
        ])
    
    # Create inline buttons for quick selection
    buttons = []
    row = []
    for i in range(min(len(movies), 10)):
        row.append(InlineKeyboardButton(str(i+1), callback_data=f"select_{i}"))
        if len(row) == 5:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)
    
    keyboard = InlineKeyboardMarkup(buttons) if buttons else None
    
    await status_msg.edit_text(
        AMANBOTZ_SEARCH_RESULTS.format(
            query=query,
            count=len(movies),
            results=results_text
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )


async def handle_selection(client: Client, message: Message, selection: int):
    """Handle user selection from search results"""
    user_id = message.from_user.id
    
    if user_id not in user_search_sessions:
        return
    
    session = user_search_sessions[user_id]
    results = session["results"]
    source = session["source"]
    
    if selection < 1 or selection > len(results):
        await message.reply_text(
            "<b>⚠️ Invalid selection!</b>\n<i>Please choose a number from the list.</i>",
            parse_mode="HTML"
        )
        return
    
    movie = results[selection - 1]
    await send_movie_details(client, message, movie, source)


@Client.on_callback_query(filters.regex(r"^select_(\d+)$"))
async def select_callback(client: Client, callback_query):
    """Handle selection from inline buttons"""
    user_id = callback_query.from_user.id
    selection = int(callback_query.data.split("_")[1])
    
    if user_id not in user_search_sessions:
        await callback_query.answer("Session expired! Please search again.", show_alert=True)
        return
    
    session = user_search_sessions[user_id]
    results = session["results"]
    source = session["source"]
    
    if selection >= len(results):
        await callback_query.answer("Invalid selection!", show_alert=True)
        return
    
    movie = results[selection]
    await callback_query.answer()
    
    # Send as new message
    await send_movie_details(client, callback_query.message, movie, source, is_callback=True)


async def send_movie_details(client: Client, message: Message, movie: dict, source: str, is_callback: bool = False):
    """Send movie details with poster"""
    try:
        if source == "omdb":
            # Get full details from OMDB
            movie_id = movie.get("imdbID")
            details = await amanbotz_api.omdb_get_movie(imdb_id=movie_id)
            
            if not details:
                await message.reply_text(AMANBOTZ_ERROR_API, parse_mode="HTML")
                return
            
            formatted = amanbotz_api.format_movie_details_omdb(details)
            
            caption = AMANBOTZ_MOVIE_DETAILS_OMDB.format(
                title=formatted["title"],
                year=formatted["year"],
                released=formatted["released"],
                runtime=formatted["runtime"],
                genre=formatted["genre"],
                language=formatted["language"],
                awards=formatted["awards"],
                director=formatted["director"],
                actors=formatted["actors"],
                plot=formatted["plot"][:500] + "..." if len(formatted["plot"]) > 500 else formatted["plot"],
                imdb_rating=formatted["imdb_rating"],
                box_office=formatted["box_office"],
                imdb_id=formatted["imdb_id"]
            )
            
            poster_url = formatted["poster"]
            
        else:  # tmdb
            # Get full details from TMDB
            movie_id = movie.get("id")
            details = await amanbotz_api.tmdb_get_movie(movie_id)
            
            if not details:
                await message.reply_text(AMANBOTZ_ERROR_API, parse_mode="HTML")
                return
            
            formatted = amanbotz_api.format_movie_details_tmdb(details)
            
            caption = AMANBOTZ_MOVIE_DETAILS_TMDB.format(
                title=formatted["title"],
                year=formatted["year"],
                released=formatted["released"],
                runtime=formatted["runtime"],
                genre=formatted["genre"],
                language=formatted["language"],
                plot=formatted["plot"][:500] + "..." if len(formatted["plot"]) > 500 else formatted["plot"],
                rating=formatted["rating"],
                budget=formatted["budget"],
                revenue=formatted["revenue"]
            )
            
            poster_url = formatted["poster"]
        
        # Create back button
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 Home", callback_data="start"),
                InlineKeyboardButton("🔍 Search Again", switch_inline_query_current_chat="")
            ]
        ])
        
        # Send poster with details
        if poster_url and poster_url != "N/A":
            try:
                if is_callback:
                    await message.reply_photo(
                        photo=poster_url,
                        caption=caption,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
                else:
                    await message.reply_photo(
                        photo=poster_url,
                        caption=caption,
                        parse_mode="HTML",
                        reply_markup=keyboard
                    )
            except Exception:
                # Fallback to text if poster fails
                await message.reply_text(
                    caption,
                    parse_mode="HTML",
                    reply_markup=keyboard,
                    disable_web_page_preview=True
                )
        else:
            await message.reply_text(
                caption,
                parse_mode="HTML",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
            
    except Exception as e:
        await message.reply_text(
            f"{AMANBOTZ_ERROR_API}\n\n<code>{str(e)}</code>",
            parse_mode="HTML"
        )
