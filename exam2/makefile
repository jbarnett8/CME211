CXX=g++
CXXFLAGS=-std=c++11 -Wall -Wpedantic -Wconversion -Wextra -O3
DEPS = Stock.hpp main.cpp
OBJ = Stock.o main.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CXXFLAGS)

main: $(OBJ)
	$(CXX) -o $@ $^ $(CXXFLAGS)

clean:
	rm -f *.o ~* main
