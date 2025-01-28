#include <iostream>
#include "hex_inspector.h"
#include "constants.h"

int main(int argc, char* argv[]) {
    if (argc != 2) {
        std::cout << HexConstants::BOLD + HexConstants::RED 
                  << HexConstants::USAGE_MESSAGE 
                  << HexConstants::RESET << std::endl;
        return 1;
    }

    try {
        HexInspector inspector(argv[1]);
        inspector.display_hex_dump();
    }
    catch (const std::exception& e) {
        std::cout << HexConstants::RED << "Error: " << e.what() 
                  << HexConstants::RESET << std::endl;
        return 1;
    }

    return 0;
}