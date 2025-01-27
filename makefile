CXX = g++
CXXFLAGS = -std=c++17 -Wall -Wextra -lncurses -pthread
OBJ = src/menu.o src/utils.o
EXEC = hexinspector

$(EXEC): $(OBJ)
	$(CXX) $(OBJ) -o $(EXEC)

src/menu.o: src/menu.cpp inc/utils.h
	$(CXX) $(CXXFLAGS) -c src/menu.cpp -o src/menu.o

src/utils.o: src/utils.cpp inc/utils.h
	$(CXX) $(CXXFLAGS) -c src/utils.cpp -o src/utils.o

clean:
	rm -f $(OBJ) $(EXEC)
