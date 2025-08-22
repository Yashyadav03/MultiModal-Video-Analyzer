import os
import tempfile
from typing import Optional

def create_temp_file(suffix: str = ".mp3") -> str:
    """Create a temporary file and return its path"""
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    temp_path = temp_file.name
    temp_file.close()
    return temp_path

def cleanup_file(file_path: str) -> None:
    """Delete a file if it exists"""
    if os.path.exists(file_path):
        os.unlink(file_path)