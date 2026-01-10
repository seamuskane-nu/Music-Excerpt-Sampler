from pydub import AudioSegment
import pygame
from typing import Optional
import os

#Uncomment on windows only
"""
AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"
os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"
"""

class ExcerptPlayer:
    """Handles audio loading, slicing, and playback."""
    
    def __init__(self):
        self.current_audio: Optional[AudioSegment] = None
        self.file_path: str = ""
        self.start_time: float = 0.0
        self.end_time: float = 0.0
        self.temp_file: str = "temp_excerpt.wav"
        self.volume: float = 0.75

        pygame.mixer.init()
        pygame.mixer.music.set_volume(self.volume)
    
    def load_excerpt(self, file_path: str, start: float, end: float) -> None:
        """
        Load and slice audio excerpt with fades.
        
        Args:
            file_path: Path to audio file
            start: Start time in seconds
            end: End time in seconds
        """
        audio = AudioSegment.from_file(file_path)

        audio = audio.set_sample_width(2)
        audio = audio.set_frame_rate(44100)
        audio = audio.set_channels(2)

        start_ms = int(start * 1000)
        end_ms = int(end * 1000)

        excerpt = audio[start_ms:end_ms]
        excerpt = excerpt.fade_in(5).fade_out(10)

        self.current_audio = excerpt
        self.file_path = file_path
        self.start_time = start
        self.end_time = end
    
    def play(self) -> None:
        """
        Play the loaded excerpt (non-blocking).
        """
        if self.current_audio is None:
            print("No audio loaded")
            return
        
        pygame.mixer.music.stop()

        self.current_audio.export(self.temp_file, format="wav")

        pygame.mixer.music.load(self.temp_file)
        pygame.mixer.music.play()

    
    def stop(self) -> None:
        """
        Stop current playback.
        """
        pygame.mixer.music.stop()

    
    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
        return pygame.mixer.music.get_busy()
    
    def set_volume(self, volume:float) -> None:
        """
        Docstring for set_volume
        
        :param self: Description
        :param volume: Description
        :type volume: float
        """
        volume = max(0.0, min(1.0, volume))
        self.volume = volume
        pygame.mixer.music.set_volume(volume)

    def set_volume_percent(self, percent: float) -> None:
        """
        Docstring for set_volume_percent
        
        :param self: Description
        :param percent: Description
        :type percent: float
        """
        self.set_volume(percent/100.0)

    def get_volume(self) -> None:
        """
        Docstring for get_volume
        
        :param self: Description
        """
        return self.volume
    
    def get_volume_percent(self) -> None:
        """
        Docstring for get_volume
        
        :param self: Description
        """
        return self.volume * 100
    
    def get_info(self) -> dict:
        """
        Get current excerpt information.
        
        Returns:
            Dict with file_path, start_time, end_time
        """
        return {
            "file_path": self.file_path,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "volume": self.volume
        }


if __name__ == "__main__":
    import time
    
    player = ExcerptPlayer()
    
    test_file = r"C:\Users\seamu\OneDrive\Desktop\Music\HOME - Before The Night (FLAC)\nnmmmmn!.wav"
    
    print("Loading excerpt...")
    player.load_excerpt(test_file, start=10.0, end=25.0)  # 15 second excerpt
    
    print("Playing with volume changes during playback...")
    player.play()
    
    # Change volume while playing
    for i in range(10):
        volume = 1.0 - (i * 0.1)  # Fade from 100% to 10%
        player.set_volume(volume)
        print(f"Volume: {volume*100:.0f}%")
        time.sleep(1.5)
    
    print("Done!")