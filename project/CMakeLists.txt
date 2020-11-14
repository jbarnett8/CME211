cmake_minimum_required(VERSION 3.5)
project(cme211project)

set(CMAKE_CXX_STANDARD 11)

#set(CMAKE_CXX_FLAGS "-g -Wall -Wpedantic")
set(CMAKE_BUILD_TYPE Debug)

add_executable(main main.cpp CGSolver.hpp CGSolver.cpp matvecops.hpp
        matvecops.cpp COO2CSR.hpp COO2CSR.cpp sparse.hpp sparse.cpp
        heat.hpp heat.cpp)