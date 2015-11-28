#ifndef COMMON_SESSION_LOCAL_SESSION_H
#define COMMON_SESSION_LOCAL_SESSION_H

#include "common/logging/logger.h"
#include "common/session/session.h"

namespace common {
  namespace session {
    
    class LocalSession : public Session {
    private:
      common::logging::Logger::ptr logger_;
    public:
      LocalSession(std::unique_ptr<common::channel::Channel> channel)
      : Session(std::move(channel)), 
        logger_(common::logging::GetLogger("LocalSession")) {}

      virtual void ReadNextMessage(protobuf::DataMessage& message) override;
      virtual void SendMessage(protobuf::DataMessage& message) override;
      virtual void Close() override;
      virtual void Print(std::ostream& os) const override;
    };
    
  }
}

#endif
