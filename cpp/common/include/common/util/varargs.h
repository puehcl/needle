/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/* 
 * File:   varargs.h
 * Author: clemens
 *
 * Created on November 30, 2015, 11:33 AM
 */

#ifndef COMMON_UTIL_VARARGS_H
#define COMMON_UTIL_VARARGS_H

#include <sstream>

namespace common {
  
  namespace util {
    
    namespace varargs {
      
      namespace detail {
   
        template<typename Arg>
        std::ostream& BuildStream(std::ostream& stream, const Arg& arg) {
          return stream << arg;
        }

        template<typename Arg1, typename... Args>
        std::ostream& BuildStream(std::ostream& stream, const Arg1& arg1, 
            const Args&... args) {
          return BuildStream(stream << arg1, args...);
        }
        
      }
    
      template<typename... Args>
      std::string ToString(const Args&... args) {
        std::stringstream stream;
        detail::BuildStream(stream, args...);
        return stream.str();
      }
    
    }
    
  }
  
}


#endif /* COMMON_UTIL_VARARGS_H */

