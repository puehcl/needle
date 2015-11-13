#include <iostream>

#include "common/arguments/arguments.h"
#include "common/config.h"

#define MODULE_NAME "needle-host"

int main(int argc, char* argv[]) {
    common::arguments::get_description().add_options()
        OPTDEF_HELP
        OPTDEF_VERSION
        OPTDEF_MEDIATOR_HOSTNAME
        OPTDEF_MEDIATOR_PORT
        OPTDEF_LOCAL_HOSTNAME
        OPTDEF_LOCAL_PORT("The port to which the host should connect when a connection is established.")
    ;
    if(!common::arguments::parse(MODULE_NAME, argc, argv)) {
        return 1;
    }
    common::arguments::options& opts = common::arguments::get_options();

}
