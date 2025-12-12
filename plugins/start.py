"""
Start Command Handler
Impressive welcome page with random movie poster
"""

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import amanbotz_db
from api import amanbotz_api
from config import AMANBOTZ_OWNER_ID
from script import AMANBOTZ_START_MESSAGE, AMANBOTZ_ERROR_BANNED


@Client.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    """Handle /start command"""
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name or "User"
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(
            AMANBOTZ_ERROR_BANNED,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    # Add user to database
    await amanbotz_db.add_user(user_id, username, first_name)
    
    # Get random movie poster
    random_movie = await amanbotz_api.get_random_poster()
    
    # Create keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
        ],
        [
            InlineKeyboardButton("📢 Channel", url="https://t.me/AmanBotz"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/AmanBotz")
        ]
    ])
    
    if random_movie and random_movie.get("poster"):
        # Send poster with welcome message
        caption = AMANBOTZ_START_MESSAGE.format(
            first_name=first_name,
            movie_title=random_movie.get("title", "Unknown"),
            movie_year=random_movie.get("year", "N/A"),
            movie_rating=random_movie.get("rating", "N/A")
        )
        
        try:
            await message.reply_photo(
                photo=random_movie["poster"],
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=keyboard
            )
        except Exception:
            # Fallback if poster fails
            await message.reply_text(
                caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
    else:
        # No poster available
        fallback_message = AMANBOTZ_START_MESSAGE.format(
            first_name=first_name,
            movie_title="Featured Movie",
            movie_year="2024",
            movie_rating="8.5"
        )
        await message.reply_text(
            fallback_message,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )


@Client.on_callback_query(filters.regex("^start$"))
async def start_callback(client: Client, callback_query):
    """Handle start button callback"""
    user_id = callback_query.from_user.id
    first_name = callback_query.from_user.first_name or "User"
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await callback_query.answer("You are banned!", show_alert=True)
        return
    
    # Get random movie poster
    random_movie = await amanbotz_api.get_random_poster()
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("📚 Help", callback_data="help"),
            InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
        ],
        [
            InlineKeyboardButton("📢 Channel", url="https://t.me/AmanBotz"),
            InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/AmanBotz")
        ]
    ])
    
    if random_movie and random_movie.get("poster"):
        caption = AMANBOTZ_START_MESSAGE.format(
            first_name=first_name,
            movie_title=random_movie.get("title", "Unknown"),
            movie_year=random_movie.get("year", "N/A"),
            movie_rating=random_movie.get("rating", "N/A")
        )
        
        try:
            await callback_query.message.edit_media(
                media=dict(type="photo", media=random_movie["poster"]),
                reply_markup=keyboard
            )
            await callback_query.message.edit_caption(
                caption=caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=keyboard
            )
        except Exception:
            await callback_query.message.edit_text(
                caption,
                parse_mode=enums.ParseMode.HTML,
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
    else:
        fallback_message = AMANBOTZ_START_MESSAGE.format(
            first_name=first_name,
            movie_title="Featured Movie",
            movie_year="2024",
            movie_rating="8.5"
        )
        await callback_query.message.edit_text(
            fallback_message,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    
    await callback_query.answer()