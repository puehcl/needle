cmake_minimum_required(VERSION 2.8.12)
project (mediator)

set (PROJECT_INCLUDE_DIR    ${CMAKE_CURRENT_SOURCE_DIR}/include)
set (PROJECT_SOURCE_DIR     ${CMAKE_CURRENT_SOURCE_DIR}/src)

include_directories (${PROJECT_INCLUDE_DIR})

file(GLOB mediator_SRC
    "${PROJECT_SOURCE_DIR}/*.cpp"
)

add_executable (mediator ${mediator_SRC})

target_link_libraries( mediator
    ${common_LIBRARY}
    ${Boost_LIBRARIES}
)
