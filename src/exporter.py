from pydub import AudioSegment
from pathlib import Path
import os
from datetime import datetime

def export_excerpt(audio: AudioSegment, original_path: str, start: float, end: float, output_folder: str) -> str:
    """
    Export audio excerpt to file.
    
    Args:
        audio: AudioSegment containing the excerpt
        original_path: Path to original audio file
        start: Start time of excerpt
        end: End time of excerpt
        output_folder: Where to save exports
        
    Returns:
        Path to exported file
    """

def generate_export_filename(original_path: str, start: float, end: float) -> str:
    """
    Generate descriptive filename for export.
    Format: "originalname_0m23s-0m28s_timestamp.wav"
    
    Args:
        original_path: Original file path
        start: Start time
        end: End time
        
    Returns:
        Filename string
    """

def ensure_export_folder(folder: str) -> None:
    """
    Create export folder if it doesn't exist.
    
    Args:
        folder: Path to export folder
    """