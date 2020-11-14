cmake_minimum_required(VERSION 3.5)
project(cme211exam2)

set(CMAKE_CXX_STANDARD 11)

#set(CMAKE_CXX_FLAGS "-g -Wall -Wpedantic")
set(CMAKE_BUILD_TYPE Debug)

add_executable(main main.cpp Stock.hpp Stock.cpp)