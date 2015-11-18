cmake_minimum_required(VERSION 2.8.12)
project (client)

set (PROJECT_INCLUDE_DIR    ${CMAKE_CURRENT_SOURCE_DIR}/include)
set (PROJECT_SOURCE_DIR     ${CMAKE_CURRENT_SOURCE_DIR}/src)

include_directories (${PROJECT_INCLUDE_DIR})

file(GLOB client_SRC
    "${PROJECT_SOURCE_DIR}/*.cpp"
)

add_executable (client ${client_SRC})

target_link_libraries( client
    ${common_LIBRARY}
    ${Log4cxx_LIBRARIES}
    ${Boost_LIBRARIES}
)
