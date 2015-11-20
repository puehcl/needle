cmake_minimum_required(VERSION 2.8.12)
project (host)

set (PROJECT_INCLUDE_DIR    ${CMAKE_CURRENT_SOURCE_DIR}/include)
set (PROJECT_SOURCE_DIR     ${CMAKE_CURRENT_SOURCE_DIR}/src)

include_directories (${PROJECT_INCLUDE_DIR})

file(GLOB host_SRC
    "${PROJECT_SOURCE_DIR}/*.cpp"
)

add_executable (host ${host_SRC})

target_link_libraries( host
    ${common_LIBRARY}
    ${Log4cxx_LIBRARIES}
    ${Boost_LIBRARIES}
)
