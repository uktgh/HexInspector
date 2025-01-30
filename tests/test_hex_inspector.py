import unittest
from src.hex_inspector import hex_inspector

class TestHexInspector(unittest.TestCase):

    def test_hex_inspector_valid_file(self):
        test_file = "test_file.bin"
        with open(test_file, "wb") as f:
            f.write(b"Hello World!")
        
        hex_output = hex_inspector(test_file)
        self.assertTrue("48 65 6C 6C 6F 20 57 6F" in hex_output)
    
    def test_hex_inspector_invalid_file(self):
        with self.assertRaises(FileNotFoundError):
            hex_inspector("non_existent_file.bin")

if __name__ == "__main__":
    unittest.main()
