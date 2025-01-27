#ifndef UTILS_H
#define UTILS_H

#include <cstdint>
#include <cstddef>
#include <string>

void load_exe(const std::string& path, uint8_t*& data, size_t& size);
void hex_dump(const uint8_t* data, size_t size, size_t offset);
void search_pattern(const uint8_t* data, size_t size, const std::string& pattern);
void print_file_metadata(const std::string& path);

#endif
