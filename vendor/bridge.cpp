#include <pybind11/pybind11.h>
#include "head.hpp" // Including your libcvault header

namespace py = pybind11;

PYBIND11_MODULE(libcvault, m) {
    m.doc() = "Python bindings for libcvault file metadata analyzer";

    // Expose libcvault C++ functions directly to Python
    m.def("populate_data", &populateData, "Scan directory and load metadata");
    m.def("get_file_count", &getFileCount, "Return number of loaded files");
    m.def("get_total_bytes", &getTotalBytes, "Return total byte size of loaded files");
    m.def("sort_file_on_byte", &sortFileOnByte, "Sort files by size(Ascending)");
    m.def("sort_file_on_name", &sortFileOnName, "Sort files by name(a-z)");
    m.def("search_file", &searchFile, "Search a file by name");
    m.def("max_file", &maxFile, "Return largest file(based on size)");
    m.def("line_count", &lineCount, "Count lines in a file");
}
