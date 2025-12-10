"""
Settings Handler
Manage bot settings from bot (Owner only)
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import amanbotz_db
from config import AMANBOTZ_OWNER_ID, AMANBOTZ_CHECK_INTERVAL
from script import (
    AMANBOTZ_ERROR_BANNED,
    AMANBOTZ_ERROR_OWNER_ONLY,
    AMANBOTZ_ERROR_INVALID_ID,
    AMANBOTZ_SUCCESS_SET_CHANNEL,
    AMANBOTZ_SUCCESS_TOGGLE_AUTO,
    AMANBOTZ_SETTINGS_MESSAGE
)


def is_owner(user_id: int) -> bool:
    """Check if user is the bot owner"""
    return user_id == AMANBOTZ_OWNER_ID


@Client.on_message(filters.command("setchannel") & filters.private)
async def set_channel_command(client: Client, message: Message):
    """Handle /setchannel command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get channel ID
    if len(message.command) < 2:
        await message.reply_text(
            "<b>⚠️ Usage:</b> <code>/setchannel [channel_id]</code>\n\n"
            "<i>Example: /setchannel -1001234567890</i>",
            parse_mode="HTML"
        )
        return
    
    try:
        channel_id = int(message.command[1])
    except ValueError:
        await message.reply_text(AMANBOTZ_ERROR_INVALID_ID, parse_mode="HTML")
        return
    
    # Verify bot is admin in channel
    try:
        chat = await client.get_chat(channel_id)
        member = await client.get_chat_member(channel_id, "me")
        
        if not member.privileges or not member.privileges.can_post_messages:
            await message.reply_text(
                "<b>⚠️ Bot must be an admin in the channel with posting rights!</b>",
                parse_mode="HTML"
            )
            return
        
    except Exception as e:
        await message.reply_text(
            f"<b>⚠️ Cannot access channel!</b>\n\n"
            f"<i>Make sure the bot is added to the channel as admin.</i>\n"
            f"<code>{str(e)}</code>",
            parse_mode="HTML"
        )
        return
    
    # Set channel
    await amanbotz_db.set_auto_post_channel(channel_id)
    
    await message.reply_text(
        AMANBOTZ_SUCCESS_SET_CHANNEL.format(channel_id=channel_id),
        parse_mode="HTML"
    )


@Client.on_message(filters.command("toggleauto") & filters.private)
async def toggle_auto_command(client: Client, message: Message):
    """Handle /toggleauto command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Check if channel is set
    channel = await amanbotz_db.get_auto_post_channel()
    if not channel:
        await message.reply_text(
            "<b>⚠️ Please set a channel first!</b>\n\n"
            "<i>Use /setchannel [channel_id]</i>",
            parse_mode="HTML"
        )
        return
    
    # Toggle auto-posting
    new_status = await amanbotz_db.toggle_auto_post()
    status_text = "ENABLED ✅" if new_status else "DISABLED ❌"
    
    await message.reply_text(
        AMANBOTZ_SUCCESS_TOGGLE_AUTO.format(status=status_text),
        parse_mode="HTML"
    )


@Client.on_message(filters.command("settings") & filters.private)
async def settings_command(client: Client, message: Message):
    """Handle /settings command"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is admin or owner
    if not await amanbotz_db.is_admin(user_id) and not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get settings
    settings = await amanbotz_db.get_settings()
    
    channel = settings.get("auto_post_channel", 0)
    auto_enabled = settings.get("auto_post_enabled", False)
    
    channel_text = f"<code>{channel}</code>" if channel else "<i>Not set</i>"
    auto_text = "Enabled ✅" if auto_enabled else "Disabled ❌"
    
    # Create keyboard for owner
    keyboard = None
    if is_owner(user_id):
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton(
                    "🔄 Toggle Auto-Post",
                    callback_data="toggle_auto"
                )
            ],
            [
                InlineKeyboardButton("🏠 Home", callback_data="start")
            ]
        ])
    
    await message.reply_text(
        AMANBOTZ_SETTINGS_MESSAGE.format(
            channel=channel_text,
            auto_status=auto_text,
            interval=AMANBOTZ_CHECK_INTERVAL
        ),
        parse_mode="HTML",
        reply_markup=keyboard
    )


@Client.on_callback_query(filters.regex("^toggle_auto$"))
async def toggle_auto_callback(client: Client, callback_query):
    """Handle toggle auto callback"""
    user_id = callback_query.from_user.id
    
    # Check if user is owner
    if not is_owner(user_id):
        await callback_query.answer("Owner only!", show_alert=True)
        return
    
    # Check if channel is set
    channel = await amanbotz_db.get_auto_post_channel()
    if not channel:
        await callback_query.answer("Set a channel first!", show_alert=True)
        return
    
    # Toggle auto-posting
    new_status = await amanbotz_db.toggle_auto_post()
    status_text = "ENABLED ✅" if new_status else "DISABLED ❌"
    
    await callback_query.answer(f"Auto-posting is now {status_text}")
    
    # Update message
    settings = await amanbotz_db.get_settings()
    channel = settings.get("auto_post_channel", 0)
    auto_enabled = settings.get("auto_post_enabled", False)
    
    channel_text = f"<code>{channel}</code>" if channel else "<i>Not set</i>"
    auto_text = "Enabled ✅" if auto_enabled else "Disabled ❌"
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔄 Toggle Auto-Post",
                callback_data="toggle_auto"
            )
        ],
        [
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
