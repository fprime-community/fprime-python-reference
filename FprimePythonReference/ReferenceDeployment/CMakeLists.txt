#####
# 'ReferenceDeployment' Deployment:
#
# This registers the 'ReferenceDeployment' deployment to the build system. 
# Custom components that have not been added at the project-level should be added to 
# the list below.
#
#####

add_fprime_subdirectory("${CMAKE_CURRENT_LIST_DIR}/Top/")

register_fprime_deployment(
    SOURCES
        "${CMAKE_CURRENT_LIST_DIR}/Main.cpp" # Needed to appease compiler
        "${CMAKE_CURRENT_LIST_DIR}/fsw_main.py" # Python entrypoint
    CHOOSES_IMPLEMENTATIONS
        FprimePython_PythonConsole
    DEPENDS
        ${FPRIME_CURRENT_MODULE}_Top
)

# The conventional C++ deployment executable links component libraries containing pybind11
# code, so it must resolve the Python C API at link time. The fprime_py extension module
# does not need this: it receives these symbols from the hosting interpreter.
# Guarded: pybind11 is not located during fprime sub-builds
if (TARGET pybind11::embed)
    target_link_libraries("${FPRIME_CURRENT_MODULE}" PRIVATE pybind11::embed)
endif()
