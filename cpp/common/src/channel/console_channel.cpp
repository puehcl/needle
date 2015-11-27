/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

#include <iostream>

#include "common/channel/console_channel.h"

namespace common {
  namespace channel {
    
    void ConsoleChannel::Write(std::string buffer) {
      std::cout << buffer << std::endl;
    }
    
    std::string ConsoleChannel::Read() {
      logger_->Debug("Reading line on stdin");
      std::string line;
      std::getline(std::cin, line);
      logger_->Debug("Read line on stdin, returning");
      return line;
    }
    
    void ConsoleChannel::Close() {
      
    }
    
  }
}