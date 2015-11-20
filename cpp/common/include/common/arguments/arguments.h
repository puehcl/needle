#ifndef COMMON_OPTIONS_H
#define COMMON_OPTIONS_H

#include <boost/program_options/options_description.hpp>
#include <boost/program_options/parsers.hpp>
#include <boost/program_options/value_semantic.hpp>
#include <boost/program_options/variables_map.hpp>

#include "common/config.h"

#define OPT_HELP "help"
#define OPT_VERSION "version"
#define OPT_MEDIATOR_HOSTNAME "mediator-hostname"
#define OPT_MEDIATOR_PORT "mediator-port"
#define OPT_LOCAL_HOSTNAME "local-hostname"
#define OPT_LOCAL_INTERFACE "local-interface"
#define OPT_LOCAL_PORT "local-port"

#define OPTDEF_HELP (OPT_HELP, "See this message")
#define OPTDEF_VERSION (OPT_VERSION, "Print the version")
#define OPTDEF_MEDIATOR_PORT (\
  OPT_MEDIATOR_PORT,\
  boost::program_options::value<int>()->default_value(DEFAULT_MEDIATOR_PORT),\
  "The port number of the mediator")
#define OPTDEF_MEDIATOR_HOSTNAME (\
  OPT_MEDIATOR_HOSTNAME,\
  boost::program_options::value<std::string>()\
      ->default_value(DEFAULT_MEDIATOR_HOSTNAME),\
  "The hostname of the mediator")
#define OPTDEF_LOCAL_PORT(DESCRIPTION) (\
  OPT_LOCAL_PORT,\
  boost::program_options::value<int>()->default_value(DEFAULT_LOCAL_PORT),\
  DESCRIPTION)
#define OPTDEF_LOCAL_HOSTNAME (\
  OPT_LOCAL_HOSTNAME,\
  boost::program_options::value<std::string>()\
    ->default_value(DEFAULT_LOCAL_HOSTNAME),\
  "The hostname where the server will connect to if there is an incoming \
  connection")
#define OPTDEF_LOCAL_INTERFACE (\
  OPT_LOCAL_INTERFACE,\
  boost::program_options::value<std::string>()\
    ->default_value(DEFAULT_LOCAL_INTERFACE),\
  "The local interface to bind the listening socket to")

namespace common {

  namespace arguments {
    typedef boost::program_options::variables_map options;
    typedef boost::program_options::options_description description;

    description& get_description();
    options& get_options();
    bool parse(std::string module_name, int argc, char* argv[]);
  }

}

#endif
