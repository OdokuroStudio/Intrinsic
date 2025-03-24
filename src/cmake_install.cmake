# Install script for directory: /home/zss/Intrinsic/craftium/src

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/usr/local")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
           CMAKE_INSTALL_CONFIG_NAME "${BUILD_TYPE}")
  else()
    set(CMAKE_INSTALL_CONFIG_NAME "Release")
  endif()
  message(STATUS "Install configuration: \"${CMAKE_INSTALL_CONFIG_NAME}\"")
endif()

# Set the component getting installed.
if(NOT CMAKE_INSTALL_COMPONENT)
  if(COMPONENT)
    message(STATUS "Install component: \"${COMPONENT}\"")
    set(CMAKE_INSTALL_COMPONENT "${COMPONENT}")
  else()
    set(CMAKE_INSTALL_COMPONENT)
  endif()
endif()

# Install shared libraries without execute permission?
if(NOT DEFINED CMAKE_INSTALL_SO_NO_EXE)
  set(CMAKE_INSTALL_SO_NO_EXE "1")
endif()

# Is this installation the result of a crosscompile?
if(NOT DEFINED CMAKE_CROSSCOMPILING)
  set(CMAKE_CROSSCOMPILING "FALSE")
endif()

# Set default install directory permissions.
if(NOT DEFINED CMAKE_OBJDUMP)
  set(CMAKE_OBJDUMP "/usr/bin/objdump")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/minetest" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/minetest")
    file(RPATH_CHECK
         FILE "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/minetest"
         RPATH "")
  endif()
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/bin" TYPE EXECUTABLE FILES "/home/zss/Intrinsic/craftium/bin/minetest")
  if(EXISTS "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/minetest" AND
     NOT IS_SYMLINK "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/minetest")
    if(CMAKE_INSTALL_DO_STRIP)
      execute_process(COMMAND "/usr/bin/strip" "$ENV{DESTDIR}${CMAKE_INSTALL_PREFIX}/bin/minetest")
    endif()
  endif()
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/be/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/be/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/bg/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/bg/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ca/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ca/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/cs/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/cs/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/cy/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/cy/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/da/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/da/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/de/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/de/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/el/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/el/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/eo/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/eo/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/es/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/es/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/et/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/et/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/eu/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/eu/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/fa/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/fa/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/fi/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/fi/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/fil/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/fil/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/fr/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/fr/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ga/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ga/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/gd/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/gd/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/gl/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/gl/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/hu/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/hu/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ia/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ia/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/id/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/id/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/it/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/it/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ja/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ja/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/jbo/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/jbo/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/jv/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/jv/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/kk/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/kk/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ko/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ko/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ky/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ky/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/lt/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/lt/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/lv/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/lv/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/lzh/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/lzh/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/mi/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/mi/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/mn/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/mn/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/mr/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/mr/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ms/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ms/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/nb/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/nb/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/nl/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/nl/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/nn/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/nn/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/oc/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/oc/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/pl/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/pl/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/pt/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/pt/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/pt_BR/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/pt_BR/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ro/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ro/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/ru/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/ru/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/sk/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/sk/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/sl/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/sl/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/sr_Cyrl/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/sr_Cyrl/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/sr_Latn/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/sr_Latn/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/sv/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/sv/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/sw/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/sw/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/tr/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/tr/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/tt/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/tt/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/uk/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/uk/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/vi/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/vi/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/yue/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/yue/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/zh_CN/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/zh_CN/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/locale/zh_TW/LC_MESSAGES" TYPE FILE FILES "/home/zss/Intrinsic/craftium/locale/zh_TW/LC_MESSAGES/minetest.mo")
endif()

if(CMAKE_INSTALL_COMPONENT STREQUAL "Unspecified" OR NOT CMAKE_INSTALL_COMPONENT)
  file(INSTALL DESTINATION "${CMAKE_INSTALL_PREFIX}/." TYPE DIRECTORY FILES "/home/zss/Intrinsic/craftium/src/../fonts" FILES_MATCHING REGEX "/[^/]*\\.ttf$" REGEX "/[^/]*\\.txt$")
endif()

if(NOT CMAKE_INSTALL_LOCAL_ONLY)
  # Include the install script for each subdirectory.
  include("/home/zss/Intrinsic/craftium/src/threading/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/content/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/database/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/gui/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/mapgen/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/network/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/script/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/unittest/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/benchmark/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/util/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/irrlicht_changes/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/server/cmake_install.cmake")
  include("/home/zss/Intrinsic/craftium/src/client/cmake_install.cmake")

endif()

