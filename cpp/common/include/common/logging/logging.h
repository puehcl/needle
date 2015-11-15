#ifndef COMMON_LOGGING_LOGGING_H
#define COMMON_LOGGING_LOGGING_H

#include <iostream>
#include <memory>

namespace common {

  namespace logging {

    class Logger {
    public:
      using ptr = std::unique_ptr<Logger>;

      virtual void Debug(std::ostream message) = 0;
      virtual void Info(std::ostream message) = 0;
      virtual void Warn(std::ostream message) = 0;
      virtual void Error(std::ostream message) = 0;
    };

    Logger::ptr GetLogger(std::string name);

  }

}

#endif
