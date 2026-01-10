"""Exporting File Module"""

from pathlib import Path
from datetime import datetime
from player import ExcerptPlayer

def export_excerpt(player: ExcerptPlayer, output_folder: str) -> str:
    """
    Export audio excerpt to file.

        
    Returns:
        Path to exported file
    """
    if player.current_audio is None:
        raise ValueError("No audio loaded")
    info = player.get_info()
    filename = generate_export_filename(info["file_path"])
    ensure_export_folder(output_folder)
    output_path = Path(output_folder) / filename
    player.current_audio.export(output_path, format="wav")
    return str(output_path)

def generate_export_filename(original_path: str) -> str:
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

    path_name = Path(original_path)
    file_name = f"{path_name.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
    return file_name

def ensure_export_folder(folder: str) -> None:
    """
    Create export folder if it doesn't exist.
    
    Args:
        folder: Path to export folder
    """
    path = Path(folder)
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
