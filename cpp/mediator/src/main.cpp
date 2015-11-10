#include <iostream>

#include "common/arguments.h"
#include "common/config.h"

int main(int argc, char* argv[]) {
    common::arguments::get_description().add_options()
        ARGDEF_HELP
        ARGDEF_LOCAL_INTERFACE
        ARGDEF_LOCAL_PORT("The port on which the mediator should listen for incoming connections.")
    ;
    if(!common::arguments::parse(argc, argv)) {
        return 1;
    }
    common::arguments::options& opts = common::arguments::get_options();

}
