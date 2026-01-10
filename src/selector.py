"""Excerpt Selecting Module"""
from typing import Tuple, Optional
import random
import librosa
from cache import get_cached_onsets, update_cache


def get_audio_info(file_path: str, cache: dict) -> Tuple[float, list[float], float]:
    """
    Get duration and onset times for an audio file.
    Uses cache if available, otherwise analyzes file.
    
    Args:
        file_path: Path to audio file
        cache: Onset cache dictionary
        
    Returns:
        Tuple of (duration, onsets_list)
    """

    cached = get_cached_onsets(file_path, cache)
    if cached is not None:
        print("(using cached onsets)")
        return cached["duration"], cached["onsets"], cached["bpm"]

    print("(analyzing onsets)")
    duration, onsets = detect_onsets(file_path)
    beats, bpm = detect_beats(file_path)

    update_cache(file_path, duration, onsets, bpm, beats, cache)

    return duration, onsets, bpm

def get_beats_info(file_path: str, cache: dict) -> Tuple[list[float], float]:
    """
    Get beat positions and BPM from cache or detection.
    
    Args:
        file_path: Path to audio file
        cache: Cache dictionary
        
    Returns:
        Tuple of (beat_times, bpm)
    """
    cached = get_cached_onsets(file_path, cache)
    if cached is not None and "beats" in cached:
        return cached["beats"], cached["bpm"]

    beats, bpm = detect_beats(file_path)
    return beats, bpm


def detect_onsets(file_path: str) -> Tuple[float, list[float]]:
    """
    Analyze audio file for onset times using librosa.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Tuple of (duration, list of onset times in seconds)
    """

    y, sr = librosa.load(file_path, sr=None, mono=True)
    duration = librosa.get_duration(y=y, sr=sr)

    onsets = librosa.onset.onset_detect(
        y=y, sr=sr, units="time", backtrack=True
    )

    return duration, list(onsets)


def choose_random_excerpt_manual(
        file_path: str, excerpt_length: float, cache: dict) -> Tuple[float, float]:
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
    duration, onsets, _ = duration_onsets
    random_excerpt = choose_excerpt_from_onsets(onsets, excerpt_length,duration)
    if random_excerpt is None:
        return fallback_random_excerpt(duration, excerpt_length)
    return random_excerpt

def choose_random_excerpt_bars(
        file_path: str, cache: dict, num_bars: int = 4) -> Tuple[float, float, float]:
    """Choose excerpt based on BPM (N bars long)."""
    # Get BPM, calculate length, choose onset
    duration, onsets, bpm = get_audio_info(file_path, cache)
    excerpt_length = calculate_excerpt_length_from_bars(bpm, num_bars)
    random_excerpt = choose_excerpt_from_onsets(onsets, excerpt_length, duration)

    if random_excerpt is None:
        start, end =  fallback_random_excerpt(duration, excerpt_length)
        return start, end, bpm
    start, end = random_excerpt
    return start, end, bpm

def choose_random_excerpt_beats(
        file_path: str, cache: dict, num_bars: int = 2) -> Tuple[float, float, float]:
    """
    Choose excerpt aligned to beats (N beats long).
    
    Args:
        file_path: Path to audio file
        cache: Cache
        num_beats: Number of beats for excerpt
        
    Returns:
        (start_time, end_time, bpm)
    """
    duration, _, _ = get_audio_info(file_path, cache)
    beats, bpm = get_beats_info(file_path, cache)
    excerpt_length = calculate_excerpt_length_from_bars(bpm, num_bars)

    valid_beats = [beat for beat in beats if beat <= (duration - excerpt_length)]

    if not valid_beats:
        print("list is empty")
        start, end = fallback_random_excerpt(duration, excerpt_length)
        return start, end, bpm

    chosen = random.choice(valid_beats)

    end_time = chosen + excerpt_length

    return chosen, end_time, bpm

def choose_excerpt_from_onsets(
        onsets: list[float], excerpt_length: float, duration: float) -> Optional[
            Tuple[float, float]]:
    """
    Select a random onset as start point for excerpt.
    
    Args:
        onsets: List of onset times
        excerpt_length: Desired length
        duration: Total audio duration
        
    Returns:
        (start, end) times or None if no valid onsets
    """
    valid_onsets = [onset for onset in onsets if onset <= (duration - excerpt_length)]
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

def detect_bpm(file_path: str) -> float:
    """
    Detect tempo/BPM of audio file.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        BPM as float
    """
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
        tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

        bpm = float(tempo[0]) if len(tempo) > 0 else 120.0

        if bpm < 60 or bpm > 250:
            print(f"Warning : detected BPM {bpm:.1f} is out of range, using 120")
            bpm = 120
        return bpm
    except Exception as e:
        print(f"  Warning: BPM detection failed ({e}), using 120")
        return 120

def detect_beats(file_path: str) -> Tuple[list[float], float]:
    """
    Detect beat positions and BPM.
    
    Args:
        file_path: Path to audio file
        
    Returns:
        Tuple of (beat_times, bpm)
    """
    try:
        y, sr = librosa.load(file_path, sr=None, mono=True)
        tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
        beat_times = librosa.frames_to_time(beat_frames, sr=sr)

        bpm = float(tempo[0]) if len(tempo) > 0 else 120.0

        return list(beat_times), bpm

    except Exception as e:
        print(f"Beat detection failed: {e}")
        return [], 120.0

def calculate_excerpt_length_from_bars(bpm: float, num_bars: int = 4) -> float:
    """
    ASSUMES 4/4 TIME SIG! WONT WORK WITH OTHERS"""
    beats_per_bar = 4
    total_beats = beats_per_bar * num_bars
    return (total_beats * 60) / bpm
