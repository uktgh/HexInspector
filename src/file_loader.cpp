#include "../inc/file_loader.h"
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <iostream>

uint8_t* load_exe(const std::string& path, size_t& size) {
    int fd = open(path.c_str(), O_RDONLY);
    if (fd == -1) {
        return nullptr;
    }

    struct stat file_stat;
    if (fstat(fd, &file_stat) == -1) {
        close(fd);
        return nullptr;
    }

    size = file_stat.st_size;
    uint8_t* data = (uint8_t*)mmap(NULL, size, PROT_READ, MAP_PRIVATE, fd, 0);
    close(fd);

    if (data == MAP_FAILED) {
        return nullptr;
    }

    return data;
}

void print_file_metadata(const std::string& path) {
    struct stat file_stat;
    if (stat(path.c_str(), &file_stat) == -1) {
        std::cerr << "Error retrieving file metadata." << std::endl;
        return;
    }

    std::cout << "File size: " << file_stat.st_size << " bytes" << std::endl;
    std::cout << "Last modified: " << ctime(&file_stat.st_mtime) << std::endl;
}
