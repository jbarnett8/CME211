CXX=g++
CXXFLAGS=-std=c++11 -Wall -Wpedantic -Wconversion -Wextra -O3
DEPS = CGSolver.hpp COO2CSR.hpp matvecops.hpp heat.hpp sparse.hpp main.cpp
OBJ = CGSolver.o COO2CSR.o matvecops.o heat.o sparse.o main.o

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CXXFLAGS)

main: $(OBJ)
	$(CXX) -o $@ $^ $(CXXFLAGS)

clean:
	rm -f *.o ~* main
