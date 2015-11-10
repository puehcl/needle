#include <iostream>

#include "common/arguments.h"
#include "common/config.h"

int main(int argc, char* argv[]) {
    common::arguments::get_description().add_options()
        ARGDEF_HELP
        ARGDEF_MEDIATOR_HOSTNAME
        ARGDEF_MEDIATOR_PORT
        ARGDEF_LOCAL_HOSTNAME
        ARGDEF_LOCAL_PORT("The port to which the host should connect when a connection is established.")
    ;
    if(!common::arguments::parse(argc, argv)) {
        return 1;
    }
    common::arguments::options& opts = common::arguments::get_options();

}
