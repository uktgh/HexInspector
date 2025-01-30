import zipfile
import gzip
import io

class CompressionHandler:
    def extract(self, filepath):
        if filepath.endswith('.zip'):
            return self.extract_zip(filepath)
        elif filepath.endswith('.gz'):
            return self.extract_gz(filepath)
        else:
            raise ValueError("Tipo di file non supportato per la compressione")

    def extract_zip(self, filepath):
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            file_content = zip_ref.read(zip_ref.namelist()[0])  # Estrai il primo file
        return file_content

    def extract_gz(self, filepath):
        with gzip.open(filepath, 'rb') as f:
            return f.read()
