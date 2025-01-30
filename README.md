# 🔍 HexInspector

this is a powerful hex editor designed for inspecting and analyzing binary files. it provides a modern user interface with advanced features such as hex view, pattern analysis, and file comparison.

## features

- hex view with customizable bytes per row
- ascii and offset display options
- file comparison
- pattern analysis
- hash calculation (MD5, SHA-1, SHA-256)
- go to offset

## installation & usage

to install HexInspector, clone the repository and install the required dependencies:

```bash
git clone https://github.com/uktgh/HexInspector.git
cd HexInspector
pip install -r requirements.txt
```

to run HexInspector, execute the following command:

```bash
python main.py
```

## todo

- [x] implement hex view with customizable bytes per row
- [x] add ascii and offset display options
- [x] implement file comparison
- [x] implement pattern analysis
- [x] implement hash calculation (MD5, SHA-1, SHA-256)
- [x] add search functionality
- [x] add go to offset functionality
- [ ] improve pattern analysis with more advanced algorithms
- [ ] add support for editing binary files
- [ ] implement undo/redo functionality
- [ ] add more hash algorithms (e.g., SHA-512)
- [ ] improve file comparison with visual diff
- [ ] add support for large files with efficient memory usage
- [ ] implement a plugin system for extensibility
