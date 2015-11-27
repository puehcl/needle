
#include <thread>

#include "common/relay/relay.h"
#include "messages.pb.h"

namespace common {
  
  namespace relay {
 
    std::uint64_t relay_uid_{0};
    
    const std::uint64_t GetNextUID() {
      relay_uid_ = relay_uid_ + 1;
      return relay_uid_;
    }
    
    void Relay::Start() { 
      logger_->Trace("Entering Start()");
      thread_ = std::thread([this]() {
        std::thread direction1([this]() {
          protobuf::DataMessage message;
          while(true) {
            session1_->ReadNextMessage(message);
            session2_->SendMessage(message);
          }
        });
        std::thread direction2([this]() {
          protobuf::DataMessage message;
          while(true) {
            session2_->ReadNextMessage(message);
            session1_->SendMessage(message);
          }
        });
        direction1.join();
        direction2.join();
        on_finish_callback_(*this);
      });
      thread_.detach();
    }
    
  }
 
}