#ifndef COMMON_SESSION_LOCAL_SESSION_H
#define COMMON_SESSION_LOCAL_SESSION_H

#include "common/session/session.h"

class LocalSession : public Session {
public:
  LocalSession(std::unique_ptr<Channel> channel)
  : Session(std::move(channel)) {}

  void OnReadMessage(CallbackFunction callback);
  void SendMessage(protobuf::DataMessage& message);
};

#endif
