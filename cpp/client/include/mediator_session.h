#ifndef CLIENT_MEDIATOR_SESSION_H
#define CLIENT_MEDIATOR_SESSION_H

#include "common/session/session.h"

class MediatorSession : public Session {
public:
  //MediatorSession() : Session(std::unique_ptr<Channel>(new UDPChannel())) {}
  MediatorSession() : Session(std::unique_ptr<Channel>()) {}
  void OnReadMessage(CallbackFunction callback);
  void SendMessage(protobuf::DataMessage& message);
};

#endif
