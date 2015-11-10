#include <iostream>

#include "arguments.h"

namespace common {

    namespace arguments {

        boost::program_options::options_description desc("Available options");
        boost::program_options::variables_map variables_map;

        description& get_description() {
            return desc;
        }

        options& get_options() {
            return variables_map;
        }

        bool parse(int argc, char* argv[]) {
            try {
                boost::program_options::store(
                    boost::program_options::parse_command_line(argc, argv, desc),
                    variables_map);
                boost::program_options::notify(variables_map);
            } catch(const std::exception& e) {
                std::cerr << e.what() << std::endl;
                std::cerr << desc << std::endl;
                return false;
            }
            if(variables_map.count(ARG_HELP)) {
                std::cerr << desc << std::endl;
                return false;
            }
            return true;
        }
    }

}
