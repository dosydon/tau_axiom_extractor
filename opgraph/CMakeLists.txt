cmake_minimum_required(VERSION 3.2)
# set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
# set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

FIND_PACKAGE(PythonLibs 3.4)
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})
include(GenerateExportHeader)
set(CMAKE_SWIG_OUTDIR ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR})

include_directories(
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${PROJECT_BINARY_DIR}
    ${PYTHON_INCLUDE_PATH}
)

set(EXAM_SRCS
    opgraph.h
    opgraph.cc
)

set(INTERFACE_FILES
    opgraph.i
)

# set_source_files_properties(${INTERFACE_FILES} PROPERTIES CPLUSPLUS ON SWIG_FLAGS "-py3")
set_source_files_properties(${INTERFACE_FILES} PROPERTIES CPLUSPLUS ON )
swig_add_module(opgraph python ${INTERFACE_FILES}
    ${EXAM_SRCS}
)

swig_link_libraries(opgraph
    ${PYTHON_LIBRARIES}
    emon
)
