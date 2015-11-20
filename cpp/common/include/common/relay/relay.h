#ifndef COMMON_RELAY_RELAY_H
#define COMMON_RELAY_RELAY_H

#include <memory>

#include "common/session/session.h"

class Relay {
private:
  std::unique_ptr<Session> session1_;
  std::unique_ptr<Session> session2_;
public:
  Relay(  std::unique_ptr<Session>& session1,
          std::unique_ptr<Session>& session2) {
    session1_ = std::move(session1);
    session2_ = std::move(session2);
  }
};

#endif
