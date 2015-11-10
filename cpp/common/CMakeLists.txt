cmake_minimum_required(VERSION 2.8.12)
project (common)

set (PROJECT_INCLUDE_DIR    ${CMAKE_CURRENT_SOURCE_DIR}/include/common)
set (PROJECT_SOURCE_DIR     ${CMAKE_CURRENT_SOURCE_DIR}/src)

include_directories (${PROJECT_INCLUDE_DIR})

configure_file (
    "${PROJECT_INCLUDE_DIR}/config.h.in"
    "${PROJECT_INCLUDE_DIR}/config.h"
)

file(GLOB common_SRC
    "${PROJECT_SOURCE_DIR}/*.cpp"
)

## define the common library
set ( common_LIBRARY common PARENT_SCOPE )
add_library ( common ${common_SRC} )
