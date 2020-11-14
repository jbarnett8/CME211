cmake_minimum_required(VERSION 3.5)
project(hw5)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS "-Wall -Wconversion -Wextra -Wpedantic")

add_executable(hw5
        mazesolver.cpp)
