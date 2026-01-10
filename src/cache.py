import json
import os
from pathlib import Path
from typing import Optional
from config import CACHE_FILE

def load_cache() -> dict:
    """
    Load onset cache from disk.
    
    Returns:
        Dictionary mapping file paths to onset data
    """
    if Path(CACHE_FILE).exists():
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Cache file corrupted")
            return {}
    else:
        return {}

def save_cache(cache: dict) -> None:
    """
    Save onset cache to disk.
    
    Args:
        cache: Dictionary of onset data to save
    """
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Failed to save cache: {e}")

def get_cached_onsets(file_path: str, cache: dict) -> Optional[dict]:
    """
    Get cached onset data for a file if valid.
    
    Args:
        file_path: Path to audio file
        cache: Current cache dictionary
        
    Returns:
        Cached data dict or None if invalid/missing
        Format: {"duration": float, "onsets": [float], "bpm": float, beats: list[float] "last_modified": int}
    """
    if file_path not in cache:
        return None

    cached_data = cache[file_path]

    try:
        current = os.path.getmtime(file_path)
        cached_time = cached_data["last_modified"]

        if current != cached_time:
            return None

        return cached_data
    except (FileNotFoundError, KeyError):
        return None

def update_cache(file_path: str, duration: float, onsets: list[float], bpm: float, beats: list[float], cache: dict) -> None:
    """
    Add/update onset data for a file in cache.
    
    Args:
        file_path: Path to audio file
        duration: Duration in seconds
        onsets: List of onset times in seconds
        cache: Cache dictionary to update
    """
    current = os.path.getmtime(file_path)
    file_dict = {"duration": duration,
                 "onsets": onsets,
                 "beats": beats,
                 "last_modified": current,
                 "bpm": bpm}
    cache[file_path] = file_dict
