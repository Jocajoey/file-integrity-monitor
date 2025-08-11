"""
Models: data models for the application.
Checklist:
1. Define Filerecord data class for storing metadata and hash
2. Define Diff dataclass to store differences between two file records
3.Create a type alias for readability
"""

from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass(frozen=True )
class Filerecord:
    """Data class to store file metadata and hash."""
    path: str
    hash: str
    mtime: float
    sha256: str
    
    Manifest = Dict[str, Filerecord] #map relative paths to Filerecords
    
    @dataclass
    class Diff:
        """Data class to store differences between two file records."""
        added: List[Filerecord]
        removed: List[Filerecord]
        modified: List[Tuple[Filerecord, Filerecord]]
        unchanged: List[Filerecord]
        