"""
Help Command Handler
Display help menu for users
"""

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from database import amanbotz_db
from config import AMANBOTZ_OWNER_ID
from script import AMANBOTZ_HELP_MESSAGE, AMANBOTZ_ADMIN_HELP, AMANBOTZ_ERROR_BANNED


@Client.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    """Handle /help command"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(
            AMANBOTZ_ERROR_BANNED,
            parse_mode="HTML"
        )
        return
    
    # Create keyboard
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 Home", callback_data="start"),
            InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
        ]
    ])
    
    # Check if user is admin/owner
    is_admin = await amanbotz_db.is_admin(user_id) or user_id == AMANBOTZ_OWNER_ID
    
    help_text = AMANBOTZ_HELP_MESSAGE
    
    if is_admin:
        # Add admin button
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 Home", callback_data="start"),
                InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
            ],
            [
                InlineKeyboardButton("👑 Admin Help", callback_data="admin_help")
            ]
        ])
    
    await message.reply_text(
        help_text,
        parse_mode="HTML",
        reply_markup=keyboard,
        disable_web_page_preview=True
    )


@Client.on_callback_query(filters.regex("^help$"))
async def help_callback(client: Client, callback_query):
    """Handle help button callback"""
    user_id = callback_query.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await callback_query.answer("You are banned!", show_alert=True)
        return
    
    # Check if user is admin/owner
    is_admin = await amanbotz_db.is_admin(user_id) or user_id == AMANBOTZ_OWNER_ID
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 Home", callback_data="start"),
            InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
        ]
    ])
    
    if is_admin:
        keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🏠 Home", callback_data="start"),
                InlineKeyboardButton("🔍 Search", switch_inline_query_current_chat="")
            ],
            [
                InlineKeyboardButton("👑 Admin Help", callback_data="admin_help")
            ]
        ])
    
    try:
        await callback_query.message.edit_text(
            AMANBOTZ_HELP_MESSAGE,
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    except Exception:
        pass
    
    await callback_query.answer()


@Client.on_callback_query(filters.regex("^admin_help$"))
async def admin_help_callback(client: Client, callback_query):
    """Handle admin help button callback"""
    user_id = callback_query.from_user.id
    
    # Check if user is admin/owner
    is_admin = await amanbotz_db.is_admin(user_id) or user_id == AMANBOTZ_OWNER_ID
    
    if not is_admin:
        await callback_query.answer("You don't have permission!", show_alert=True)
        return
    
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🏠 Home", callback_data="start"),
            InlineKeyboardButton("📚 Help", callback_data="help")
        ]
    ])
    
    try:
        await callback_query.message.edit_text(
            AMANBOTZ_ADMIN_HELP,
            parse_mode="HTML",
            reply_markup=keyboard,
            disable_web_page_preview=True
        )
    except Exception:
        pass
    
    await callback_query.answer()
