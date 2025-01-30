import binascii

# Funzione per leggere e visualizzare il file in formato esadecimale
def hex_inspector(file_path):
    try:
        with open(file_path, "rb") as file:
            byte = file.read(16)  # Legge 16 byte alla volta
            offset = 0  # Posizione corrente nel file
            hex_data = []
            
            while byte:
                # Visualizzazione esadecimale
                hex_rep = ' '.join(f'{b:02X}' for b in byte)
                
                # Visualizzazione ASCII
                ascii_rep = ''.join(chr(b) if 32 <= b < 127 else '.' for b in byte)
                
                # Aggiungi la riga con offset, esadecimale e ASCII
                hex_data.append(f'{offset:08X}  {hex_rep:<47}  {ascii_rep}')
                
                offset += 16
                byte = file.read(16)
            
            return "\n".join(hex_data)
    
    except FileNotFoundError:
        raise FileNotFoundError("File non trovato.")
    except Exception as e:
        raise Exception(f"Errore: {e}")
