# file_structure.md

# HexInspector Project File Structure

This document provides an overview of the file structure for the HexInspector project. The structure is organized to facilitate easy navigation and understanding of the project's components.

## Directory Structure

```
HexInspector/
├── compression.py
├── features.md
├── gui.py
├── hexviewer.py
├── main.py
├── requirements.txt
├── utils.py
└── file_structure.md
```

### Description of Key Files

- **compression.py**: Contains the `CompressionHandler` class responsible for handling file extraction from ZIP and GZ archives.
- **features.md**: Documents the roadmap for future development, detailing features, implementation steps, and expected outcomes.
- **gui.py**: Implements the graphical user interface using Tkinter, providing functionalities for file operations, viewing, and analysis.
- **hexviewer.py**: Provides the `HexViewer` class for reading and displaying hex data, calculating checksums, and searching patterns.
- **main.py**: The entry point of the application, initializing the GUI and starting the main loop.
- **requirements.txt**: Lists the dependencies required for the project, ensuring all necessary packages are installed.
- **utils.py**: Contains utility functions, such as retrieving file metadata.
- **file_structure.md**: This document, providing an overview of the project's file structure.

This structure is designed to separate concerns and organize the codebase logically, making it easier for developers to navigate and maintain the project.
