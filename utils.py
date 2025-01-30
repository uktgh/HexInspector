import os
import time
import pwd
import grp

def get_file_metadata(filepath):
    try:
        stats = os.stat(filepath)
        metadata = (
            f"Nome file: {os.path.basename(filepath)}\\n"
            f"Dimensione: {stats.st_size} byte\\n"
            f"Data creazione: {time.ctime(stats.st_ctime)}\\n"
            f"Ultima modifica: {time.ctime(stats.st_mtime)}\\n"
            f"Permessi: {oct(stats.st_mode)[-3:]}\\n"
            f"Proprietario: {pwd.getpwuid(stats.st_uid).pw_name}\\n"
            f"Gruppo: {grp.getgrgid(stats.st_gid).gr_name}"
        )
        return metadata
    except Exception as e:
        return f"Errore nel recuperare i metadati: {str(e)}"