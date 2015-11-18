
#include <sstream>

#include <log4cxx/logger.h>
#include <log4cxx/basicconfigurator.h>
#include <log4cxx/consoleappender.h>
#include <log4cxx/patternlayout.h>

#include "common/logging/logger.h"

namespace common {
  namespace logging {
    
    template<typename Arg>
    std::ostream& Logger::BuildStream(std::ostream& stream, const Arg& arg) {
      return stream << arg;
    }
    
    template<typename Arg1, typename... Args>
    std::ostream& Logger::BuildStream(std::ostream& stream, const Arg1& arg1, 
        const Args&... args) {
      return BuildStream(stream << arg1, args...);
    }
    
    template<typename... Args>
    void Logger::Trace(const Args&... args) {
      if(internal_logger_->isTraceEnabled()) {
        std::ostringstream stream;
        LOG4CXX_TRACE(internal_logger_, BuildStream(stream, args...));
      }
    }
    
    Logger::ptr GetLogger(std::string name) {
      return Logger::ptr(new Logger(log4cxx::Logger::getLogger(name)));
    }
    
  }
}

