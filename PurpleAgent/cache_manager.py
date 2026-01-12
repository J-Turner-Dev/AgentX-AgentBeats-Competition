"""
Simple file-based cache to avoid repeated API calls during development.
Saves money (well, would if we weren't using FREE APIs!)
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Any


class CacheManager:
    """Manages caching of API responses"""

    def __init__(self, cache_dir: str = "../data/cache"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_cache_key(self, key: str) -> str:
        """Generate cache filename from key"""
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Retrieve from cache"""
        cache_file = self.cache_dir / f"{self._get_cache_key(key)}.json"

        if cache_file.exists():
            try:
                with open(cache_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return None

        return None

    def set(self, key: str, value: Any):
        """Store in cache"""
        cache_file = self.cache_dir / f"{self._get_cache_key(key)}.json"

        try:
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(value, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not cache: {e}")

    def clear(self):
        """Clear all cache"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
        print("Cache cleared!")
