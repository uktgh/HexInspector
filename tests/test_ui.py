import unittest
from unittest.mock import patch, MagicMock
from src.ui import open_file, save_file

class TestUI(unittest.TestCase):

    @patch("src.ui.filedialog.askopenfilename", return_value="test_file.bin")
    @patch("src.ui.hex_inspector", return_value="Data in hex format")
    def test_open_file(self, mock_hex_inspector, mock_askopenfilename):
        with patch("src.ui.text_box") as mock_text_box:
            open_file()
            mock_askopenfilename.assert_called_once()
            mock_text_box.delete.assert_called_with(1.0, "end")
            mock_text_box.insert.assert_called_with("end", "Data in hex format")

    @patch("src.ui.filedialog.asksaveasfilename", return_value="output.txt")
    @patch("builtins.open", MagicMock())
    def test_save_file(self):
        with patch("src.ui.text_box") as mock_text_box:
            mock_text_box.get.return_value = "Data to save"
            save_file()
            open.assert_called_with("output.txt", "w")
            open().write.assert_called_with("Data to save")

if __name__ == "__main__":
    unittest.main()
