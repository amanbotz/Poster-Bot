"""
Broadcast Handler
Send messages to all users (Owner only)
"""

import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from database import amanbotz_db
from config import AMANBOTZ_OWNER_ID
from script import (
    AMANBOTZ_ERROR_BANNED,
    AMANBOTZ_ERROR_OWNER_ONLY,
    AMANBOTZ_BROADCAST_START,
    AMANBOTZ_BROADCAST_PROGRESS,
    AMANBOTZ_BROADCAST_COMPLETE
)


def is_owner(user_id: int) -> bool:
    """Check if user is the bot owner"""
    return user_id == AMANBOTZ_OWNER_ID


@Client.on_message(filters.command("broadcast") & filters.private)
async def broadcast_command(client: Client, message: Message):
    """Handle /broadcast command - Owner only"""
    user_id = message.from_user.id
    
    # Check if user is banned
    if await amanbotz_db.is_banned(user_id):
        await message.reply_text(AMANBOTZ_ERROR_BANNED, parse_mode="HTML")
        return
    
    # Check if user is owner
    if not is_owner(user_id):
        await message.reply_text(AMANBOTZ_ERROR_OWNER_ONLY, parse_mode="HTML")
        return
    
    # Check if message is a reply
    if not message.reply_to_message:
        await message.reply_text(
            "<b>⚠️ Usage:</b> Reply to a message with <code>/broadcast</code>",
            parse_mode="HTML"
        )
        return
    
    # Get the message to broadcast
    broadcast_msg = message.reply_to_message
    
    # Get all users
    users = await amanbotz_db.get_all_users()
    total_users = len(users)
    
    if total_users == 0:
        await message.reply_text(
            "<b>⚠️ No users to broadcast to!</b>",
            parse_mode="HTML"
        )
        return
    
    # Start broadcast
    status_msg = await message.reply_text(
        AMANBOTZ_BROADCAST_START,
        parse_mode="HTML"
    )
    
    sent = 0
    failed = 0
    
    for i, target_user_id in enumerate(users):
        try:
            # Copy the message to user
            await broadcast_msg.copy(chat_id=target_user_id)
            sent += 1
            
        except FloodWait as e:
            # Wait for flood
            await asyncio.sleep(e.value)
            try:
                await broadcast_msg.copy(chat_id=target_user_id)
                sent += 1
            except Exception:
                failed += 1
                
        except (UserIsBlocked, InputUserDeactivated):
            # User blocked bot or deactivated
            failed += 1
            # Optionally remove from database
            await amanbotz_db.delete_user(target_user_id)
            
        except Exception:
            failed += 1
        
        # Update progress every 20 users
        if (i + 1) % 20 == 0:
            try:
                await status_msg.edit_text(
                    AMANBOTZ_BROADCAST_PROGRESS.format(
                        sent=sent,
                        failed=failed,
                        total=total_users
                    ),
                    parse_mode="HTML"
                )
            except Exception:
                pass
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.05)
    
    # Final update
    await status_msg.edit_text(
        AMANBOTZ_BROADCAST_COMPLETE.format(
            sent=sent,
            failed=failed,
            total=total_users
        ),
        parse_mode="HTML"
    )
