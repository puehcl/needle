#ifndef COMMON_CHANNEL_TCP_CHANNEL_H
#define COMMON_CHANNEL_TCP_CHANNEL_H

#define TCP_BUFFER_SIZE 512

#include <memory>

#include <boost/asio/ip/tcp.hpp>

#include "common/channel/channel.h"

namespace common {
  namespace channel {

    class TCPChannel : public Channel {
    private:
      std::unique_ptr<boost::asio::ip::tcp::socket> socket_;
    public:
      TCPChannel(std::unique_ptr<boost::asio::ip::tcp::socket> socket);
      virtual void Write(std::string buffer) override;
      virtual std::string Read() override;
      virtual void Close() override;
    };

  }
}

#endif
