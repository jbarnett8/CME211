CXX=g++
CXXFLAGS=-std=c++11 -Wall -Wpedantic -Wconversion -Wextra -O3 -I/usr/local/include/boost -L/usr/local/lib -ljpeg
DEPS = hw6.hpp image.hpp main.cpp
OBJ = hw6.o image.o main.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CXXFLAGS)

main: $(OBJ)
	$(CXX) -o $@ $^ $(CXXFLAGS)

clean:
	rm -f *.o main
