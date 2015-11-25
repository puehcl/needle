#include <functional>
#include <iostream>

#include <boost/asio.hpp>

#include "common/channel/channel.h"
#include "common/channel/tcp_channel.h"
#include "common/logging/logger.h"
#include "common/session/session.h"
#include "common/session/local_session.h"

#include "client.h"
#include "mediator_session.h"

Client::Client( std::string mediator_host_name, unsigned short mediator_port,
                std::string local_interface,    unsigned short local_port)
              : logger_(common::logging::GetLogger("Client")),
                mediator_port_(mediator_port), 
                local_port_(local_port),
                local_acceptor_(ioservice_) {
  mediator_host_name_ =
    boost::asio::ip::address::from_string(mediator_host_name);
  local_interface_ =
    boost::asio::ip::address::from_string(local_interface);
}

void Client::Run(void) {
  logger_->Trace("entering Run");

  PrepareAcceptor();
  StartAccept();

  std::getchar();
    //setup server socket
    //listen for connection
    //on connection, spawn new thread, give the thread the tcp channel

    //thread connects to mediator

}

void Client::PrepareAcceptor() {
  boost::asio::ip::tcp::endpoint endpoint(local_interface_, local_port_);
  local_acceptor_.open(endpoint.protocol());
  local_acceptor_.set_option(
    boost::asio::ip::tcp::acceptor::reuse_address(true));
  local_acceptor_.bind(endpoint);
  local_acceptor_.listen();
}

/**
 * Starts the accept loop on the previously prepared acceptor, this function
 * runs/blocks until the client is shut down
 */
void Client::StartAccept() {
  logger_->Trace("entering StartAccept");
  bool timeout = false;
  //create a new socket which will be initialized when a new
  //connection is accepted
  std::unique_ptr<boost::asio::ip::tcp::socket> socket(
    new boost::asio::ip::tcp::socket(ioservice_));
  //run until client is shut down
  while(!shutdown_) {
    //if no accept timeout occurred, create new socket because the one in the
    //local unique_ptr is now NULL (moved to CreateRelay)
    if(!timeout) {
      socket.reset(new boost::asio::ip::tcp::socket(ioservice_));
    }
    //accept connections on the server socket and initialize the given socket
    //with the new connection
    logger_->Info("Waiting for new connection...");
    local_acceptor_.accept(*socket);
    logger_->Info("New connection accepted: ", socket->remote_endpoint());
    //further process the socket, create a relay between local connection
    //and the server
    CreateRelay(std::move(socket));
  }
}

void Client::CreateRelay(std::unique_ptr<boost::asio::ip::tcp::socket> socket) {
  std::unique_ptr<common::channel::Channel> local_channel(
    new common::channel::TCPChannel(std::move(socket)));
  std::unique_ptr<common::session::Session> local_session(
    new common::session::LocalSession(std::move(local_channel)));
  std::unique_ptr<common::session::Session> mediator_session(
  new MediatorSession());
  std::uint64_t relay_uid = common::relay::GetNextUID();
  std::unique_ptr<common::relay::Relay> relay(new common::relay::Relay(
    relay_uid,
    std::move(local_session), 
    std::move(mediator_session), 
    std::bind(&Client::OnRelayFinished, this, std::placeholders::_1)));
  relays_.insert(std::make_pair(relay_uid, std::move(relay)));
}

void Client::OnRelayFinished(const common::relay::Relay& relay) {
  relays_.erase(relay.get_uid());
}

void Client::Shutdown() {
  shutdown_ = true;
}
