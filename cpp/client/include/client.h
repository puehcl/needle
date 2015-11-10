
#ifndef CLIENT_CLIENT_H
#define CLIENT_CLIENT_H

#include <string>

class Client {
private:
    ::std::string mediator_host_name_;
    ::std::string local_interface_;
    int mediator_port_;
    int local_port_;
public:
    Client( ::std::string mediator_host_name, int mediator_port,
            ::std::string local_interface, int local_port) :
        mediator_host_name_(mediator_host_name),
        mediator_port_(mediator_port),
        local_interface_(local_interface),
        local_port_(local_port) {};

    void Run();
};

#endif
