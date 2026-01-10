import sys
import random
from pathlib import Path

# Your modules
from scanner import scan_music_library
from selector import choose_random_excerpt_bars, choose_random_excerpt_manual, choose_random_excerpt_beats
from player import ExcerptPlayer
from config import MUSIC_FOLDER, EXCERPT_LENGTH, CACHE_FILE, EXPORTS_FOLDER
from exporter import export_excerpt

class MusicExcerptSampler:
    def __init__(self):
        # Initialize all the components
        self.files: list[str] = []
        self.cache: dict = {}
        self.player: ExcerptPlayer = ExcerptPlayer()
        self.current_file: str = ""
        self.is_playing: bool = False

        self.last_mode_info: str = ""
        self.mode: str = "beat"
        # beat, bar, onset
        self.num_bars: int = 2

    def initialize(self):
        # Scan library, load cache
        from cache import load_cache

        print("Scanning music library...")
        self.files = scan_music_library()
        if self.files is None:
            sys.exit
        print(f"{len(self.files)} found!")
        print("Loading cache...")
        self.cache = load_cache()
        print(f"Caches has {len(self.cache)} entries")

    def toggle_mode(self):
        if self.mode == "beat":
            self.mode = "bar"
        elif self.mode == "bar":
            self.mode = "onset"
        elif self.mode == "onset":
            self.mode = "beat"

        if self.mode == "beat":
            print(f"→ Switched to beat locked mode with {self.num_bars} for length")
        elif self.mode == "bar":
            print(f"→ Switched to onset {self.num_bars}-bar mode)")
        else:
            print(f"→ Switched to manual onset mode ({EXCERPT_LENGTH}s fixed)")

    def select_random_excerpt(self):
        # Pick random file + random excerpt

        if self.player.is_playing():
            self.player.stop()

        random_file = random.choice(self.files)

        if self.mode == "beat":
            start, end, bpm = choose_random_excerpt_beats(
                random_file, self.cache, num_bars=self.num_bars)
            mode_info = f"beat-locked ({self.num_bars} bars) at {bpm:.1f} BPM"

        elif self.mode == "bar":
            start, end, bpm = choose_random_excerpt_bars(
                random_file, self.cache, num_bars=self.num_bars)
            mode_info = f"{self.num_bars} bar mode at {bpm:.1f} BPM"
        else:
            start, end = choose_random_excerpt_manual(random_file, EXCERPT_LENGTH, self.cache,)
            mode_info = f"manual onset mode ({EXCERPT_LENGTH}s)"

        self.player.load_excerpt(random_file, start, end)
        self.current_file = random_file

        duration = end - start
        self.last_mode_info = mode_info 
        print(f"{random_file} was selected")
        print(f"Excerpt: {duration:.2f}s ({mode_info})")

    def toggle_playback(self):
        # Play or pause
        if not self.current_file:
            print("nothing loaded")
            return
        if self.player.is_playing():
            self.player.stop()
            self.is_playing = False
        else:
            self.player.play()
            self.is_playing = True

    def export_current(self):
        # Save excerpt to file
        if self.current_file == "":
            print("Nothing loaded")
            return
        try:
            output_path = export_excerpt(self.player, EXPORTS_FOLDER)
            print(f"Exported to: {output_path}")
        except Exception as e:
            print(f"Export failed: {e}")

    def change_volume(self, adjustment):
        # Increase/decrease volume
        current_volume = self.player.get_volume_percent()
        new_volume = max(0.0, min(100.0, (adjustment + current_volume)))
        self.player.set_volume_percent(new_volume)

    def show_menu(self):
        # Display current state and options
        info = self.player.get_info()
        if self.is_playing is False:
            playing = "Paused"
        else:
            playing = "Playing"
        print("=== Music Excerpt Sampler ===")
        print(f"Current: {info['file_path']}")

        duration = info['end_time'] - info['start_time']

        if self.last_mode_info:
            print(f"Excerpt: {info['start_time']} - {info['end_time']} [{duration}s ({self.last_mode_info})]")
        else:
            print(f"Excerpt: {info['start_time']:.2f}s - {info['end_time']:.2f}s [{duration:.2f}s]")

        print(f"Status: {playing}")
        print(f"Volume: {self.player.get_volume_percent()}")

        print("\n[R] Randomize new excerpt")
        print("[P] Play/Pause")
        print("[+] Volume up   [-] Volume down")
        print("[B] Toggle mode")
        print("[E] Export current excerpt")
        print("[Q] Quit\n")


    def run(self):
        # Main loop - handle user input

        while True:
            self.show_menu()
            choice = input("Enter choice: ").lower().strip()

            if choice == 'r':
                self.select_random_excerpt()
            elif choice == 'p':
                self.toggle_playback()
            elif choice == '+':
                self.change_volume(10)
            elif choice == '-':
                self.change_volume(-10)
            elif choice == 'e':
                self.export_current()
            elif choice == 'b':
                self.toggle_mode()
            elif choice == 'q':
                from cache import save_cache
                print("Saving cache...")
                save_cache(self.cache)
                print("Bye!")
                break
            else:
                print("Invalid choice!")

def main():
    """Entry point."""
    app = MusicExcerptSampler()
    app.initialize()
    app.run()

if __name__ == "__main__":
    main()

