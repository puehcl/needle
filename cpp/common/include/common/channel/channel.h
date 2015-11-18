#ifndef COMMON_CHANNEL_CHANNEL_H
#define COMMON_CHANNEL_CHANNEL_H

#include <vector>

class Channel {
public:
  using Buffer = std::vector<char>;

  virtual ~Channel() {};
  virtual void Write(Buffer buffer) = 0;
  virtual Buffer Read() = 0;
  virtual void Close() = 0;
};

#endif
