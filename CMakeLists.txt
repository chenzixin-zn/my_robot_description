cmake_minimum_required(VERSION 3.8)
project(agx_arm_description)

find_package(ament_cmake REQUIRED)

# Install the description directories that actually exist in this checkout so
# package://agx_arm_description/... URIs resolve without install-time failures.
set(AGX_DESCRIPTION_DIRS)
foreach(dir nero piper piper_h piper_l piper_x revo2)
  if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/${dir}")
    list(APPEND AGX_DESCRIPTION_DIRS "${dir}")
  endif()
endforeach()

install(DIRECTORY ${AGX_DESCRIPTION_DIRS}
  DESTINATION share/${PROJECT_NAME}
)

# Backward-compatibility layout for packages that still reference the legacy
# agx_arm_urdf/<arm_type>/... paths inside agx_arm_description. Install only
# data directories needed by downstream includes/mesh URIs to avoid duplicate
# launch file names within the package share directory.
set(AGX_NERO_COMPAT_DIRS urdf meshes config rviz srdf)
foreach(dir IN LISTS AGX_NERO_COMPAT_DIRS)
  if(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/nero/${dir}")
    install(DIRECTORY "nero/${dir}"
      DESTINATION share/${PROJECT_NAME}/agx_arm_urdf/nero
    )
  endif()
endforeach()

ament_package()
