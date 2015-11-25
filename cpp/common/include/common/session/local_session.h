#ifndef COMMON_SESSION_LOCAL_SESSION_H
#define COMMON_SESSION_LOCAL_SESSION_H

#include "common/session/session.h"

namespace common {
  namespace session {
    
    class LocalSession : public Session {
    public:
      LocalSession(std::unique_ptr<common::channel::Channel> channel)
      : Session(std::move(channel)) {}

      virtual void ReadNextMessage(protobuf::DataMessage& message) override;
      virtual void SendMessage(protobuf::DataMessage& message) override;
    };
    
  }
}

#endif
