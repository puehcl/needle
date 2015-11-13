
#ifndef CLIENT_CLIENT_H
#define CLIENT_CLIENT_H

#include <string>
#include <thread>

#include <boost/asio.hpp>

class Client {
private:
  bool shutdown_{false};
  boost::asio::ip::address mediator_host_name_;
  boost::asio::ip::address local_interface_;
  unsigned short mediator_port_;
  unsigned short local_port_;
  boost::asio::io_service ioservice_;
  boost::asio::ip::tcp::acceptor local_acceptor_;

  void PrepareAcceptor();
  void StartAccept();
  void CreateRelay(std::unique_ptr<boost::asio::ip::tcp::socket> socket);
public:
  Client( std::string mediator_host_name, unsigned short mediator_port,
          std::string local_interface,    unsigned short local_port);
  void Run();
  void Shutdown();
};

#endif
