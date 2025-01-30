import mmap
from typing import Generator
import os

class AsyncFileReader:
    def __init__(self, filename: str, chunk_size: int = 1024 * 1024):
        self.filename = filename
        self.chunk_size = chunk_size
        self._file = None
        self._mmap = None
        
    def __enter__(self):
        self._file = open(self.filename, 'rb')
        self._mmap = mmap.mmap(self._file.fileno(), 0, access=mmap.ACCESS_READ)
        return self
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._mmap:
            self._mmap.close()
        if self._file:
            self._file.close()
            
    def read_chunks(self) -> Generator[bytes, None, None]:
        for i in range(0, len(self._mmap), self.chunk_size):
            yield self._mmap[i:i + self.chunk_size]