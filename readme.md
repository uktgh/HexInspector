# HexInspector

## project structure
```
HexInspector/
├── src/
│   ├── inc/
│   │   ├── constants.h 
│   │   └── hex_inspector.h
│   ├── main.cpp
│   └── hex_inspector.cpp
├── makefile
└── readme.md
```

## todo
- [x] hexadecimal display with offset and ascii
- [x] navigation between pages
- [x] pattern search (hex/ascii
- [x] syntax highlighting
- [x] string analysis
- [x] hex export
- [x] metadata display
- [x] entropy calculation
- [x] byte frequency analysis
- [ ] editing mode
- [ ] support for large files (lazy loading)
- [ ] bookmarks
- [ ] file comparison
- [ ] plugin system
- [ ] support for specific formats (pe, elf, etc.)
- [ ] unicode support
- [ ] export to different formats
- [ ] undo/redo for changes
- [ ] advanced search (regex, wildcards)

## usage
```
make
hex_inspector <filename>
```
### commands
- n -> next page
- p -> previous page
- s -> select page
- f -> find pattern
- h -> toggle highlight
- x -> export hex
- t -> show strings
- m -> show metadata
- b -> set bookmark
- g -> goto offset
- ? -> show this help
- e -> exit

