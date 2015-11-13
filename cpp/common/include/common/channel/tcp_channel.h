#ifndef COMMON_CHANNEL_TCP_CHANNEL_H
#define COMMON_CHANNEL_TCP_CHANNEL_H

//#define TCP_BUFFER_SIZE 512

#include <memory>

#include <boost/asio.hpp>

#include "common/channel/channel.h"

class TCPChannel : public Channel {
private:
  std::unique_ptr<boost::asio::ip::tcp::socket> socket_;
  Buffer buffer_;
  CallbackFunction callback_;

  void AsyncRead();
  void AsyncReadHandler(const boost::system::error_code &ec,
    const std::size_t& bytes_read);
public:
  TCPChannel(std::unique_ptr<boost::asio::ip::tcp::socket> socket);
  void OnRead(CallbackFunction callback);
  void Write(Buffer& buffer);
  void Close();
};

#endif
