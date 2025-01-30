import unittest
from src.hashing import calculate_checksum
from src.file_utils import save_file
import os

class TestUtils(unittest.TestCase):

    def test_calculate_checksum(self):
        file_path = 'test_file.bin'
        with open(file_path, 'wb') as f:
            f.write(b"Hello World!")
        
        checksum = calculate_checksum(file_path, 'sha256')
        self.assertTrue(len(checksum) > 0)

    def test_save_file(self):
        file_path = 'test_save.bin'
        data = b"Sample Data"
        save_file(file_path, data)
        self.assertTrue(os.path.exists(file_path))

if __name__ == '__main__':
    unittest.main()
