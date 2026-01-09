import json
import os
from pathlib import Path
from typing import Optional

def load_cache() -> dict:
    """
    Load onset cache from disk.
    
    Returns:
        Dictionary mapping file paths to onset data
    """

def save_cache(cache: dict) -> None:
    """
    Save onset cache to disk.
    
    Args:
        cache: Dictionary of onset data to save
    """

def get_cached_onsets(file_path: str, cache: dict) -> Optional[dict]:
    """
    Get cached onset data for a file if valid.
    
    Args:
        file_path: Path to audio file
        cache: Current cache dictionary
        
    Returns:
        Cached data dict or None if invalid/missing
        Format: {"duration": float, "onsets": [float], "last_modified": int}
    """

def update_cache(file_path: str, duration: float, onsets: list[float], cache: dict) -> None:
    """
    Add/update onset data for a file in cache.
    
    Args:
        file_path: Path to audio file
        duration: Duration in seconds
        onsets: List of onset times in seconds
        cache: Cache dictionary to update
    """