#include <iostream>

#include "client.h"
#include "common/arguments.h"
#include "common/config.h"

int main(int argc, char* argv[]) {
    common::arguments::get_description().add_options()
        ARGDEF_HELP
        ARGDEF_MEDIATOR_HOSTNAME
        ARGDEF_MEDIATOR_PORT
        ARGDEF_LOCAL_INTERFACE
        ARGDEF_LOCAL_PORT("The port on which the client should listen for incoming connections.")
    ;
    if(!common::arguments::parse(argc, argv)) {
        return 1;
    }
    common::arguments::options& opts = common::arguments::get_options();

    Client client(
        opts[ARG_MEDIATOR_HOSTNAME].as<std::string>(),
        opts[ARG_MEDIATOR_PORT].as<int>(),
        opts[ARG_LOCAL_INTERFACE].as<std::string>(),
        opts[ARG_LOCAL_PORT].as<int>());

    client.Run();

}
