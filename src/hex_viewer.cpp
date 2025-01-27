#include "../inc/hex_viewer.h"
#include <iostream>
#include <sstream>
#include <iomanip>

#define BYTES_PER_LINE 16

void hex_dump(const uint8_t* data, size_t size, int start_row) {
    int row = start_row;
    for (size_t i = 0; i < size; i += BYTES_PER_LINE) {
        std::stringstream ss;
        ss << std::hex << std::setfill('0');
        for (int j = 0; j < BYTES_PER_LINE && i + j < size; ++j) {
            ss << std::setw(2) << (int)data[i + j] << " ";
        }
        std::string line = ss.str();
        std::cout << line << std::endl;
        row++;
    }
}

void search_pattern(const uint8_t* data, size_t size, const std::string& pattern) {
    std::stringstream ss;
    for (size_t i = 0; i < size - pattern.size(); ++i) {
        bool found = true;
        for (size_t j = 0; j < pattern.size(); ++j) {
            if (data[i + j] != pattern[j]) {
                found = false;
                break;
            }
        }
        if (found) {
            ss << "Pattern found at offset: 0x" << std::hex << i << std::endl;
        }
    }
    std::cout << ss.str();
}
