#pragma once
#include <string>

namespace HexConstants {
    const std::string RESET     = "\033[0m";
    const std::string RED       = "\033[31m";
    const std::string GREEN     = "\033[32m";
    const std::string YELLOW    = "\033[33m";
    const std::string BLUE      = "\033[34m";
    const std::string MAGENTA   = "\033[35m";
    const std::string CYAN      = "\033[36m";
    const std::string WHITE     = "\033[37m";
    const std::string BOLD      = "\033[1m";
    
    const std::string BG_BLACK  = "\033[40m";
    const std::string BG_RED    = "\033[41m";
    const std::string BG_GREEN  = "\033[42m";
    const std::string BG_YELLOW = "\033[43m";
    const std::string BG_BLUE   = "\033[44m";
    const std::string BG_MAGENTA= "\033[45m";
    const std::string BG_CYAN   = "\033[46m";
    const std::string BG_WHITE  = "\033[47m";

    const std::string UNDERLINE = "\033[4m";
    const std::string BLINK     = "\033[5m";
    const std::string REVERSE   = "\033[7m";
    
    const size_t DEFAULT_BYTES_PER_LINE = 16;
    const size_t DEFAULT_LINES_PER_PAGE = 20;
    const size_t MIN_STRING_LENGTH = 4;
    const size_t MAX_FILE_SIZE_WARNING = 100 * 1024 * 1024; // 100MB

    const std::string HORIZONTAL_LINE = std::string(72, '-');
    const std::string OFFSET_HEADER = "offset";
    const std::string HEX_HEADER = "hexadecimal data";
    const std::string ASCII_HEADER = "ascii";
    
    const char CMD_NEXT = 'N';
    const char CMD_PREV = 'P';
    const char CMD_SELECT = 'S';
    const char CMD_FIND = 'F';
    const char CMD_HIGHLIGHT = 'H';
    const char CMD_EXPORT = 'X';
    const char CMD_STRINGS = 'T';
    const char CMD_METADATA = 'M';
    const char CMD_EXIT = 'E';
    const char CMD_HELP = '?';
    const char CMD_BOOKMARK = 'B';
    const char CMD_GOTO = 'G';
    
    const std::string ERROR_FILE_NOT_FOUND = "Error: File not found";
    const std::string ERROR_FILE_TOO_LARGE = "Warning: File is larger than " + 
                                            std::to_string(MAX_FILE_SIZE_WARNING/1024/1024) + 
                                            "MB. Loading might be slow.";
    const std::string ERROR_INVALID_COMMAND = "Error: Invalid command";
    const std::string ERROR_INVALID_PAGE = "Error: Invalid page number";
    
    const std::string USAGE_MESSAGE = "Usage: hex_inspector <filename>";
    const std::string HELP_MESSAGE = 
        "Commands:\n"
        "  N - Next page\n"
        "  P - Previous page\n"
        "  S - Select page\n"
        "  F - Find pattern\n"
        "  H - Toggle highlight\n"
        "  X - Export hex\n"
        "  T - Show strings\n"
        "  M - Show metadata\n"
        "  B - Set bookmark\n"
        "  G - Goto offset\n"
        "  ? - Show this help\n"
        "  E - Exit";

    const unsigned char PDF_HEADER[] = {0x25, 0x50, 0x44, 0x46}; // pdf
    const unsigned char PNG_HEADER[] = {0x89, 0x50, 0x4E, 0x47}; // png
    const unsigned char JPEG_HEADER[] = {0xFF, 0xD8, 0xFF};      // jpeg
    const unsigned char ELF_HEADER[] = {0x7F, 0x45, 0x4C, 0x46}; // elf
    
    const size_t ENTROPY_PRECISION = 2;
    const size_t FREQUENCY_CHART_WIDTH = 50;
    
    const size_t BYTES_PER_EXPORT_LINE = 16;
    const std::string DEFAULT_EXPORT_EXTENSION = ".hex";
}