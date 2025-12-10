"""
Main Bot File for Poster Bot
Entry point with Pyrogram client and scheduler
"""

import asyncio
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import (
    AMANBOTZ_BOT_TOKEN,
    AMANBOTZ_API_ID,
    AMANBOTZ_API_HASH,
    AMANBOTZ_CHECK_INTERVAL,
    check_api_config
)
from database import amanbotz_db
from api import amanbotz_api

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Validate API configuration
try:
    check_api_config()
except ValueError as e:
    logger.error(str(e))
    exit(1)

# Create Pyrogram Client
amanbotz_client = Client(
    "amanbotz_poster_bot",
    api_id=AMANBOTZ_API_ID,
    api_hash=AMANBOTZ_API_HASH,
    bot_token=AMANBOTZ_BOT_TOKEN,
    plugins=dict(root="plugins")
)

# Create Scheduler
amanbotz_scheduler = AsyncIOScheduler()


async def auto_post_new_releases():
    """Background task to fetch and post new releases"""
    try:
        # Check if auto-posting is enabled
        if not await amanbotz_db.is_auto_post_enabled():
            logger.info("Auto-posting is disabled")
            return
        
        # Get the channel ID
        channel_id = await amanbotz_db.get_auto_post_channel()
        if not channel_id:
            logger.info("No auto-post channel set")
            return
        
        logger.info("Checking for new releases...")
        releases = await amanbotz_api.get_new_releases()
        
        if not releases:
            logger.info("No new releases found or API not available")
            return
        
        from script import AMANBOTZ_AUTO_POST_MESSAGE
        
        for release in releases:
            # Check if already posted
            if await amanbotz_db.is_movie_posted(release["id"]):
                continue
            
            # Skip if no poster
            if not release.get("poster"):
                continue
            
            try:
                # Format the message
                message = AMANBOTZ_AUTO_POST_MESSAGE.format(
                    title=release["title"],
                    release_date=release.get("release_date", "N/A"),
                    type=release["type"].upper(),
                    rating=release.get("rating", "N/A"),
                    overview=release.get("overview", "No overview available.")[:500]
                )
                
                # Send the poster to channel
                await amanbotz_client.send_photo(
                    chat_id=channel_id,
                    photo=release["poster"],
                    caption=message,
                    parse_mode="HTML"
                )
                
                # Mark as posted
                await amanbotz_db.mark_movie_posted(release["id"], release["title"])
                logger.info(f"Posted: {release['title']}")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error posting {release['title']}: {e}")
                continue
        
        logger.info("Auto-post check completed")
        
    except Exception as e:
        logger.error(f"Error in auto-post task: {e}")


async def start_scheduler():
    """Start the scheduler for auto-posting"""
    amanbotz_scheduler.add_job(
        auto_post_new_releases,
        "interval",
        hours=AMANBOTZ_CHECK_INTERVAL,
        id="auto_post_job",
        replace_existing=True
    )
    amanbotz_scheduler.start()
    logger.info(f"Scheduler started - checking every {AMANBOTZ_CHECK_INTERVAL} hours")


async def main():
    """Main function to start the bot"""
    logger.info("Starting Poster Bot...")
    
    # Start the bot
    await amanbotz_client.start()
    
    # Start the scheduler
    await start_scheduler()
    
    # Run the first check immediately
    await auto_post_new_releases()
    
    logger.info("Bot is running!")
    
    # Keep alive
    await asyncio.Event().wait()


if __name__ == "__main__":
    try:
        amanbotz_client.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Bot stopped due to error: {e}")
