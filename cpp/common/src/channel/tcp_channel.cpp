
#include "common/channel/tcp_channel.h"

TCPChannel::TCPChannel(std::unique_ptr<boost::asio::ip::tcp::socket> socket) {
  socket_ = std::move(socket);
}

void TCPChannel::AsyncRead() {
  socket_->async_read_some(
    boost::asio::buffer(buffer_),
    std::bind(
      &TCPChannel::AsyncReadHandler,
      this,
      std::placeholders::_1,
      std::placeholders::_2
  ));
}

void TCPChannel::AsyncReadHandler(  const boost::system::error_code &ec,
                                    const std::size_t& bytes_read) {
  if(!ec) {
    callback_(buffer_, bytes_read);
    AsyncRead();
  }
}

void TCPChannel::OnRead(CallbackFunction callback) {
  callback_ = callback;
  AsyncRead();
}

void TCPChannel::Write(Buffer& buffer) {

}

void TCPChannel::Close() {

}
