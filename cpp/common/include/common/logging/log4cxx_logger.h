#ifndef COMMON_LOGGING_LOG4CXX_LOGGER_H
#define COMMON_LOGGING_LOG4CXX_LOGGER_H

#include "common/logging/logging.h"

namespace common {

  namespace logging {

    class Log4cxxLogger : public Logger {
    public:
      virtual void Debug(std::ostream message);
      virtual void Info(std::ostream message);
      virtual void Warn(std::ostream message);
      virtual void Error(std::ostream message);
    };

  }

}

#endif
