cmake_minimum_required(VERSION 2.8)   #1  指定 cmake 的最小版本
project(cc_blackbox)                     #2  设置项目名
set (CMAKE_CXX_FLAGS "-lstdc++fs -std=c++17")

include_directories(./)

set(SRC                               #4  添加可执行源文件
   ./main.cpp
  )
add_executable(cc_blackbox ${SRC})

