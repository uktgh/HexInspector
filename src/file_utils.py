import zipfile
import tarfile
import gzip
import shutil

def open_compressed_file(file_path):
    if file_path.endswith('.zip'):
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall("/tmp")
            return zip_ref.namelist()[0]
    elif file_path.endswith('.tar.gz') or file_path.endswith('.tgz'):
        with tarfile.open(file_path, "r:gz") as tar_ref:
            tar_ref.extractall("/tmp")
            return tar_ref.getnames()[0]
    elif file_path.endswith('.gz'):
        with gzip.open(file_path, 'rb') as f:
            file_path = '/tmp/tempfile'
            with open(file_path, 'wb') as out_file:
                out_file.write(f.read())
            return file_path
    else:
        return file_path  # Return the original path if not compressed

def save_file(file_path, data):
    with open(file_path, "wb") as file:
        file.write(data)
