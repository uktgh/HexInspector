#include <iostream>
#include <ncurses.h>
#include "../inc/menu.h"

void handle_user_input(uint8_t*& exe_data, size_t& exe_size) {
    std::string path;
    std::cout << "Enter the path to the EXE: ";
    std::cin >> path;

    // Carica il file EXE
    exe_data = load_exe(path, exe_size);

    if (exe_data == nullptr) {
        std::cerr << "Failed to load EXE." << std::endl;
        return;  // Uscita dalla funzione in caso di errore
    }

    // Esegui un dump esadecimale del file
    hex_dump(exe_data, exe_size, 0);

    // Cerca un pattern
    std::string pattern;
    std::cout << "Enter the pattern to search: ";
    std::cin >> pattern;
    search_pattern(exe_data, exe_size, pattern);

    // Stampa i metadati del file
    print_file_metadata(path);

    // Pulizia dei dati allocati dinamicamente
    delete[] exe_data;
}
