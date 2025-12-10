"""
Stats Handler
View bot statistics (Owner only)
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import amanbotz_db
from config import AMANBOTZ_OWNER_ID
from script import AMANBOTZ_ERROR_BANNED, AMANBOTZ_ERROR_OWNER_ONLY, AMANBOTZ_STATS_MESSAGE


def is_owner(user_id: int) -> bool:
    """Check if user is the bot owner"""
    return user_id == AMANBOTZ_OWNER_ID


@Client.on_message(filters.command("stats") & filters.private)
async def stats_command(client: Client, message: Message):
    """Handle /stats command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get statistics
    total_users = await amanbotz_db.get_users_count()
    banned_users = await amanbotz_db.get_banned_count()
    total_admins = await amanbotz_db.get_admins_count()
    movies_posted = await amanbotz_db.get_posted_count()
    
    # Get auto-post status
    settings = await amanbotz_db.get_settings()
    auto_enabled = settings.get("auto_post_enabled", False)
    channel = settings.get("auto_post_channel", 0)
    
    auto_text = "Enabled ✅" if auto_enabled else "Disabled ❌"
    channel_text = f"<code>{channel}</code>" if channel else "<i>Not set</i>"
    
    # Create keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="show_settings"),
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")
        ],
        [
            InlineKeyboardButton("🏠 Home", callback_data="start")
        ]
    ])
    
    await message.reply_text(
        AMANBOTZ_STATS_MESSAGE.format(
            total_users=total_users,
            banned_users=banned_users,
            total_admins=total_admins + 1,  # +1 for owner
            movies_posted=movies_posted,
            auto_status=auto_text,
            channel=channel_text
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^refresh_stats$"))
async def refresh_stats_callback(client: Client, callback_query):
    """Handle refresh stats callback"""
    user_id = callback_query.from_user.id
    
    # Check if user is owner
    if not is_owner(user_id):
        await callback_query.answer("Owner only!", show_alert=True)
        return
    
    # Get statistics
    total_users = await amanbotz_db.get_users_count()
    banned_users = await amanbotz_db.get_banned_count()
    total_admins = await amanbotz_db.get_admins_count()
    movies_posted = await amanbotz_db.get_posted_count()
    
    # Get auto-post status
    settings = await amanbotz_db.get_settings()
    auto_enabled = settings.get("auto_post_enabled", False)
    channel = settings.get("auto_post_channel", 0)
    
    auto_text = "Enabled ✅" if auto_enabled else "Disabled ❌"
    channel_text = f"<code>{channel}</code>" if channel else "<i>Not set</i>"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚙️ Settings", callback_data="show_settings"),
            InlineKeyboardButton("🔄 Refresh", callback_data="refresh_stats")
        ],
        [
            InlineKeyboardButton("🏠 Home", callback_data="start")
        ]
    ])
    
    try:
        await callback_query.message.edit_text(
            AMANBOTZ_STATS_MESSAGE.format(
                total_users=total_users,
                banned_users=banned_users,
                total_admins=total_admins + 1,
                movies_posted=movies_posted,
                auto_status=auto_text,
                channel=channel_text
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )
        await callback_query.answer("Stats refreshed!")
    except Exception:
        await callback_query.answer("Stats already up to date!")


@Client.on_callback_query(filters.regex("^show_settings$"))
async def show_settings_callback(client: Client, callback_query):
    """Handle show settings callback"""
    from script import AMANBOTZ_SETTINGS_MESSAGE
    from config import AMANBOTZ_CHECK_INTERVAL
    
    user_id = callback_query.from_user.id
    
    # Check if user is owner
    if not is_owner(user_id):
        await callback_query.answer("Owner only!", show_alert=True)
        return
    
    # Get settings
    settings = await amanbotz_db.get_settings()
    channel = settings.get("auto_post_channel", 0)
    auto_enabled = settings.get("auto_post_enabled", False)
    
    channel_text = f"<code>{channel}</code>" if channel else "<i>Not set</i>"
    auto_text = "Enabled ✅" if auto_enabled else "Disabled ❌"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🔄 Toggle Auto-Post", callback_data="toggle_auto")
        ],
        [
            InlineKeyboardButton("📊 Stats", callback_data="refresh_stats"),
            InlineKeyboardButton("🏠 Home", callback_data="start")
        ]
    ])
    
    try:
        await callback_query.message.edit_text(
            AMANBOTZ_SETTINGS_MESSAGE.format(
                channel=channel_text,
                auto_status=auto_text,
                interval=AMANBOTZ_CHECK_INTERVAL
            ),
            parse_mode="HTML",
            reply_markup=keyboard
        )
    except Exception:
        pass
    
    await callback_query.answer()
