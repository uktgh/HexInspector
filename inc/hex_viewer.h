#ifndef HEX_VIEWER_H
#define HEX_VIEWER_H

#include <cstdint>
#include <string>

void hex_dump(const uint8_t* data, size_t size, int start_row);
void search_pattern(const uint8_t* data, size_t size, const std::string& pattern);

#endif
