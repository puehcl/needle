
#include "common/relay/relay.h"

namespace common {
  
  namespace relay {
 
    std::uint64_t relay_uid_{0};
    
    const std::uint64_t GetNextUID() {
      relay_uid_ = relay_uid_ + 1;
      return relay_uid_;
    }
    
    void Relay::Start() { 
      
    }
    
  }
 
}