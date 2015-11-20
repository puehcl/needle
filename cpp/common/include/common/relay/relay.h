#ifndef COMMON_RELAY_RELAY_H
#define COMMON_RELAY_RELAY_H

#include <cstdint>
#include <functional>
#include <memory>
#include <thread>

#include "common/session/session.h"

namespace common {
  namespace relay {
    
    class Relay {
    private:
      using CallbackFunction = std::function<void(const Relay&)>;
      
      const std::uint64_t uid_;
      const std::unique_ptr<Session> session1_;
      const std::unique_ptr<Session> session2_;
      const CallbackFunction on_finish_callback_;
      std::unique_ptr<std::thread> thread_;
    public:
      Relay(  std::uint64_t uid,
              std::unique_ptr<Session>& session1,
              std::unique_ptr<Session>& session2,
              CallbackFunction on_finish_callback)
        : uid_(uid),
          session1_(std::move(session1)),
          session2_(std::move(session2)),
          on_finish_callback_(on_finish_callback) {}
        
        std::uint64_t get_uid() { return uid_; }
    };
    
    std::uint64_t GetNextUID();
    
  }
}

#endif
