/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   ConsoleChannel.h
 * Author: clemens
 *
 * Created on November 27, 2015, 2:26 PM
 */

#ifndef COMMON_CHANNEL_CONSOLE_CHANNEL_H
#define COMMON_CHANNEL_CONSOLE_CHANNEL_H

#include "common/channel/channel.h"
#include "common/logging/logger.h"

namespace common {
  namespace channel {
    
    class ConsoleChannel : public Channel {
    private:
      common::logging::Logger::ptr logger_;
    public:
      ConsoleChannel() 
      : logger_(common::logging::GetLogger("ConsoleChannel")) {}
      
      virtual void Write(std::string buffer) override;
      virtual std::string Read() override;
      virtual void Close() override;
      virtual void Print(std::ostream& os) const override;
    };   
    
  }
}

#endif /* COMMON_CHANNEL_CONSOLE_CHANNEL_H */

