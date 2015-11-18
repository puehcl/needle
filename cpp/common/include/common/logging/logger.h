#ifndef COMMON_LOGGING_LOGGING_H
#define COMMON_LOGGING_LOGGING_H

#include <iostream>
#include <memory>
#include <mutex>

#include <log4cxx/logger.h>

#define LOGGER_LOG_PATTERN "\%d{yyyy-MM-dd HH:mm:ss} \%-5p \%c: \%m\%n"

namespace common {

  namespace logging {

    class Logger {
    private:
      log4cxx::LoggerPtr internal_logger_;
            
      template<typename Arg>
      std::ostream& BuildStream(std::ostream& stream, const Arg& arg) {
        return stream << arg;
      }
      
      template<typename Arg1, typename... Args>
      std::ostream& BuildStream(std::ostream& stream, const Arg1& arg1, 
            const Args&... args) {
        return BuildStream(stream << arg1, args...);
      }
      
    public:
      using ptr = std::unique_ptr<Logger>;

      Logger(log4cxx::LoggerPtr internal_logger)
        : internal_logger_(internal_logger) {}
      
      template<typename... Args>
      void Trace(const Args&... args) {
        if(internal_logger_->isTraceEnabled()) {
          std::ostringstream stream;
          BuildStream(stream, args...);
          LOG4CXX_TRACE(internal_logger_, stream.str());
        }
      }
      
      template<typename... Args>
      void Debug(const Args&... args) {
        if(internal_logger_->isDebugEnabled()) {
          std::ostringstream stream;
          BuildStream(stream, args...);
          LOG4CXX_DEBUG(internal_logger_, stream.str());
        }
      }
      
      template<typename... Args>
      void Info(const Args&... args) {
        if(internal_logger_->isInfoEnabled()) {
          std::ostringstream stream;
          BuildStream(stream, args...);
          LOG4CXX_INFO(internal_logger_, stream.str());
        }
      }
      
      template<typename... Args>
      void Warn(const Args&... args) {
        if(internal_logger_->isWarnEnabled()) {
          std::ostringstream stream;
          BuildStream(stream, args...);
          LOG4CXX_WARN(internal_logger_, stream.str());
        }
      }
      
      template<typename... Args>
      void Error(const Args&... args) {
        if(internal_logger_->isErrorEnabled()) {
          std::ostringstream stream;
          BuildStream(stream, args...);
          LOG4CXX_ERROR(internal_logger_, stream.str());
        }
      }
      
      template<typename... Args>
      void Fatal(const Args&... args) {
        if(internal_logger_->isFatalEnabled()) {
          std::ostringstream stream;
          BuildStream(stream, args...);
          LOG4CXX_FATAL(internal_logger_, stream.str());
        }
      }
     
    };
    
    Logger::ptr GetLogger(std::string name);

    namespace detail {
      
      bool Configure();
      log4cxx::LevelPtr GetLogLevel();
    }
    
  }

}

#endif
