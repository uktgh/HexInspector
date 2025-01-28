// include/hex_inspector.h
#pragma once
#include <vector>
#include <string>
#include <map>
#include <ctime>
#include <cstdint>

class HexInspector {
public:
    explicit HexInspector(const std::string& path = "");

    void load_file();
    void display_hex_dump();

private:
    static constexpr size_t BYTES_PER_LINE = 16;
    static constexpr size_t LINES_PER_PAGE = 20;

    std::string file_path;
    std::vector<unsigned char> file_data;
    size_t current_page;

    struct FileMetadata {
        size_t fileSize;
        std::time_t modificationTime;
        std::map<unsigned char, size_t> byteFrequency;
        double entropy;
    } metadata;

    void clear_screen() const;
    void print_hex_line(size_t offset, size_t length, size_t highlight_index = SIZE_MAX) const;
    void print_footer() const;
    void export_hex(const std::string& output_file_path) const;
    void display_strings() const;
    void display_metadata() const;
    std::string get_color_for_byte(unsigned char byte) const;
    void calculate_metadata();
};