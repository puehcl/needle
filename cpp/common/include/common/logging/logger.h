#ifndef COMMON_LOGGING_LOGGING_H
#define COMMON_LOGGING_LOGGING_H

#include <iostream>
#include <memory>
#include <mutex>

#include <log4cxx/basicconfigurator.h>
#include <log4cxx/consoleappender.h>
#include <log4cxx/patternlayout.h>
#include <log4cxx/logger.h>

#include "common/config.h"
#include "common/util/varargs.h"

#define LOGGER_LOG_PATTERN "\%d{yyyy-MM-dd HH:mm:ss} \%-5p \%c: \%m\%n"

namespace common {

  namespace logging {
    
    class Logger {
    private:
      log4cxx::LoggerPtr internal_logger_;
      
    public:
      using ptr = std::unique_ptr<Logger>;

      Logger(log4cxx::LoggerPtr internal_logger)
        : internal_logger_(internal_logger) {}
      
      template<typename... Args>
      void Trace(const Args&... args) {
        if(internal_logger_->isTraceEnabled()) {
          std::string str = common::util::varargs::ToString(args...);
          LOG4CXX_TRACE(internal_logger_, str);
        }
      }
      
      template<typename... Args>
      void Debug(const Args&... args) {
        if(internal_logger_->isDebugEnabled()) {
          std::string str = common::util::varargs::ToString(args...);
          LOG4CXX_DEBUG(internal_logger_, str);
        }
      }
      
      template<typename... Args>
      void Info(const Args&... args) {
        if(internal_logger_->isInfoEnabled()) {
          std::string str = common::util::varargs::ToString(args...);
          LOG4CXX_INFO(internal_logger_, str);
        }
      }
      
      template<typename... Args>
      void Warn(const Args&... args) {
        if(internal_logger_->isWarnEnabled()) {
          std::string str = common::util::varargs::ToString(args...);
          LOG4CXX_WARN(internal_logger_, str);
        }
      }
      
      template<typename... Args>
      void Error(const Args&... args) {
        if(internal_logger_->isErrorEnabled()) {
          std::string str = common::util::varargs::ToString(args...);
          LOG4CXX_ERROR(internal_logger_, str);
        }
      }
      
      template<typename... Args>
      void Fatal(const Args&... args) {
        if(internal_logger_->isFatalEnabled()) {
          std::string str = common::util::varargs::ToString(args...);
          LOG4CXX_FATAL(internal_logger_, str);
        }
      }
     
    };
    
    namespace detail {

      bool Configure();      
      log4cxx::LevelPtr GetLogLevel();
      Logger::ptr GetLoggerFromString(std::string str);
    
    }
    
    template<typename... Args>
    Logger::ptr GetLogger(const Args&... args) {
      std::string str = common::util::varargs::ToString(args...);
      return detail::GetLoggerFromString(str);
    }
    
  }

}

#endif
