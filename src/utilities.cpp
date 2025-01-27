#include <sstream>
#include <iomanip>
#include <cstdint>

#include "../inc/utilities.h"

std::string to_hex(const uint8_t* data, size_t size) {
    std::stringstream ss;
    for (size_t i = 0; i < size; ++i) {
        ss << std::setw(2) << std::setfill('0') << std::hex << (int)data[i] << " ";
    }
    return ss.str();
}
