"""Caching system for API responses to reduce redundant API calls."""

import hashlib
import json
import logging
import os
import sqlite3
import time
from typing import Any, Dict, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Default cache configuration
DEFAULT_CACHE_SIZE_LIMIT = 1000  # Number of entries
DEFAULT_CACHE_AGE_LIMIT = 7 * 24 * 60 * 60  # 7 days in seconds
DEFAULT_CACHE_DB_PATH = os.path.expanduser("~/.quizcraft/cache.db")


class ResponseCache:
    """Cache for storing and retrieving API responses."""
    
    def __init__(
        self,
        db_path: Optional[str] = None,
        size_limit: int = DEFAULT_CACHE_SIZE_LIMIT,
        age_limit: int = DEFAULT_CACHE_AGE_LIMIT,
    ):
        """
        Initialize the response cache.
        
        Args:
            db_path: Path to the SQLite database file
            size_limit: Maximum number of cache entries
            age_limit: Maximum age of cache entries in seconds
        """
        # If no path is provided, use the default
        self.db_path = db_path or os.environ.get("CACHE_DB_PATH", DEFAULT_CACHE_DB_PATH)
        self.size_limit = int(os.environ.get("CACHE_SIZE_LIMIT", size_limit))
        self.age_limit = age_limit
        
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Initialize database
        self._init_db()
    
    def _init_db(self) -> None:
        """Initialize the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create table if it doesn't exist
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS response_cache (
            hash TEXT PRIMARY KEY,
            prompt TEXT,
            response TEXT,
            timestamp INTEGER,
            metadata TEXT
        )
        ''')
        
        # Create index for faster pruning
        cursor.execute('CREATE INDEX IF NOT EXISTS timestamp_idx ON response_cache (timestamp)')
        
        conn.commit()
        conn.close()
        
    def _calculate_hash(self, prompt: str, params: Dict[str, Any]) -> str:
        """
        Calculate a hash for the prompt and parameters.
        
        Args:
            prompt: The prompt text
            params: Dictionary of parameters
            
        Returns:
            MD5 hash as a string
        """
        # Convert parameters to a consistent string representation
        param_str = json.dumps(params, sort_keys=True)
        
        # Combine prompt and parameters
        combined = f"{prompt}|{param_str}"
        
        # Calculate MD5 hash
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, prompt: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Get a cached response if it exists and is not too old.
        
        Args:
            prompt: The prompt text
            params: Dictionary of parameters
            
        Returns:
            Cached response or None if not found
        """
        hash_key = self._calculate_hash(prompt, params)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute(
            'SELECT response, timestamp FROM response_cache WHERE hash = ?',
            (hash_key,)
        )
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            return None
            
        response_str, timestamp = result
        
        # Check if cache entry is too old
        if time.time() - timestamp > self.age_limit:
            logger.info(f"Cache hit, but entry too old. Hash: {hash_key}")
            self.delete(prompt, params)
            return None
            
        try:
            # Parse the JSON response
            response = json.loads(response_str)
            logger.info(f"Cache hit. Hash: {hash_key}")
            return response
        except json.JSONDecodeError:
            logger.warning(f"Failed to parse cached response. Hash: {hash_key}")
            return None
    
    def set(
        self,
        prompt: str,
        params: Dict[str, Any],
        response: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store a response in the cache.
        
        Args:
            prompt: The prompt text
            params: Dictionary of parameters
            response: The response to cache
            metadata: Optional metadata about the request
        """
        hash_key = self._calculate_hash(prompt, params)
        timestamp = int(time.time())
        
        # Convert response and metadata to JSON strings
        response_str = json.dumps(response)
        metadata_str = json.dumps(metadata or {})
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Insert or replace cache entry
        cursor.execute(
            'INSERT OR REPLACE INTO response_cache VALUES (?, ?, ?, ?, ?)',
            (hash_key, prompt, response_str, timestamp, metadata_str)
        )
        
        # Prune cache if necessary
        self._prune_cache(cursor)
        
        conn.commit()
        conn.close()
        
        logger.info(f"Added entry to cache. Hash: {hash_key}")
    
    def delete(self, prompt: str, params: Dict[str, Any]) -> bool:
        """
        Delete a specific cache entry.
        
        Args:
            prompt: The prompt text
            params: Dictionary of parameters
            
        Returns:
            True if an entry was deleted, False otherwise
        """
        hash_key = self._calculate_hash(prompt, params)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM response_cache WHERE hash = ?', (hash_key,))
        deleted = cursor.rowcount > 0
        
        conn.commit()
        conn.close()
        
        if deleted:
            logger.info(f"Deleted cache entry. Hash: {hash_key}")
            
        return deleted
    
    def clear(self) -> int:
        """
        Clear all cache entries.
        
        Returns:
            Number of entries deleted
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM response_cache')
        deleted = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        logger.info(f"Cleared cache. Deleted {deleted} entries.")
        return deleted
    
    def _prune_cache(self, cursor: sqlite3.Cursor) -> None:
        """
        Prune the cache if it exceeds the size limit.
        
        Args:
            cursor: SQLite cursor to use
        """
        # Get current cache size
        cursor.execute('SELECT COUNT(*) FROM response_cache')
        current_size = cursor.fetchone()[0]
        
        # If we're under the limit, nothing to do
        if current_size <= self.size_limit:
            return
            
        # Calculate how many entries to remove
        to_remove = current_size - self.size_limit
        
        # Delete oldest entries
        cursor.execute(
            'DELETE FROM response_cache WHERE hash IN '
            '(SELECT hash FROM response_cache ORDER BY timestamp ASC LIMIT ?)',
            (to_remove,)
        )
        
        logger.info(f"Pruned {to_remove} oldest entries from cache.")
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the cache.
        
        Returns:
            Dictionary with cache statistics
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM response_cache')
        total_entries = cursor.fetchone()[0]
        
        cursor.execute('SELECT MIN(timestamp), MAX(timestamp) FROM response_cache')
        min_timestamp, max_timestamp = cursor.fetchone()
        
        if min_timestamp and max_timestamp:
            oldest = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(min_timestamp))
            newest = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(max_timestamp))
        else:
            oldest = newest = "N/A"
        
        conn.close()
        
        return {
            "total_entries": total_entries,
            "size_limit": self.size_limit,
            "age_limit_days": self.age_limit / (24 * 60 * 60),
            "oldest_entry": oldest,
            "newest_entry": newest,
            "db_path": self.db_path
        }