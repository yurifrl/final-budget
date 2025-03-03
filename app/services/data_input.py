"""
Provides file management and iteration capabilities for bank statement files.
"""

from pathlib import Path
from typing import List, Iterator, Optional
from datetime import datetime


class DataInput:
    """
    Manages bank statement files with iteration and sorting capabilities.
    
    This handler maintains a collection of files in a specified directory,
    providing methods to access them by recency and iterate through them
    in a controlled manner.
    """
    
    def __init__(self, directory: str, file_pattern: str = "*.pdf"):
        # Store normalized path to prevent path-related issues
        self.directory = Path(directory).resolve()
        self.file_pattern = file_pattern
        self._refresh_files()
    
    def _refresh_files(self) -> None:
        """
        Updates the internal file list by scanning the directory.
        Files are sorted by modification time in descending order.
        """
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
            
        self._files = sorted(
            self.directory.glob(self.file_pattern),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
    
    @property
    def latest(self) -> Optional[Path]:
        """The most recently modified file in the directory."""
        self._refresh_files()
        return self._files[0] if self._files else None
    
    @property
    def oldest(self) -> Optional[Path]:
        """The oldest file in the directory."""
        self._refresh_files()
        return self._files[-1] if self._files else None
    
    def files_on_date(self, date: datetime) -> List[Path]:
        """Returns all files modified on the specified date."""
        self._refresh_files()
        target_date = date.date()
        return [
            f for f in self._files
            if datetime.fromtimestamp(f.stat().st_mtime).date() == target_date
        ]
    
    def __iter__(self) -> Iterator[Path]:
        """
        Enables iteration over files in chronological order (newest to oldest).
        
        Example:
            handler = FileHandler("statements/")
            for file in handler:
                process_file(file)
        """
        self._refresh_files()
        return iter(self._files)
    
    def __len__(self) -> int:
        """Returns the number of files in the directory."""
        return len(self._files) 