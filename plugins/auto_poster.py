"""
Auto Poster Module
Background task for fetching and posting new releases
This module is imported by the main bot file
"""

import asyncio
import logging
from api import amanbotz_api
from database import amanbotz_db
from script import AMANBOTZ_AUTO_POST_MESSAGE

logger = logging.getLogger(__name__)


async def check_and_post_releases(client):
    """
    Check for new releases and post to channel
    This is called by the scheduler in the main bot file
    """
    try:
        # Check if auto-posting is enabled
        if not await amanbotz_db.is_auto_post_enabled():
            logger.info("Auto-posting is disabled, skipping...")
            return
        
        # Get the channel ID
        channel_id = await amanbotz_db.get_auto_post_channel()
        if not channel_id:
            logger.info("No auto-post channel set, skipping...")
            return
        
        logger.info("Fetching new releases...")
        
        # Get new releases from API
        releases = await amanbotz_api.get_new_releases()
        
        if not releases:
            logger.info("No releases found or API unavailable")
            return
        
        posted_count = 0
        
        for release in releases:
            # Check if already posted
            if await amanbotz_db.is_movie_posted(release["id"]):
                continue
            
            # Skip if no poster
            if not release.get("poster"):
                continue
            
            try:
                # Format the message
                overview = release.get("overview", "No overview available.")
                if len(overview) > 500:
                    overview = overview[:497] + "..."
                
                message = AMANBOTZ_AUTO_POST_MESSAGE.format(
                    title=release["title"],
                    release_date=release.get("release_date", "N/A"),
                    type=release["type"].upper(),
                    rating=release.get("rating", "N/A"),
                    overview=overview
                )
                
                # Send the poster to channel
                await client.send_photo(
                    chat_id=channel_id,
                    photo=release["poster"],
                    caption=message,
                    parse_mode="HTML"
                )
                
                # Mark as posted
                await amanbotz_db.mark_movie_posted(release["id"], release["title"])
                posted_count += 1
                logger.info(f"Posted: {release['title']}")
                
                # Delay to avoid rate limiting
                await asyncio.sleep(3)
                
            except Exception as e:
                logger.error(f"Error posting {release['title']}: {e}")
                continue
        
        logger.info(f"Auto-post complete. Posted {posted_count} new releases.")
        
    except Exception as e:
        logger.error(f"Error in auto-post task: {e}")


async def manual_post_check(client, message):
    """
    Manually trigger a check for new releases
    Called by admin command
    """
    try:
        # Check if auto-posting is enabled
        if not await amanbotz_db.is_auto_post_enabled():
            await message.reply_text(
                "<b>⚠️ Auto-posting is disabled!</b>\n"
                "<i>Enable it first with /toggleauto</i>",
                parse_mode="HTML"
            )
            return
        
        # Get the channel ID
        channel_id = await amanbotz_db.get_auto_post_channel()
        if not channel_id:
            await message.reply_text(
                "<b>⚠️ No channel set!</b>\n"
                "<i>Set a channel first with /setchannel</i>",
                parse_mode="HTML"
            )
            return
        
        status = await message.reply_text(
            "<b>🔄 Checking for new releases...</b>",
            parse_mode="HTML"
        )
        
        # Get new releases
        releases = await amanbotz_api.get_new_releases()
        
        if not releases:
            await status.edit_text(
                "<b>❌ No releases found or API unavailable!</b>",
                parse_mode="HTML"
            )
            return
        
        # Count new releases
        new_count = 0
        for release in releases:
            if not await amanbotz_db.is_movie_posted(release["id"]):
                new_count += 1
        
        if new_count == 0:
            await status.edit_text(
                "<b>✅ No new releases to post!</b>\n"
                "<i>All releases have already been posted.</i>",
                parse_mode="HTML"
            )
            return
        
        await status.edit_text(
            f"<b>📤 Found {new_count} new releases!</b>\n"
            "<i>Posting to channel...</i>",
            parse_mode="HTML"
        )
        
        # Post releases
        await check_and_post_releases(client)
        
        await status.edit_text(
            f"<b>✅ Posted {new_count} new releases!</b>",
            parse_mode="HTML"
        )
        
    except Exception as e:
        await message.reply_text(
            f"<b>❌ Error:</b> <code>{str(e)}</code>",
            parse_mode="HTML"
        )
