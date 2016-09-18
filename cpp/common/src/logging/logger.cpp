/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

#include "common/logging/logger.h"

namespace common {

  namespace logging {

    namespace detail {
      
      static bool configured{Configure()};
      
      bool Configure() {
        log4cxx::LayoutPtr layout(new log4cxx::PatternLayout(LOGGER_LOG_PATTERN));
        log4cxx::AppenderPtr console_appender = 
          new log4cxx::ConsoleAppender(layout);
        log4cxx::BasicConfigurator::configure(console_appender);
        log4cxx::Logger::getRootLogger()->setLevel(GetLogLevel());
        return true;
      }
      
      log4cxx::LevelPtr GetLogLevel() {
        switch(LOG_LEVEL) {
          case(LOG_LEVEL_FATAL):
            return log4cxx::Level::getFatal();
          case(LOG_LEVEL_ERROR):
            return log4cxx::Level::getError();
          case(LOG_LEVEL_WARN):
            return log4cxx::Level::getWarn();
          case(LOG_LEVEL_INFO):
            return log4cxx::Level::getInfo();
          case(LOG_LEVEL_DEBUG):
            return log4cxx::Level::getDebug();
          case(LOG_LEVEL_TRACE):
          default:
            return log4cxx::Level::getTrace();
        }
      }
      
      Logger::ptr GetLoggerFromString(std::string str) {
        return Logger::ptr(new Logger(log4cxx::Logger::getLogger(str)));
      }
      
    }   
  }
}