cmake_minimum_required(VERSION 2.8.12)
project (common)

set (PROJECT_INCLUDE_DIR    ${CMAKE_CURRENT_SOURCE_DIR}/include)
set (PROJECT_SOURCE_DIR     ${CMAKE_CURRENT_SOURCE_DIR}/src)

include_directories (${PROJECT_INCLUDE_DIR})

configure_file (
    "${PROJECT_INCLUDE_DIR}/common/config.h.in"
    "${PROJECT_INCLUDE_DIR}/common/config.h"
)

file (GLOB_RECURSE common_SRC "*.cpp")

## define the common library
set ( common_HDRS       ${PROJECT_INCLUDE_DIR}  PARENT_SCOPE)
set ( common_LIBRARY    common                  PARENT_SCOPE )
add_library ( common ${common_SRC} )
