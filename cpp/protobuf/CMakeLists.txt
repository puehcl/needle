cmake_minimum_required(VERSION 2.8.12)
project (protobuf)

include (FindProtobuf)

set (PROTO_FILE messages.proto)
protobuf_generate_cpp (protobuf_SRCS protobuf_HDRS ${PROTO_FILE})

## get the actual directory of the header file
get_filename_component (INCLUDE_DIR ${protobuf_HDRS} DIRECTORY)

## copy the header file into a subfolder, so it can be used as "protobuf/headerfile.h"
## file (MAKE_DIRECTORY ${INCLUDE_DIR}/protobuf)
## file (COPY ${protobuf_HDRS} DESTINATION ${INCLUDE_DIR}/protobuf)

## define the protobuf library
set (protobuf_HDRS              ${INCLUDE_DIR}  PARENT_SCOPE)
set (Protobuf_PROJECT_LIBRARY   protobuf        PARENT_SCOPE)
add_library (protobuf ${protobuf_SRCS})
