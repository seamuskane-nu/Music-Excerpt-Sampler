import sys
import random
from pathlib import Path

# Your modules
from scanner import scan_music_library
from selector import choose_random_excerpt
from player import ExcerptPlayer
from config import MUSIC_FOLDER, EXCERPT_LENGTH, CACHE_FILE

class MusicExcerptSampler:
    def __init__(self):
        # Initialize all the components
        self.files: list[str] = []
        self.cache: dict = {}
        self.player: ExcerptPlayer = ExcerptPlayer()
        self.current_file: str = ""
        self.is_playing: bool = False

    def initialize(self):
        # Scan library, load cache
        print("Scanning music library...")
        self.files = scan_music_library()
        if self.files is None:
            sys.exit
        print(f"{len(self.files)} found!")

    def select_random_excerpt(self):
        # Pick random file + random excerpt
        random_file = random.choice(self.files)
        start, end = choose_random_excerpt(random_file, EXCERPT_LENGTH)
        self.player.load_excerpt(random_file, start, end)
        self.current_file = random_file
        print(f"{random_file} was selected")

    def toggle_playback(self):
        # Play or pause
        if self.current_file is "":
            print("nothing loaded")
            return
        if self.player.is_playing():
            self.player.stop()
            self.is_playing = False
        else:
            self.player.play()
            self.is_playing = True

    #def export_current(self):
        # Save excerpt to file
        
    def change_volume(self, adjustment):
        # Increase/decrease volume
        current_volume = self.player.get_volume_percent()
        new_volume = max(0.0, min(1.0, (adjustment + current_volume)))
        self.player.set_volume_percent(new_volume)

    def show_menu(self):
        # Display current state and options
        info = self.player.get_info()
        if self.is_playing is False:
            playing = "Paused"
        else:
            playing = "Playing"
        print("=== Music Excerpt Sampler ===")
        print(f"Current: {info["file_path"]}")

        print(f"Excerpt: {info["start_time"]} - {info["end_time"]} [{EXCERPT_LENGTH}s]")
        print(f"Status: {playing}")
        print(f"Volume: {self.player.get_volume_percent()}")

        print("\n[R] Randomize new excerpt")
        print("[P] Play/Pause")
        print("[+] Volume up   [-] Volume down")
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
                self.toggle_playback
            elif choice == '+':
                self.change_volume(10)
            elif choice == '-':
                self.change_volume(-10)
            elif choice == 'e':
                print("export")
            elif choice == 'q':
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

