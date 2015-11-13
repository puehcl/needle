cmake_minimum_required (VERSION 2.8.12)
project (needle)

set (needle_VERSION_MAJOR 0)
set (needle_VERSION_MINOR 1)

set (CMAKE_VERBOSE_MAKEFILE true)

set (CUSTOM_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/CMakeModules")
set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CUSTOM_MODULE_PATH}")

message (${CMAKE_MODULE_PATH})

## Compiler flags
if(CMAKE_COMPILER_IS_GNUCXX)
    set(CMAKE_CXX_FLAGS "-std=c++11")
endif()

find_package ( Protobuf REQUIRED )
find_package ( Boost REQUIRED program_options system )
find_package ( Log4cxx REQUIRED )


add_subdirectory (protobuf)
include_directories (${protobuf_HDRS})

add_subdirectory (common)
include_directories (${common_HDRS})

add_subdirectory (client)
add_subdirectory (host)
add_subdirectory (mediator)
