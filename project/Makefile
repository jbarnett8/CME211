CXX=g++
CXXFLAGS=-std=c++11 -Wall -Wpedantic -Wconversion -Wextra
DEPS = CGSolver.hpp COO2CSR.hpp matvecops.hpp main.cpp
OBJ = CGSolver.o COO2CSR.o matvecops.o main.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CXXFLAGS)

main: $(OBJ)
	$(CXX) -o $@ $^ $(CXXFLAGS)

clean:
	rm -f *.o main
