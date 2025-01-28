#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>
#include <cstdlib>
#include <sstream>
#include <algorithm>

#define reset   "\033[0m"
#define red     "\033[31m"
#define yellow  "\033[33m"
#define cyan    "\033[36m"

namespace HexInspector {
    class HexInspector {
private:
    std::vector<uint8_t> data;
    size_t current_offset = 0;

    static const size_t bytes_per_row = 16;
    static const size_t rows_per_page = 20;

    std::string current_filename;

    void clear_screen() {
        #ifdef _WIN32
            system("cls");
        #else
            system("clear");
        #endif
    }

    void load_file(const std::string& filename) {
        std::ifstream file(filename, std::ios::binary);

        if (!file) {
            throw std::runtime_error("[-] couldn't open : " + filename);
        }

        data.clear();

        char byte;

        while (file.get(byte)) {
            data.push_back(static_cast<uint8_t>(byte));
        }

        current_filename = filename;
    }

    void show_hex_dump() {
        clear_screen();

        std::cout << cyan << "file : " << current_filename << reset << "\n";
        std::cout << cyan << "dimension : " << data.size() << " bytes" << reset << "\n\n";

        std::cout << cyan << "OFFSET      00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F    ASCII" << reset << "\n\n";

        for (size_t i = 0; i < rows_per_page && (current_offset + i * bytes_per_row) < data.size(); ++i) {
            size_t offset = current_offset + i * bytes_per_row;

            std::cout << cyan << std::setfill('0') << std::setw(8) << std::hex << offset << reset << "   ";

            for (size_t j = 0; j < bytes_per_row; ++j) {
                if (offset + j < data.size()) {
                    std::cout << std::setfill('0') << std::setw(2) << std::hex << static_cast<int>(data[offset + j]) << reset << " ";
                } else {
                    std::cout << "   ";
                }
            }

            std::cout << "   ";
            for (size_t j = 0; j < bytes_per_row; ++j) {
                if (offset + j < data.size()) {
                    char c = data[offset + j];
                    std::cout << cyan << (c >= 32 && c <= 126 ? c : '.');
                }
            }

            std::cout << "\n";
        }
    }

    void show_menu() {                                          
        std::cout << "\n\n[1] open file\n";
        std::cout << "[2] next\n";
        std::cout << "[3] back\n";
        std::cout << "[4] go to offset\n";
        std::cout << "[5] search byte\n";
        std::cout << "[6] export dump in file\n";
        std::cout << "[7] show ascii strings\n";
        std::cout << "[8] exit\n";
        std::cout << "\n[?] select : ";
    }

    void search_byte() {
        std::cout << "[?] insert byte sequence : ";
        std::string input;
        std::cin.ignore();
        std::getline(std::cin, input);

        std::vector<uint8_t> search_pattern;
        std::stringstream ss(input);
        std::string byteStr;

        while (ss >> byteStr) {
            search_pattern.push_back(static_cast<uint8_t>(std::stoi(byteStr, nullptr, 16)));
        }

        bool found = false;
        for (size_t i = 0; i < data.size() - search_pattern.size() + 1; ++i) {
            bool match = true;
            for (size_t j = 0; j < search_pattern.size(); ++j) {
                if (data[i + j] != search_pattern[j]) {
                    match = false;
                    break;
                }
            }
            if (match) {
                current_offset = i;
                found = true;
                break;
            }
        }

        if (!found) {
            std::cout << red << "[-] sequence not found" << reset << "\n";
            std::cin.get();
        }
    }

    void export_dump_to_file() {
        std::cout << "[?] insert a name for the file : ";
        std::string filename;
        std::cin >> filename;

        std::ofstream output_file(filename, std::ios::binary);
        if (!output_file) {
            std::cout << red << "[-] couldn't open the file !" << reset << "\n";
            return;
        }

        for (size_t i = 0; i < data.size(); ++i) {
            output_file.put(data[i]);
        }

        std::cout << cyan << "[+] dump exported succesfully : " << filename << reset << "\n";
        std::cin.get();
    }

    void show_ascii_strings() {
        std::cout << "\n" << yellow << "[?] ascii string found in :" << reset << "\n";

        std::string current_string;
        for (size_t i = 0; i < data.size(); ++i) {
            char c = data[i];
            if (c >= 32 && c <= 126) {
                current_string += c;
            } else {
                if (!current_string.empty()) {
                    std::cout << current_string << "\n";
                    current_string.clear();
                }
            }
        }

        if (!current_string.empty()) {
            std::cout << current_string << "\n";
        }
    }

public:
    void run() {
        std::cout << cyan << " _              _                     _           " << reset << "\n";
        std::cout << cyan << "| |_ ___ _ _   |_|___ ___ ___ ___ ___| |_ ___ ___ " << reset << "\n";
        std::cout << cyan << "|   | -_|_'_|  | |   |_ -| . | -_|  _|  _| . |  _|" << reset << "\n";
        std::cout << cyan << "|_|_|___|_,_|  |_|_|_|___|  _|___|___|_| |___|_|  " << reset << "\n";
        std::cout << cyan << "                         |_|                      " << reset << "\n\n";

        while (true) {
            if (!data.empty()) {
                show_hex_dump();
            }

            show_menu();

            int choice;
            std::cin >> choice;

            switch (choice) {
                case 1: {
                    std::cout << "[?] file name : ";
                    std::string filename;
                    std::cin >> filename;

                    try {
                        load_file(filename);
                    } catch (const std::exception& e) {
                        std::cout << red << e.what() << reset << std::endl;
                        std::cin.get();
                    }

                    break;
                }

                case 2:
                    if (current_offset + rows_per_page * bytes_per_row < data.size()) {
                        current_offset += rows_per_page * bytes_per_row;
                    }
                    break;

                case 3:
                    if (current_offset >= rows_per_page * bytes_per_row) {
                        current_offset -= rows_per_page * bytes_per_row;
                    }
                    break;

                case 4: {
                    std::cout << "[?] insert offset : ";
                    std::string offsetStr;
                    std::cin >> offsetStr;
                    size_t new_offset = std::stoull(offsetStr, nullptr, 16);

                    if (new_offset < data.size()) {
                        current_offset = new_offset;
                    }

                    break;
                }

                case 5:
                    search_byte();
                    break;

                case 6:
                    export_dump_to_file();
                    break;

                case 7:
                    show_ascii_strings();
                    std::cin.get();
                    break;

                case 8:
                    return;

                default:
                    continue;
            }
        }
    }
};
}

int main() {
    HexInspector::HexInspector inspector;
    inspector.run();
    return 0;
}
