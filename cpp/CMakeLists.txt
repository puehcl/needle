cmake_minimum_required (VERSION 2.8.12)
project (needle)

set (needle_VERSION_MAJOR 0)
set (needle_VERSION_MINOR 1)

include_directories (common/include)

add_subdirectory (common)
add_subdirectory (client)
