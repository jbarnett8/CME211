cmake_minimum_required(VERSION 3.10)
project(hw6)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)

find_package(Boost)
find_package(JPEG)

include_directories(${Boost_INCLUDE_DIRS})
link_libraries(${JPEG_LIBRARIES})

set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wconversion -Wextra -pedantic -O3")

include_directories(.)

add_executable(main
        hw6.cpp
        hw6.hpp
        main.cpp
        image.hpp
        image.cpp)
