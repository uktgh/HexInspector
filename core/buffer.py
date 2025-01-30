import ctypes

from typing import Optional

class MemoryBuffer:
    def __init__(self, initial_size: int = 1024 * 1024):
        self._buffer = (ctypes.c_ubyte * initial_size)()
        self._size = 0
        self._capacity = initial_size
        
    def extend(self, data: bytes) -> None:
        new_size = self._size + len(data)

        if new_size > self._capacity:
            new_capacity = max(self._capacity * 2, new_size)
            new_buffer = (ctypes.c_ubyte * new_capacity)()
            ctypes.memmove(new_buffer, self._buffer, self._size)

            self._buffer = new_buffer
            self._capacity = new_capacity

        ctypes.memmove(ctypes.byref(self._buffer, self._size), data, len(data))
        self._size = new_size

    def set_data(self, data: bytes) -> None:
        self._size = len(data)

        if self._size > self._capacity:
            self._capacity = self._size
            self._buffer = (ctypes.c_ubyte * self._capacity)()

        ctypes.memmove(self._buffer, data, self._size)

    def __getitem__(self, key: slice) -> memoryview:
        if isinstance(key, slice):
            start = key.start or 0
            stop = min(key.stop or self._size, self._size)
            
            return memoryview(self._buffer)[start:stop]

        raise TypeError("only slicing is supported")