#include "FprimePython/FprimePython.hpp"
#include "FprimePythonReference/ReferenceDeployment/Top/ReferenceDeploymentTopologyAc.hpp"
#include "FprimePythonReference/ReferenceDeployment/Top/ReferenceDeploymentTopologyDefs.hpp"

// Function used to bind the deployment into Python
void setup_user_deployment(pybind11::module_& m) {
    // Bind in the topology state type
    pybind11::class_<ReferenceDeployment::TopologyState>(m, "TopologyState")
        .def(pybind11::init<>())
        .def_readwrite("hostname", &ReferenceDeployment::TopologyState::hostname)
        .def_readwrite("port", &ReferenceDeployment::TopologyState::port);

    // The FileHandling subtopology requires the using topology to supply the parameter database
    // file name before parameters are read during topology setup
    FileHandling::prmDb.configure("PrmDb.dat");
}
