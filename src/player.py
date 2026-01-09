from pydub import AudioSegment
import simpleaudio as sa
from typing import Optional
import os

AudioSegment.converter = r"C:\ffmpeg\bin\ffmpeg.exe"
AudioSegment.ffprobe = r"C:\ffmpeg\bin\ffprobe.exe"

os.environ["PATH"] += os.pathsep + r"C:\ffmpeg\bin"

class ExcerptPlayer:
    """Handles audio loading, slicing, and playback."""
    
    def __init__(self):
        self.current_audio: Optional[AudioSegment] = None
        self.playback_obj: Optional[sa.PlayObject] = None
        self.file_path: str = ""
        self.start_time: float = 0.0
        self.end_time: float = 0.0
    
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
        if self.playback_obj is not None:
            self.playback_obj.stop()

        self.playback_obj = sa.play_buffer(
            self.current_audio.raw_data,
            num_channels=self.current_audio.channels,
            bytes_per_sample=2,
            sample_rate=self.current_audio.frame_rate
            )

    
    def stop(self) -> None:
        """
        Stop current playback.
        """
        if self.playback_obj is not None:
            self.playback_obj.stop()
            self.playback_obj = None

    
    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
        if self.playback_obj is not None:
            return self.playback_obj.is_playing()
        return False

    
    def get_info(self) -> dict:
        """
        Get current excerpt information.
        
        Returns:
            Dict with file_path, start_time, end_time
        """
        return {
            "file_path": self.file_path,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
    


if __name__ == "__main__":
    player = ExcerptPlayer()
    
    # Use a real file path from your music library
    test_file = r"C:\Users\seamu\OneDrive\Desktop\Music\HOME - Before The Night (FLAC)\nnmmmmn!.wav"
    
    print("Loading excerpt...")
    player.load_excerpt(test_file, start=10.0, end=15.0)
    
    info = player.get_info()
    print(f"Loaded: {info['file_path']}")
    print(f"Time: {info['start_time']:.2f}s - {info['end_time']:.2f}s")
    
    print("\nPlaying 5-second excerpt...")
    player.play()
    
    import time
    time.sleep(2)
    print(f"Is still playing? {player.is_playing()}")
    
    time.sleep(3)
    print(f"Is still playing? {player.is_playing()}")
    
    print("\nStopping...")
    player.stop()
    print("Done!")