
#include <boost/asio/write.hpp>

#include "common/channel/tcp_channel.h"

namespace common {
  namespace channel {

    TCPChannel::TCPChannel(
        std::unique_ptr<boost::asio::ip::tcp::socket> socket) {
      socket_ = std::move(socket);
    }

    void TCPChannel::Write(std::string buffer) {
      //send all data in the buffer
      boost::asio::write(*socket_, boost::asio::buffer(buffer, buffer.size()));
    }

    std::string TCPChannel::Read() {
      std::size_t bytes_read;
      char buffer[TCP_BUFFER_SIZE];
      bytes_read = socket_->receive(boost::asio::buffer(buffer));
      return std::string(buffer, bytes_read);
    }

    void TCPChannel::Close() {
      boost::system::error_code ec;
      //shutdown send and receive functionality on the socket
      socket_->shutdown(boost::asio::ip::tcp::socket::shutdown_both, ec);
      if(ec) {

      }
      socket_->close(ec);
      if(ec) {

      }
    }

  }
}
