find_path(
  OGG_INCLUDE_DIRS
  NAMES
  ogg
  PATHS
  include)

find_library(
  OGG_LIBRARIES
  NAMES
  ogg libogg_static
  PATHS
  lib)

include(FindPackageHandleStandardArgs)

find_package_handle_standard_args(OGG REQUIRED_VARS OGG_LIBRARIES OGG_INCLUDE_DIRS)
