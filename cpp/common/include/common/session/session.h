#ifndef COMMON_SESSION_SESSION_H
#define COMMON_SESSION_SESSION_H

#include <functional>
#include <memory>
#include <utility>

#include "common/channel/channel.h"
#include "messages.pb.h"

//used to keep the state for the connection with the mediator/peer
class Session {
protected:
  typedef std::function<void(protobuf::DataMessage&)> CallbackFunction;

  std::unique_ptr<Channel> channel_;
public:
  Session(std::unique_ptr<Channel> channel) {channel_ = std::move(channel);}
  virtual void OnReadMessage(CallbackFunction callback) = 0;
  virtual void SendMessage(protobuf::DataMessage& message) = 0;
};

#endif
