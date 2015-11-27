#ifndef COMMON_RELAY_RELAY_H
#define COMMON_RELAY_RELAY_H

#include <cstdint>
#include <functional>
#include <memory>
#include <thread>

#include "common/logging/logger.h"
#include "common/session/session.h"

namespace common {
  namespace relay {
    
    class Relay {
    private:
      using CallbackFunction = std::function<void(Relay&)>;
      
      const common::logging::Logger::ptr logger_;
      const std::uint64_t uid_;
      const std::unique_ptr<common::session::Session> session1_;
      const std::unique_ptr<common::session::Session> session2_;
      const CallbackFunction on_finish_callback_;
      std::thread thread_;
    public:
      Relay(  std::uint64_t uid,
              std::unique_ptr<common::session::Session> session1,
              std::unique_ptr<common::session::Session> session2,
              CallbackFunction on_finish_callback)
        : logger_(
            common::logging::GetLogger("Relay[" + std::to_string(uid) + "]")),
          uid_(uid),
          session1_(std::move(session1)),
          session2_(std::move(session2)),
          on_finish_callback_(on_finish_callback) {}
        
        void Start();
        
        const std::uint64_t& get_uid() const { return uid_; }
    };
    
    const std::uint64_t GetNextUID();
    
  }
}

#endif
