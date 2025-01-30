import zipfile
import gzip
import io

class CompressionHandler:
    def extract(self, filepath):
        extract_methods = {
            '.zip': self.extract_zip,
            '.gz': self.extract_gz
        }
        for ext, method in extract_methods.items():
            if filepath.endswith(ext):
                return method(filepath)
        raise ValueError(f"Unsupported file type for compression: {filepath}")

    def extract_zip(self, filepath):
        try:
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                return zip_ref.read(zip_ref.namelist()[0])  # Extract the first file
        except (zipfile.BadZipFile, IndexError) as e:
            raise RuntimeError(f"Failed to extract ZIP file: {e}")

    def extract_gz(self, filepath):
        try:
            with gzip.open(filepath, 'rb') as f:
                return f.read()
        except OSError as e:
            raise RuntimeError(f"Failed to extract GZ file: {e}")