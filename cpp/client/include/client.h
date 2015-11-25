
#ifndef CLIENT_CLIENT_H
#define CLIENT_CLIENT_H

#include <cstdint>
#include <memory>
#include <string>
#include <thread>
#include <unordered_map>

#include <boost/asio.hpp>

#include "common/logging/logger.h"
#include "common/relay/relay.h"

class Client {
private:
  common::logging::Logger::ptr logger_;
  bool shutdown_{false};
  boost::asio::ip::address mediator_host_name_;
  boost::asio::ip::address local_interface_;
  unsigned short mediator_port_;
  unsigned short local_port_;
  boost::asio::io_service ioservice_;
  boost::asio::ip::tcp::acceptor local_acceptor_;
  std::unordered_map< std::uint64_t, 
                      std::unique_ptr<common::relay::Relay>> relays_;

  void PrepareAcceptor();
  void StartAccept();
  void CreateRelay(std::unique_ptr<boost::asio::ip::tcp::socket> socket);
  void OnRelayFinished(const common::relay::Relay& relay);
public:
  Client( std::string mediator_host_name, unsigned short mediator_port,
          std::string local_interface,    unsigned short local_port);
  void Run();
  void Shutdown();
};

#endif
