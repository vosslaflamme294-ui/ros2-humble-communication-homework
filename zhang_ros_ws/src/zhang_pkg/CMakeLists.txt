cmake_minimum_required(VERSION 3.8)
project(zhang_pkg)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/StudentInfo.msg"
  "srv/AddTwoInts.srv"
  "action/CountUntil.action"
  DEPENDENCIES builtin_interfaces std_msgs
)

install(PROGRAMS
  scripts/student_publisher.py
  scripts/student_subscriber.py
  scripts/add_two_ints_server.py
  scripts/add_two_ints_client.py
  scripts/count_until_action_server.py
  scripts/count_until_action_client.py
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY launch
  DESTINATION share/${PROJECT_NAME}
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
