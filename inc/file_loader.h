#ifndef FILE_LOADER_H
#define FILE_LOADER_H

#include <string>
#include <cstdint>
#include <sys/types.h>

uint8_t* load_exe(const std::string& path, size_t& size);
void print_file_metadata(const std::string& path);

#endif
