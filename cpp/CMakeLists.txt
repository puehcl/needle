cmake_minimum_required (VERSION 2.8.12)
project (needle)

set (CMAKE_VERBOSE_MAKEFILE true)

## Compiler flags
if(CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "-std=c++11")
endif()

find_package ( Boost COMPONENTS program_options REQUIRED )

set (needle_VERSION_MAJOR 0)
set (needle_VERSION_MINOR 1)

include_directories (common/include)

add_subdirectory (common)
add_subdirectory (client)
add_subdirectory (host)
add_subdirectory (mediator)
