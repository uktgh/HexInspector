import os
import time

def get_file_metadata(filepath):
    try:
        stats = os.stat(filepath)
        metadata = (
            f"Nome file: {os.path.basename(filepath)}\n"
            f"Dimensione: {stats.st_size} byte\n"
            f"Data creazione: {time.ctime(stats.st_ctime)}\n"
            f"Ultima modifica: {time.ctime(stats.st_mtime)}\n"
            f"Permessi: {oct(stats.st_mode)[-3:]}"
        )
        return metadata
    except Exception as e:
        return f"Errore nel recuperare i metadati: {str(e)}"
