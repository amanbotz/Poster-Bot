"""
Admin Management Handler
Add/remove admins, ban/unban users (Owner only)
"""

from pyrogram import Client, filters
from pyrogram.types import Message
from database import amanbotz_db
from config import AMANBOTZ_OWNER_ID
from script import (
    AMANBOTZ_ERROR_BANNED,
    AMANBOTZ_ERROR_OWNER_ONLY,
    AMANBOTZ_ERROR_INVALID_ID,
    AMANBOTZ_SUCCESS_BAN,
    AMANBOTZ_SUCCESS_UNBAN,
    AMANBOTZ_SUCCESS_ADD_ADMIN,
    AMANBOTZ_SUCCESS_REMOVE_ADMIN,
    AMANBOTZ_ADMIN_LIST
)


def is_owner(user_id: int) -> bool:
    """Check if user is the bot owner"""
    return user_id == AMANBOTZ_OWNER_ID


@Client.on_message(filters.command("ban") & filters.private)
async def ban_user_command(client: Client, message: Message):
    """Handle /ban command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get target user ID
    if len(message.command) < 2:
        await message.reply_text(
            "<b>⚠️ Usage:</b> <code>/ban [user_id]</code>",
            parse_mode="HTML"
        )
        return
    
    try:
        target_id = int(message.command[1])
    except ValueError:
        await message.reply_text(AMANBOTZ_ERROR_INVALID_ID, parse_mode="HTML")
        return
    
    # Can't ban owner
    if target_id == AMANBOTZ_OWNER_ID:
        await message.reply_text(
            "<b>⚠️ Cannot ban the owner!</b>",
            parse_mode="HTML"
        )
        return
    
    # Ban the user
    result = await amanbotz_db.ban_user(target_id)
    
    if result:
        await message.reply_text(
            AMANBOTZ_SUCCESS_BAN.format(user_id=target_id),
            parse_mode="HTML"
        )
    else:
        await message.reply_text(
            "<b>⚠️ User is already banned!</b>",
            parse_mode="HTML"
        )


@Client.on_message(filters.command("unban") & filters.private)
async def unban_user_command(client: Client, message: Message):
    """Handle /unban command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get target user ID
    if len(message.command) < 2:
        await message.reply_text(
            "<b>⚠️ Usage:</b> <code>/unban [user_id]</code>",
            parse_mode="HTML"
        )
        return
    
    try:
        target_id = int(message.command[1])
    except ValueError:
        await message.reply_text(AMANBOTZ_ERROR_INVALID_ID, parse_mode="HTML")
        return
    
    # Unban the user
    result = await amanbotz_db.unban_user(target_id)
    
    if result:
        await message.reply_text(
            AMANBOTZ_SUCCESS_UNBAN.format(user_id=target_id),
            parse_mode="HTML"
        )
    else:
        await message.reply_text(
            "<b>⚠️ User is not banned!</b>",
            parse_mode="HTML"
        )


@Client.on_message(filters.command("addadmin") & filters.private)
async def add_admin_command(client: Client, message: Message):
    """Handle /addadmin command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get target user ID
    if len(message.command) < 2:
        await message.reply_text(
            "<b>⚠️ Usage:</b> <code>/addadmin [user_id]</code>",
            parse_mode="HTML"
        )
        return
    
    try:
        target_id = int(message.command[1])
    except ValueError:
        await message.reply_text(AMANBOTZ_ERROR_INVALID_ID, parse_mode="HTML")
        return
    
    # Add admin
    result = await amanbotz_db.add_admin(target_id)
    
    if result:
        await message.reply_text(
            AMANBOTZ_SUCCESS_ADD_ADMIN.format(user_id=target_id),
            parse_mode="HTML"
        )
    else:
        await message.reply_text(
            "<b>⚠️ User is already an admin!</b>",
            parse_mode="HTML"
        )


@Client.on_message(filters.command("removeadmin") & filters.private)
async def remove_admin_command(client: Client, message: Message):
    """Handle /removeadmin command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get target user ID
    if len(message.command) < 2:
        await message.reply_text(
            "<b>⚠️ Usage:</b> <code>/removeadmin [user_id]</code>",
            parse_mode="HTML"
        )
        return
    
    try:
        target_id = int(message.command[1])
    except ValueError:
        await message.reply_text(AMANBOTZ_ERROR_INVALID_ID, parse_mode="HTML")
        return
    
    # Remove admin
    result = await amanbotz_db.remove_admin(target_id)
    
    if result:
        await message.reply_text(
            AMANBOTZ_SUCCESS_REMOVE_ADMIN.format(user_id=target_id),
            parse_mode="HTML"
        )
    else:
        await message.reply_text(
            "<b>⚠️ User is not an admin!</b>",
            parse_mode="HTML"
        )


@Client.on_message(filters.command("admins") & filters.private)
async def list_admins_command(client: Client, message: Message):
    """Handle /admins command"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is admin or owner
    if not await amanbotz_db.is_admin(user_id) and not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Get all admins
    admins = await amanbotz_db.get_all_admins()
    
    if not admins:
        admin_list = "<i>No admins added yet.</i>"
    else:
        admin_list = "\n".join([f"• <code>{admin_id}</code>" for admin_id in admins])
    
    # Add owner to list
    full_list = f"👑 <b>Owner:</b> <code>{AMANBOTZ_OWNER_ID}</code>\n\n<b>Admins:</b>\n{admin_list}"
    
    await message.reply_text(
        AMANBOTZ_ADMIN_LIST.format(
            admins=full_list,
            count=len(admins) + 1  # +1 for owner
        ),
        parse_mode="HTML"
    )
