from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa
from typing import Optional

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
    
    def play(self) -> None:
        """
        Play the loaded excerpt (non-blocking).
        """
    
    def stop(self) -> None:
        """
        Stop current playback.
        """
    
    def is_playing(self) -> bool:
        """
        Check if audio is currently playing.
        
        Returns:
            True if playing, False otherwise
        """
    
    def get_info(self) -> dict:
        """
        Get current excerpt information.
        
        Returns:
            Dict with file_path, start_time, end_time
        """