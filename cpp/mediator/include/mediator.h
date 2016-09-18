//
// Created by clemens on 21/05/16.
//

#ifndef NEEDLE_MEDIATOR_H
#define NEEDLE_MEDIATOR_H

class Mediator {
public:
    Mediator(std::string local_interface, int local_port);
    void Run();
private:
    std::string local_interface_;
    int local_port_;
};

#endif //NEEDLE_MEDIATOR_H
