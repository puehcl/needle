#ifndef COMMON_OPTIONS_H
#define COMMON_OPTIONS_H

#include <boost/program_options/options_description.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/value_semantic.hpp>
#include <boost/program_options/variables_map.hpp>

#define ARG_HELP "help"
#define ARG_MEDIATOR_HOSTNAME "mediator-hostname"
#define ARG_MEDIATOR_PORT "mediator-port"
#define ARG_LOCAL_HOSTNAME "local-hostname"
#define ARG_LOCAL_INTERFACE "local-interface"
#define ARG_LOCAL_PORT "local-port"

#define ARGDEF_HELP (ARG_HELP, "See this message")
#define ARGDEF_MEDIATOR_PORT (\
    ARG_MEDIATOR_PORT,\
    boost::program_options::value<int>()->default_value(DEFAULT_MEDIATOR_PORT),\
    "The port number of the mediator")
#define ARGDEF_MEDIATOR_HOSTNAME (\
    ARG_MEDIATOR_HOSTNAME,\
    boost::program_options::value<std::string>()\
        ->default_value(DEFAULT_MEDIATOR_HOSTNAME),\
    "The hostname of the mediator")
#define ARGDEF_LOCAL_PORT(DESCRIPTION) (\
    ARG_LOCAL_PORT,\
    boost::program_options::value<int>()->default_value(DEFAULT_LOCAL_PORT),\
    DESCRIPTION)
#define ARGDEF_LOCAL_HOSTNAME (\
    ARG_LOCAL_HOSTNAME,\
    boost::program_options::value<std::string>()\
        ->default_value(DEFAULT_LOCAL_HOSTNAME),\
    "The hostname where the server will connect to if there is an incoming \
    connection")
#define ARGDEF_LOCAL_INTERFACE (\
    ARG_LOCAL_INTERFACE,\
    boost::program_options::value<std::string>()\
        ->default_value(DEFAULT_LOCAL_INTERFACE),\
    "The local interface to bind the listening socket to")

namespace common {

    namespace arguments {
        typedef boost::program_options::variables_map options;
        typedef boost::program_options::options_description description;

        description& get_description();
        options& get_options();
        bool parse(int argc, char* argv[]);
    }
}

#endif
