from functools import lru_cache
from typing import Dict

class HexCache:
    def __init__(self, capacity: int = 1000):
        self.capacity = capacity
        self._cache: Dict[int, str] = {}
        
    @lru_cache(maxsize=1024)
    def format_line(self, offset: int, data: bytes) -> str:
        hex_part = " ".join(f"{b:02x}" for b in data)
        ascii_part = "".join(chr(b) if 32 <= b <= 126 else "." for b in data)
        return f"{offset:08x}: {hex_part:<48} |{ascii_part}|\n"