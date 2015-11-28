#ifndef COMMON_CHANNEL_CHANNEL_H
#define COMMON_CHANNEL_CHANNEL_H

#include <exception>
#include <vector>

namespace common {
  namespace channel {
    
    class IOException : public std::exception {
      
    };
    
    class Channel {
    public:
      virtual ~Channel() {};
      virtual void Write(std::string buffer) = 0;
      virtual std::string Read() = 0;
      virtual void Close() = 0;
      virtual void Print(std::ostream& os) const = 0;
      
      friend std::ostream& operator<< ( std::ostream& os, 
                                        const Channel& channel) {
        channel.Print(os);
        return os;
      }
    };   
    
  }
}

#endif
