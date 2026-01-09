import sys
from scanner import scan_music_library
from cache import load_cache, save_cache
from selector import choose_random_excerpt
from player import ExcerptPlayer
from exporter import export_excerpt, ensure_export_folder
import random
from config import *

class MusicExcerptSampler:
    """Main application controller."""
    
    def __init__(self):
        self.files: list[str] = []
        self.cache: dict = {}
        self.player: ExcerptPlayer = ExcerptPlayer()
        self.current_file: str = ""
        
    def initialize(self) -> None:
        """
        Initialize application: scan library, load cache.
        """
    
    def select_random_excerpt(self) -> None:
        """
        Choose and load a random excerpt.
        """
    
    def toggle_playback(self) -> None:
        """
        Play or stop current excerpt.
        """
    
    def export_current(self) -> None:
        """
        Export current excerpt to file.
        """
    
    def show_menu(self) -> None:
        """
        Display terminal menu options.
        """
    
    def run(self) -> None:
        """
        Main application loop.
        """

def main():
    """Entry point."""
    app = MusicExcerptSampler()
    app.initialize()
    app.run()

if __name__ == "__main__":
    main()
```

**Menu Interface:**
```
=== Music Excerpt Sampler ===
Current: /path/to/song.mp3
Excerpt: 1:23 - 1:28 (5.0s)
Status: ⏸ Stopped

[R] Randomize new excerpt
[P] Play/Pause
[E] Export current excerpt
[Q] Quit

Enter choice: