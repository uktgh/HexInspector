#include <iostream>
#include <fstream>
#include <iomanip>
#include <cstring>
#include "utils.h"

// Carica il file EXE in memoria
uint8_t* load_exe(const std::string& path, size_t& size) {
    std::ifstream file(path, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << path << std::endl;
        return nullptr;  // Restituisce nullptr in caso di errore
    }

    size = file.tellg();  // Ottieni la dimensione del file
    file.seekg(0, std::ios::beg);

    uint8_t* data = new uint8_t[size];  // Allocazione dinamica per i dati
    file.read(reinterpret_cast<char*>(data), size);
    file.close();

    return data;  // Restituisci i dati letti
}


// Esegui il dump esadecimale del file
void hex_dump(const uint8_t* data, size_t size, size_t offset) {
    for (size_t i = 0; i < size; ++i) {
        if (i % 16 == 0) {
            std::cout << std::setw(8) << std::setfill('0') << std::hex << offset + i << ": ";
        }
        std::cout << std::setw(2) << std::setfill('0') << static_cast<int>(data[i]) << " ";
        if ((i + 1) % 16 == 0 || i == size - 1) {
            std::cout << std::endl;
        }
    }
}

// Cerca un pattern all'interno dei dati
void search_pattern(const uint8_t* data, size_t size, const std::string& pattern) {
    for (size_t i = 0; i < size - pattern.size(); ++i) {
        if (std::memcmp(&data[i], pattern.c_str(), pattern.size()) == 0) {
            std::cout << "Pattern found at offset: " << i << std::endl;
            return;
        }
    }
    std::cout << "Pattern not found." << std::endl;
}

// Stampa i metadati del file
void print_file_metadata(const std::string& path) {
    // Per semplicità, possiamo solo stampare il nome del file e la dimensione
    std::ifstream file(path, std::ios::binary | std::ios::ate);
    if (!file.is_open()) {
        std::cerr << "Error opening file: " << path << std::endl;
        return;
    }

    size_t size = file.tellg();
    std::cout << "File: " << path << std::endl;
    std::cout << "Size: " << size << " bytes" << std::endl;
    file.close();
}
