#ifndef CLIENT_MEDIATOR_SESSION_H
#define CLIENT_MEDIATOR_SESSION_H

#include "common/session/session.h"

class MediatorSession : public common::session::Session {
public:
  //MediatorSession() : Session(std::unique_ptr<Channel>(new UDPChannel())) {}
  MediatorSession() : Session(std::unique_ptr<common::channel::Channel>()) {}
  virtual void ReadNextMessage(protobuf::DataMessage& message) override;
  virtual void SendMessage(protobuf::DataMessage& message) override;
};

#endif
