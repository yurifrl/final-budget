from pathlib import Path
from typing import List, Iterator, Optional, Dict
from datetime import datetime
from enum import Enum


class FileType(Enum):
    FATURA = "fatura"
    EXTRATO = "extrato"
    UNKNOWN = "unknown"


class DataInput:
    def __init__(self, directory: str, file_pattern: str = "*.pdf"):
        self.directory = Path(directory).resolve()
        self.file_pattern = file_pattern
        self._refresh_files()
    
    def _get_file_type(self, file_path: Path) -> FileType:
        name = file_path.name.lower()
        
        if "fatura" in name:
            return FileType.FATURA
            
        if "extrato" in name:
            return FileType.EXTRATO
            
        return FileType.UNKNOWN
    
    def _refresh_files(self) -> None:
        if not self.directory.exists():
            self.directory.mkdir(parents=True)
            
        self._files = sorted(
            self.directory.glob(self.file_pattern),
            key=lambda x: x.stat().st_mtime,
            reverse=True
        )
        
        self._file_types: Dict[Path, FileType] = {}
        for file in self._files:
            self._file_types[file] = self._get_file_type(file)
    
    @property
    def latest(self) -> Optional[Path]:
        self._refresh_files()
        return self._files[0] if self._files else None
    
    @property
    def oldest(self) -> Optional[Path]:
        self._refresh_files()
        return self._files[-1] if self._files else None
    
    def files_on_date(self, date: datetime) -> List[Path]:
        self._refresh_files()
        target_date = date.date()
        return [
            f for f in self._files
            if datetime.fromtimestamp(f.stat().st_mtime).date() == target_date
        ]
    
    def get_files_by_type(self, file_type: FileType) -> List[Path]:
        self._refresh_files()
        return [
            f for f in self._files
            if self._file_types.get(f) == file_type
        ]
    
    def __iter__(self) -> Iterator[Path]:
        self._refresh_files()
        return iter(self._files)
    
    def __len__(self) -> int:
        return len(self._files) 