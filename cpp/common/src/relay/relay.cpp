
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
    
    Relay::Relay( const std::uint64_t uid,
                  std::unique_ptr<common::session::Session> session1,
                  std::unique_ptr<common::session::Session> session2,
                  CallbackFunction on_finish_callback)
        : uid_(uid),
          session1_(std::move(session1)),
          session2_(std::move(session2)),
          on_finish_callback_(on_finish_callback) {
      
      logger_ =
        common::logging::GetLogger("Relay[" + std::to_string(uid) + "]");
          
    }
    
    void Relay::Start() { 
      logger_->Trace("Entering Start()");
      thread_ = std::thread([this]() {
        std::thread direction1([this]() {
          RelayData(*session1_, *session2_);
        });
        std::thread direction2([this]() {
          RelayData(*session2_, *session1_);
        });
        direction1.join();
        direction2.join();
        logger_->Debug("Both threads finished, calling callback");
        on_finish_callback_(*this);
      });
      thread_.detach();
    }
    
    void Relay::RelayData(common::session::Session& session1, 
                          common::session::Session& session2) {
      protobuf::DataMessage message;
      while(true) {
        try {
          session1.ReadNextMessage(message);
        } catch(const common::session::SessionException& ex) {
          logger_->Error( "SessionException while reading from ", session1, 
                          ": ", ex.what());
          break;
        }
        try {
          session2.SendMessage(message);
        } catch(const common::session::SessionException& ex) {
          logger_->Error( "SessionException while sending to ", session2, 
                          ": ", ex.what());
          break;
        }
      }
      session1.Close();
      session2.Close();
    }
    
  }
 
}