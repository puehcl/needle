#ifndef COMMON_SESSION_SESSION_H
#define COMMON_SESSION_SESSION_H

#include <exception>
#include <functional>
#include <memory>
#include <utility>

#include "common/channel/channel.h"
#include "messages.pb.h"


namespace common {
  namespace session {
 
    class SessionException : public std::exception {
      
    };
    
    //used to keep the state for the connection with the mediator/peer
    class Session {
    protected:
      std::unique_ptr<common::channel::Channel> channel_;
    public:
      Session(std::unique_ptr<common::channel::Channel> channel) 
      : channel_(std::move(channel)) {}
      
      virtual void ReadNextMessage(protobuf::DataMessage& message) = 0;
      virtual void SendMessage(protobuf::DataMessage& message) = 0;
      virtual void Close() = 0;
      virtual void Print(std::ostream& os) const = 0;
      
      friend std::ostream& operator<< ( std::ostream& os, 
                                        const Session& session) {
        session.Print(os);
        return os;
      }
    };
    
  }
}

#endif
