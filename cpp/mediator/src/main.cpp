#include <iostream>

#include "common/arguments/arguments.h"
#include "common/config.h"

#define MODULE_NAME "needle-mediator"

int main(int argc, char* argv[]) {
    common::arguments::get_description().add_options()
        OPTDEF_HELP
        OPTDEF_VERSION
        OPTDEF_LOCAL_INTERFACE
        OPTDEF_LOCAL_PORT("The port on which the mediator should listen for incoming connections.")
    ;
    if(!common::arguments::parse(MODULE_NAME, argc, argv)) {
        return 1;
    }
    common::arguments::options& opts = common::arguments::get_options();

}
