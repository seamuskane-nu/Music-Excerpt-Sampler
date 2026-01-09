"""Scanner for audio files"""

from pathlib import Path
from config import MUSIC_FOLDER, SUPPORTED_FORMATS

def scan_music_library():
    """Scan folder for audio files."""
    print(f"Scanning {MUSIC_FOLDER}...")
    files = [
        str(p) for p in Path(MUSIC_FOLDER).rglob("*")
        if p.suffix.lower() in SUPPORTED_FORMATS
    ]
    print(f"Found {len(files)} audio files")
    return files