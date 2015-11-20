#ifndef COMMON_CHANNEL_TCP_CHANNEL_H
#define COMMON_CHANNEL_TCP_CHANNEL_H

#define TCP_BUFFER_SIZE 512

#include <memory>

#include <boost/asio/ip/tcp.hpp>

#include "common/channel/channel.h"

class TCPChannel : public Channel {
private:
  std::unique_ptr<boost::asio::ip::tcp::socket> socket_;
public:
  TCPChannel(std::unique_ptr<boost::asio::ip::tcp::socket> socket);
  virtual void Write(Buffer buffer) override;
  virtual Buffer Read() override;
  virtual void Close();
};

#endif
