#ifndef COMMON_LOGGING_LOGGING_H
#define COMMON_LOGGING_LOGGING_H

#include <iostream>
#include <memory>

#include <log4cxx/logger.h>

namespace common {

  namespace logging {

    class Logger {
    private:
      log4cxx::LoggerPtr internal_logger_;
      
      template<typename Arg>
      std::ostream& BuildStream(std::ostream& stream, const Arg& arg);
      template<typename Arg1, typename... Args>
      std::ostream& BuildStream(std::ostream& stream, const Arg1& arg1, 
        const Args&... args);
    public:
      using ptr = std::unique_ptr<Logger>;

      Logger(log4cxx::LoggerPtr internal_logger)
        : internal_logger_(internal_logger) {}
      
      template<typename... Args>
      void Trace(const Args&... args);
     
    };

    Logger::ptr GetLogger(std::string name);

  }

}

#endif
