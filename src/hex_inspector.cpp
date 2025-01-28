#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <cmath>
#include <algorithm>
#include <cctype>
#include <cstdlib>

#include "inc/hex_inspector.h"
#include "inc/constants.h"

HexInspector::HexInspector(const std::string& path) : file_path(path), current_page(0) {
    if (!file_path.empty()) {
        load_file();
    }
}

void HexInspector::load_file() {
    std::ifstream file(file_path, std::ios::binary);
    if (!file) {
        throw std::runtime_error(HexConstants::ERROR_FILE_NOT_FOUND);
    }

    file_data.assign(std::istreambuf_iterator<char>(file),
                    std::istreambuf_iterator<char>());
    
    if (file_data.size() > HexConstants::MAX_FILE_SIZE_WARNING) {
        std::cout << HexConstants::ERROR_FILE_TOO_LARGE << std::endl;
    }

    calculate_metadata();
}

void HexInspector::clear_screen() const {
    #ifdef _WIN32
        system("cls");
    #else
        system("clear");
    #endif
}

std::string HexInspector::get_color_for_byte(unsigned char byte) const {
    if (byte == 0x00) return HexConstants::RED;
    if (byte == 0xFF) return HexConstants::YELLOW;
    if (std::isprint(byte)) return HexConstants::GREEN;
    if (byte >= 0x7F) return HexConstants::MAGENTA;
    return HexConstants::RESET;
}

void HexInspector::print_hex_line(size_t offset, size_t length, size_t highlight_index) const {
    // Print offset
    std::cout << HexConstants::BLUE << std::setw(8) << std::setfill('0') 
              << std::hex << offset << HexConstants::RESET << "  ";

    // Print hex values
    std::string ascii_display;
    for (size_t i = 0; i < BYTES_PER_LINE; ++i) {
        if (i < length) {
            unsigned char byte = file_data[offset + i];
            std::string color = get_color_for_byte(byte);
            
            if (offset + i == highlight_index) {
                color = HexConstants::BG_WHITE + HexConstants::BLUE;
            }
            
            std::cout << color << std::setw(2) << std::setfill('0') 
                     << static_cast<int>(byte) << HexConstants::RESET << " ";
            
            ascii_display += std::isprint(byte) ? static_cast<char>(byte) : '.';
        } else {
            std::cout << "   ";
            ascii_display += " ";
        }
    }

    std::cout << " | " << HexConstants::GREEN << ascii_display << HexConstants::RESET << std::endl;
}

void HexInspector::print_footer() const {
    std::cout << "\n" << HexConstants::HELP_MESSAGE << std::endl;
}

void HexInspector::export_hex(const std::string& output_file_path) const {
    std::ofstream out(output_file_path);
    if (!out) {
        std::cerr << HexConstants::RED << "Error: Could not create output file" 
                 << HexConstants::RESET << std::endl;
        return;
    }

    for (size_t i = 0; i < file_data.size(); i++) {
        out << std::setw(2) << std::setfill('0') << std::hex 
            << static_cast<int>(file_data[i]);
        if ((i + 1) % HexConstants::BYTES_PER_EXPORT_LINE == 0) out << std::endl;
        else out << " ";
    }
}

void HexInspector::display_strings() const {
    size_t min_length = HexConstants::MIN_STRING_LENGTH;
    std::string current_string;
    size_t start_offset = 0;
    bool in_string = false;

    for (size_t i = 0; i < file_data.size(); i++) {
        if (std::isprint(file_data[i])) {
            if (!in_string) {
                start_offset = i;
                in_string = true;
            }
            current_string += static_cast<char>(file_data[i]);
        } else {
            if (in_string && current_string.length() >= min_length) {
                std::cout << HexConstants::BLUE << std::hex << start_offset << HexConstants::RESET 
                         << ": " << HexConstants::GREEN << current_string << HexConstants::RESET 
                         << std::endl;
            }
            current_string.clear();
            in_string = false;
        }
    }
}

void HexInspector::calculate_metadata() {
    metadata.fileSize = file_data.size();
    metadata.byteFrequency.clear();
    
    for (unsigned char byte : file_data) {
        metadata.byteFrequency[byte]++;
    }

    double entropy = 0.0;
    for (const auto& pair : metadata.byteFrequency) {
        double probability = static_cast<double>(pair.second) / file_data.size();
        if (probability > 0) {
            entropy -= probability * std::log2(probability);
        }
    }
    metadata.entropy = entropy;
}

void HexInspector::display_metadata() const {
    std::cout << HexConstants::BOLD << "\nFile Metadata:" << HexConstants::RESET << std::endl;
    std::cout << "File size: " << metadata.fileSize << " bytes" << std::endl;
    std::cout << "Entropy: " << std::fixed << std::setprecision(HexConstants::ENTROPY_PRECISION) 
              << metadata.entropy << " bits" << std::endl;
    
    size_t printable_count = std::count_if(file_data.begin(), file_data.end(), 
                                         [](unsigned char c) { return std::isprint(c); });
    size_t extended_count = std::count_if(file_data.begin(), file_data.end(),
                                        [](unsigned char c) { return c >= 0x7F; });
    
    std::cout << "Printable ASCII: " << printable_count << std::endl;
    std::cout << "Extended ASCII: " << extended_count << std::endl;
}

void HexInspector::display_hex_dump() {
    size_t total_pages = (file_data.size() + (BYTES_PER_LINE * LINES_PER_PAGE) - 1) / 
                        (BYTES_PER_LINE * LINES_PER_PAGE);
    
    while (true) {
        clear_screen();
        
        // Display header
        std::cout << HexConstants::CYAN << HexConstants::BOLD 
                 << "Hex Dump - Page " << (current_page + 1) << " of " << total_pages 
                 << HexConstants::RESET << std::endl;
        std::cout << HexConstants::HORIZONTAL_LINE << std::endl;

        // Display hex dump
        size_t start_offset = current_page * BYTES_PER_LINE * LINES_PER_PAGE;
        for (size_t i = 0; i < LINES_PER_PAGE; ++i) {
            size_t offset = start_offset + (i * BYTES_PER_LINE);
            if (offset >= file_data.size()) break;
            size_t remaining = std::min(BYTES_PER_LINE, file_data.size() - offset);
            print_hex_line(offset, remaining);
        }

        print_footer();

        // Handle input
        char cmd;
        std::cin >> cmd;
        cmd = std::toupper(cmd);

        switch (cmd) {
            case HexConstants::CMD_NEXT:
                if (current_page < total_pages - 1) current_page++;
                break;
            case HexConstants::CMD_PREV:
                if (current_page > 0) current_page--;
                break;
            case HexConstants::CMD_EXIT:
                return;
            case HexConstants::CMD_EXPORT: {
                std::string output_file;
                std::cout << "Enter output filename: ";
                std::cin >> output_file;
                export_hex(output_file);
                break;
            }
            case HexConstants::CMD_STRINGS:
                clear_screen();
                display_strings();
                std::cout << "\nPress Enter to continue...";
                std::cin.ignore(2);
                break;
            case HexConstants::CMD_METADATA:
                clear_screen();
                display_metadata();
                std::cout << "\nPress Enter to continue...";
                std::cin.ignore(2);
                break;
            default:
                std::cout << HexConstants::ERROR_INVALID_COMMAND << std::endl;
                break;
        }
    }
}