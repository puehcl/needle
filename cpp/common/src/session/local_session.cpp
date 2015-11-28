
#include "common/session/local_session.h"

namespace common {
  namespace session {
    
    void LocalSession::ReadNextMessage(protobuf::DataMessage& message) {
      logger_->Trace("Entering ReadNextMessage");
      try {
        message.set_data(channel_->Read());
      } catch(const common::channel::IOException& ex) {
        throw SessionException();
      }  
    }

    void LocalSession::SendMessage(protobuf::DataMessage& message) {
      logger_->Trace("Entering SendMessage");
      try {
        channel_->Write(message.data());
      } catch(const common::channel::IOException& ex) {
        throw SessionException();
      } 
    }    
    
    void LocalSession::Close() {
      logger_->Info("Closing session");
      channel_->Close();
    }
    
    void LocalSession::Print(std::ostream& os) const {
      os << "LocalSession[" << *channel_ << "]";
    }
    
  }
}

