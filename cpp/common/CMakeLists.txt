cmake_minimum_required(VERSION 2.8.12)
project (common)

set (PROJECT_INCLUDE_DIR ${PROJECT_SOURCE_DIR}/include)

configure_file (
    "${PROJECT_INCLUDE_DIR}/config.h.in"
    "${PROJECT_INCLUDE_DIR}/config.h"
)
