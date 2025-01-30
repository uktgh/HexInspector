import hashlib
import re

class HexViewer:
    def __init__(self, filepath):
        self.filepath = filepath

    def get_colored_hex_data(self):
        try:
            with open(self.filepath, "rb") as f:
                byte_data = f.read()
                return self.format_colored_hex(byte_data)
        except Exception as e:
            return f"Errore nel leggere il file: {str(e)}"

    def format_colored_hex(self, byte_data):
        hex_str = ""
        for i in range(0, len(byte_data), 16):
            hex_chunk = byte_data[i:i+16]
            offset = f"{i:08x}"
            hex_chunk_str = ' '.join([f"{b:02x}" for b in hex_chunk])
            ascii_chunk = ''.join([chr(b) if 32 <= b <= 126 else '.' for b in hex_chunk])

            # Colorazione dei valori esadecimali significativi
            hex_chunk_str_colored = self.color_hex_chunk(hex_chunk_str)

            hex_str += f"{offset}: {hex_chunk_str_colored:<48} | {ascii_chunk}\\\\n"
        return hex_str

    def color_hex_chunk(self, chunk):
        # Colorazione per diversi tipi di caratteri
        def colorize(match):
            byte_value = int(match.group(1), 16)
            if 32 <= byte_value <= 126:
                # ASCII printable characters
                return f"\033[92m{match.group(1)}\033[0m"
            elif byte_value < 32 or byte_value == 127:
                # Control characters
                return f"\033[91m{match.group(1)}\033[0m"
            else:
                # Non-printable characters
                return f"\033[93m{match.group(1)}\033[0m"
        
        return re.sub(r"([a-f0-9]{2})", colorize, chunk)

    def calculate_checksum(self, checksum_type):
        hash_func = None
        if checksum_type.lower() == "md5":
            hash_func = hashlib.md5
        elif checksum_type.lower() == "sha1":
            hash_func = hashlib.sha1
        elif checksum_type.lower() == "sha256":
            hash_func = hashlib.sha256
        else:
            return "Tipo di checksum non valido"

        with open(self.filepath, "rb") as f:
            file_data = f.read()
            return hash_func(file_data).hexdigest()

    def find_ascii_strings(self):
        with open(self.filepath, "rb") as f:
            byte_data = f.read()
            ascii_strings = re.findall(r'[ -~]{4,}', byte_data.decode('ascii', errors='ignore'))
            return "\\\\n".join(ascii_strings)

    def find_headers(self):
        # Placeholder per l'analisi degli header (per esempio per eseguibili)
        return "Header trovati: N/A"

    def search_pattern(self, pattern):
        if pattern is None:
            return "Pattern non valido: il pattern non può essere None"
        pattern_bytes = bytes.fromhex(pattern)
        with open(self.filepath, "rb") as f:
            byte_data = f.read()
            positions = [i for i in range(len(byte_data)) if byte_data[i:i+len(pattern_bytes)] == pattern_bytes]
            return f"Pattern trovato a: {', '.join(map(str, positions))}"

    def check_integrity(self):
        # Placeholder per la verifica dell'integrità del file
        return "Integrità verificata."

    def analyze_compression(self):
        # Placeholder per analizzare la compressione
        return "Compressione: N/A"