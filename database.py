"""
MongoDB Database Handler for Poster Bot
Handles all database operations with async support
"""

from motor.motor_asyncio import AsyncIOMotorClient
from config import AMANBOTZ_MONGODB_URI, AMANBOTZ_DB_NAME, AMANBOTZ_OWNER_ID
from datetime import datetime


class AmanbotzDatabase:
    def __init__(self):
        self.client = AsyncIOMotorClient(AMANBOTZ_MONGODB_URI)
        self.db = self.client[AMANBOTZ_DB_NAME]
        
        # Collections
        self.users = self.db["users"]
        self.admins = self.db["admins"]
        self.banned_users = self.db["banned_users"]
        self.settings = self.db["settings"]
        self.posted_movies = self.db["posted_movies"]
    
    # ============ User Operations ============
    async def add_user(self, user_id: int, username: str = None, first_name: str = None):
        """Add a new user to the database"""
        user = await self.users.find_one({"user_id": user_id})
        if not user:
            await self.users.insert_one({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "joined_date": datetime.now()
            })
            return True
        return False
    
    async def get_all_users(self):
        """Get all user IDs"""
        users = self.users.find({})
        return [user["user_id"] async for user in users]
    
    async def get_users_count(self):
        """Get total user count"""
        return await self.users.count_documents({})
    
    async def delete_user(self, user_id: int):
        """Delete a user from database"""
        await self.users.delete_one({"user_id": user_id})
    
    # ============ Admin Operations ============
    async def add_admin(self, user_id: int):
        """Add a new admin"""
        admin = await self.admins.find_one({"user_id": user_id})
        if not admin:
            await self.admins.insert_one({
                "user_id": user_id,
                "added_date": datetime.now()
            })
            return True
        return False
    
    async def remove_admin(self, user_id: int):
        """Remove an admin"""
        result = await self.admins.delete_one({"user_id": user_id})
        return result.deleted_count > 0
    
    async def is_admin(self, user_id: int):
        """Check if user is admin or owner"""
        if user_id == AMANBOTZ_OWNER_ID:
            return True
        admin = await self.admins.find_one({"user_id": user_id})
        return admin is not None
    
    async def get_all_admins(self):
        """Get all admin IDs"""
        admins = self.admins.find({})
        return [admin["user_id"] async for admin in admins]
    
    async def get_admins_count(self):
        """Get total admin count"""
        return await self.admins.count_documents({})
    
    # ============ Ban Operations ============
    async def ban_user(self, user_id: int):
        """Ban a user"""
        banned = await self.banned_users.find_one({"user_id": user_id})
        if not banned:
            await self.banned_users.insert_one({
                "user_id": user_id,
                "banned_date": datetime.now()
            })
            return True
        return False
    
    async def unban_user(self, user_id: int):
        """Unban a user"""
        result = await self.banned_users.delete_one({"user_id": user_id})
        return result.deleted_count > 0
    
    async def is_banned(self, user_id: int):
        """Check if user is banned"""
        banned = await self.banned_users.find_one({"user_id": user_id})
        return banned is not None
    
    async def get_banned_count(self):
        """Get total banned users count"""
        return await self.banned_users.count_documents({})
    
    # ============ Settings Operations ============
    async def get_settings(self):
        """Get bot settings"""
        settings = await self.settings.find_one({"_id": "bot_settings"})
        if not settings:
            # Create default settings
            default_settings = {
                "_id": "bot_settings",
                "auto_post_channel": 0,
                "auto_post_enabled": False,
                "check_interval": 6
            }
            await self.settings.insert_one(default_settings)
            return default_settings
        return settings
    
    async def update_setting(self, key: str, value):
        """Update a specific setting"""
        await self.settings.update_one(
            {"_id": "bot_settings"},
            {"$set": {key: value}},
            upsert=True
        )
    
    async def get_auto_post_channel(self):
        """Get the auto-post channel ID"""
        settings = await self.get_settings()
        return settings.get("auto_post_channel", 0)
    
    async def set_auto_post_channel(self, channel_id: int):
        """Set the auto-post channel ID"""
        await self.update_setting("auto_post_channel", channel_id)
    
    async def is_auto_post_enabled(self):
        """Check if auto-posting is enabled"""
        settings = await self.get_settings()
        return settings.get("auto_post_enabled", False)
    
    async def toggle_auto_post(self):
        """Toggle auto-posting"""
        settings = await self.get_settings()
        new_value = not settings.get("auto_post_enabled", False)
        await self.update_setting("auto_post_enabled", new_value)
        return new_value
    
    # ============ Posted Movies Operations ============
    async def is_movie_posted(self, movie_id: str):
        """Check if a movie has already been posted"""
        movie = await self.posted_movies.find_one({"movie_id": movie_id})
        return movie is not None
    
    async def mark_movie_posted(self, movie_id: str, title: str):
        """Mark a movie as posted"""
        await self.posted_movies.insert_one({
            "movie_id": movie_id,
            "title": title,
            "posted_date": datetime.now()
        })
    
    async def get_posted_count(self):
        """Get total posted movies count"""
        return await self.posted_movies.count_documents({})


# Create database instance
amanbotz_db = AmanbotzDatabase()
