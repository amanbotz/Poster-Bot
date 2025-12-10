"""
Movie API Handler for Poster Bot
Supports both TMDB and OMDB APIs (optional - at least one required)
"""

import aiohttp
import random
from config import AMANBOTZ_TMDB_API, AMANBOTZ_OMDB_API, get_available_api


class AmanbotzMovieAPI:
    def __init__(self):
        self.tmdb_base = "https://api.themoviedb.org/3"
        self.tmdb_image_base = "https://image.tmdb.org/t/p/original"
        self.omdb_base = "http://www.omdbapi.com/"
        self.available_apis = get_available_api()
    
    # ============ OMDB API Methods ============
    async def omdb_search(self, query: str):
        """Search for a movie using OMDB API"""
        if not AMANBOTZ_OMDB_API:
            return None
        
        async with aiohttp.ClientSession() as session:
            params = {
                "apikey": AMANBOTZ_OMDB_API,
                "s": query,
                "type": "movie"
            }
            async with session.get(self.omdb_base, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("Response") == "True":
                        return data.get("Search", [])
        return None
    
    async def omdb_get_movie(self, imdb_id: str = None, title: str = None):
        """Get movie details from OMDB"""
        if not AMANBOTZ_OMDB_API:
            return None
        
        async with aiohttp.ClientSession() as session:
            params = {"apikey": AMANBOTZ_OMDB_API, "plot": "full"}
            if imdb_id:
                params["i"] = imdb_id
            elif title:
                params["t"] = title
            else:
                return None
            
            async with session.get(self.omdb_base, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("Response") == "True":
                        return data
        return None
    
    async def omdb_get_random_movie(self):
        """Get a random popular movie from OMDB for start page"""
        # List of popular movie IMDb IDs for random selection
        popular_movies = [
            "tt0111161", "tt0068646", "tt0468569", "tt0071562", "tt0050083",
            "tt0108052", "tt0167260", "tt0110912", "tt0060196", "tt0120737",
            "tt0137523", "tt0109830", "tt1375666", "tt0080684", "tt0167261",
            "tt0073486", "tt0099685", "tt0133093", "tt0047478", "tt0114369",
            "tt0317248", "tt0076759", "tt0102926", "tt0038650", "tt0118799",
            "tt0120815", "tt0245429", "tt0120689", "tt0816692", "tt0114814",
            "tt0110413", "tt0056058", "tt0088763", "tt0103064", "tt0027977",
            "tt0120586", "tt0253474", "tt0407887", "tt0172495", "tt0482571"
        ]
        
        random_id = random.choice(popular_movies)
        return await self.omdb_get_movie(imdb_id=random_id)
    
    # ============ TMDB API Methods ============
    async def tmdb_search(self, query: str):
        """Search for a movie using TMDB API"""
        if not AMANBOTZ_TMDB_API:
            return None
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.tmdb_base}/search/movie"
            params = {
                "api_key": AMANBOTZ_TMDB_API,
                "query": query
            }
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("results", [])
        return None
    
    async def tmdb_get_movie(self, movie_id: int):
        """Get movie details from TMDB"""
        if not AMANBOTZ_TMDB_API:
            return None
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.tmdb_base}/movie/{movie_id}"
            params = {"api_key": AMANBOTZ_TMDB_API}
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
        return None
    
    async def tmdb_get_new_releases(self):
        """Get new movie releases from TMDB"""
        if not AMANBOTZ_TMDB_API:
            return None
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.tmdb_base}/movie/now_playing"
            params = {"api_key": AMANBOTZ_TMDB_API}
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("results", [])
        return None
    
    async def tmdb_get_tv_releases(self):
        """Get new TV series releases from TMDB"""
        if not AMANBOTZ_TMDB_API:
            return None
        
        async with aiohttp.ClientSession() as session:
            url = f"{self.tmdb_base}/tv/on_the_air"
            params = {"api_key": AMANBOTZ_TMDB_API}
            async with session.get(url, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get("results", [])
        return None
    
    def get_tmdb_poster_url(self, poster_path: str):
        """Get full poster URL from TMDB"""
        if poster_path:
            return f"{self.tmdb_image_base}{poster_path}"
        return None
    
    # ============ Combined Methods ============
    async def search_movie(self, query: str):
        """Search for a movie using available API"""
        # Prefer OMDB if available
        if "omdb" in self.available_apis:
            results = await self.omdb_search(query)
            if results:
                return {"source": "omdb", "results": results}
        
        # Fall back to TMDB
        if "tmdb" in self.available_apis:
            results = await self.tmdb_search(query)
            if results:
                return {"source": "tmdb", "results": results}
        
        return None
    
    async def get_movie_details(self, movie_id: str = None, title: str = None, source: str = None):
        """Get movie details from available API"""
        # If source is specified, use that API
        if source == "omdb" and "omdb" in self.available_apis:
            return await self.omdb_get_movie(imdb_id=movie_id, title=title)
        elif source == "tmdb" and "tmdb" in self.available_apis:
            return await self.tmdb_get_movie(int(movie_id))
        
        # Otherwise, try available APIs
        if "omdb" in self.available_apis and (movie_id or title):
            result = await self.omdb_get_movie(imdb_id=movie_id, title=title)
            if result:
                return result
        
        if "tmdb" in self.available_apis and movie_id:
            return await self.tmdb_get_movie(int(movie_id))
        
        return None
    
    async def get_random_poster(self):
        """Get a random movie poster for start page"""
        if "omdb" in self.available_apis:
            movie = await self.omdb_get_random_movie()
            if movie and movie.get("Poster") and movie.get("Poster") != "N/A":
                return {
                    "title": movie.get("Title", "Unknown"),
                    "year": movie.get("Year", "N/A"),
                    "poster": movie.get("Poster"),
                    "rating": movie.get("imdbRating", "N/A"),
                    "source": "omdb"
                }
        
        # Fallback for TMDB
        if "tmdb" in self.available_apis:
            releases = await self.tmdb_get_new_releases()
            if releases:
                movie = random.choice(releases)
                return {
                    "title": movie.get("title", "Unknown"),
                    "year": movie.get("release_date", "N/A")[:4] if movie.get("release_date") else "N/A",
                    "poster": self.get_tmdb_poster_url(movie.get("poster_path")),
                    "rating": str(movie.get("vote_average", "N/A")),
                    "source": "tmdb"
                }
        
        return None
    
    async def get_new_releases(self):
        """Get new movie and TV releases"""
        releases = []
        
        if "tmdb" in self.available_apis:
            movies = await self.tmdb_get_new_releases()
            if movies:
                for movie in movies:
                    releases.append({
                        "id": str(movie.get("id")),
                        "title": movie.get("title"),
                        "type": "movie",
                        "poster": self.get_tmdb_poster_url(movie.get("poster_path")),
                        "release_date": movie.get("release_date"),
                        "overview": movie.get("overview"),
                        "rating": movie.get("vote_average"),
                        "source": "tmdb"
                    })
            
            tv_shows = await self.tmdb_get_tv_releases()
            if tv_shows:
                for show in tv_shows:
                    releases.append({
                        "id": str(show.get("id")),
                        "title": show.get("name"),
                        "type": "tv",
                        "poster": self.get_tmdb_poster_url(show.get("poster_path")),
                        "release_date": show.get("first_air_date"),
                        "overview": show.get("overview"),
                        "rating": show.get("vote_average"),
                        "source": "tmdb"
                    })
        
        return releases
    
    def format_movie_details_omdb(self, movie: dict):
        """Format OMDB movie details for display"""
        return {
            "title": movie.get("Title", "Unknown"),
            "year": movie.get("Year", "N/A"),
            "rated": movie.get("Rated", "N/A"),
            "released": movie.get("Released", "N/A"),
            "runtime": movie.get("Runtime", "N/A"),
            "genre": movie.get("Genre", "N/A"),
            "director": movie.get("Director", "N/A"),
            "actors": movie.get("Actors", "N/A"),
            "plot": movie.get("Plot", "N/A"),
            "language": movie.get("Language", "N/A"),
            "country": movie.get("Country", "N/A"),
            "awards": movie.get("Awards", "N/A"),
            "poster": movie.get("Poster", ""),
            "imdb_rating": movie.get("imdbRating", "N/A"),
            "imdb_id": movie.get("imdbID", ""),
            "box_office": movie.get("BoxOffice", "N/A"),
            "source": "omdb"
        }
    
    def format_movie_details_tmdb(self, movie: dict):
        """Format TMDB movie details for display"""
        genres = ", ".join([g.get("name", "") for g in movie.get("genres", [])])
        return {
            "title": movie.get("title", "Unknown"),
            "year": movie.get("release_date", "N/A")[:4] if movie.get("release_date") else "N/A",
            "released": movie.get("release_date", "N/A"),
            "runtime": f"{movie.get('runtime', 'N/A')} min",
            "genre": genres,
            "plot": movie.get("overview", "N/A"),
            "language": movie.get("original_language", "N/A").upper(),
            "poster": self.get_tmdb_poster_url(movie.get("poster_path")),
            "rating": str(movie.get("vote_average", "N/A")),
            "budget": f"${movie.get('budget', 0):,}" if movie.get("budget") else "N/A",
            "revenue": f"${movie.get('revenue', 0):,}" if movie.get("revenue") else "N/A",
            "source": "tmdb"
        }


# Create API instance
amanbotz_api = AmanbotzMovieAPI()
