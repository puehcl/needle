
#include "common/session/local_session.h"

namespace common {
  namespace session {
    
    void LocalSession::ReadNextMessage(protobuf::DataMessage& message) {
      logger_->Trace("Entering ReadNextMessage");
      message.set_data(channel_->Read());
    }

    void LocalSession::SendMessage(protobuf::DataMessage& message) {
      logger_->Trace("Entering SendMessage");
      channel_->Write(message.data());
    }    
    
  }
}

