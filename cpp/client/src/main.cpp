#include <iostream>

#include "common/arguments/arguments.h"

#include "client.h"
#include "messages.pb.h"

#define MODULE_NAME "needle-client"

int main(int argc, char* argv[]) {
  common::arguments::get_description().add_options()
    OPTDEF_HELP
    OPTDEF_VERSION
    OPTDEF_MEDIATOR_HOSTNAME
    OPTDEF_MEDIATOR_PORT
    OPTDEF_LOCAL_INTERFACE
    OPTDEF_LOCAL_PORT("The port on which the client should listen for incoming connections.")
  ;
  if(!common::arguments::parse(MODULE_NAME, argc, argv)) {
    return 1;
  }
  common::arguments::options& opts = common::arguments::get_options();

  Client client(
    opts[OPT_MEDIATOR_HOSTNAME].as<std::string>(),
    opts[OPT_MEDIATOR_PORT].as<int>(),
    opts[OPT_LOCAL_INTERFACE].as<std::string>(),
    opts[OPT_LOCAL_PORT].as<int>());

  client.Run();

}
