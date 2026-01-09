import random
import librosa
from typing import Tuple, Optional

def get_audio_info(file_path: str, cache: dict) -> Tuple[float, list[float]]:
    """
    Get duration and onset times for an audio file.
    Uses cache if available, otherwise analyzes file.
    
    Args:
        file_path: Path to audio file
        cache: Onset cache dictionary
        
    Returns:
        Tuple of (duration, onsets_list)
    """

    return detect_onsets(file_path)


def detect_onsets(file_path: str) -> Tuple[float, list[float]]:
    """
    Analyze audio file for onset times using librosa.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Tuple of (duration, list of onset times in seconds)
    """


def choose_random_excerpt(file_path: str, excerpt_length: float, cache: dict) -> Tuple[float, float]:
    """
    Choose a random excerpt starting at an onset (if available).
    
    Args:
        file_path: Path to audio file
        excerpt_length: Desired excerpt length in seconds
        cache: Onset cache dictionary
        
    Returns:
        Tuple of (start_time, end_time) in seconds
    """

    duration_onsets = get_audio_info(file_path, cache)
    duration, onsets = duration_onsets
    random_excerpt = choose_excerpt_from_onsets(onsets, excerpt_length,duration)
    if random_excerpt is None:
        return fallback_random_excerpt(duration, excerpt_length)
    return random_excerpt

def choose_excerpt_from_onsets(onsets: list[float], excerpt_length: float, duration: float) -> Optional[Tuple[float, float]]:
    """
    Select a random onset as start point for excerpt.
    
    Args:
        onsets: List of onset times
        excerpt_length: Desired length
        duration: Total audio duration
        
    Returns:
        (start, end) times or None if no valid onsets
    """
    valid_onsets = [onset for onset in onsets if (onset <= duration - excerpt_length)]
    if not valid_onsets:
        print("list is empty")
        return None
    chosen = random.choice(valid_onsets)
    end = chosen + excerpt_length
    return (chosen, end)

def fallback_random_excerpt(duration: float, excerpt_length: float) -> Tuple[float, float]:
    """
    Choose random excerpt when no onsets available (ambient/pads).
    
    Args:
        duration: Audio duration
        excerpt_length: Desired length
        
    Returns:
        (start, end) times
    """
    max_start = max(0, duration - excerpt_length)
    start = random.uniform(0, max_start)
    end = start + excerpt_length
    return start, end

