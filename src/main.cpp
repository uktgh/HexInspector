#include <iostream>
#include <ncurses.h>
#include <cstdint>

#include "../inc/utils.h"

void handle_user_input(uint8_t* exe_data, size_t exe_size) {
    std::string path;
    std::cout << "Enter the path to the EXE: ";
    std::cin >> path;

    exe_data = load_exe(path, exe_data, exe_size);

    hex_dump(exe_data, exe_size, 0);

    std::string pattern;
    std::cout << "Enter the pattern to search: ";
    std::cin >> pattern;
    search_pattern(exe_data, exe_size, pattern);

    print_file_metadata(path);
}
