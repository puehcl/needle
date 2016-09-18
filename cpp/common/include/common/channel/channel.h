#ifndef COMMON_CHANNEL_CHANNEL_H
#define COMMON_CHANNEL_CHANNEL_H

#include <exception>
#include <vector>

#include "common/util/varargs.h"

namespace common {
  namespace channel {
    
    class IOException : public std::exception {
    private:
      std::string message_;
    public:
      template<typename FstPart, typename... MsgParts>
      IOException(const FstPart& fst, const MsgParts&... msg): 
        message_(common::util::varargs::ToString(fst, msg...)) {}
      
      virtual const char* what() const noexcept override { 
        return message_.c_str(); 
      }
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
