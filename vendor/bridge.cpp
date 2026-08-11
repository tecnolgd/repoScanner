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
    m.def("get_file_name", &getFileName, "Returns the name of the file");
    m.def("get_file_size", &getFileSize, "Returns the size of the file");
    m.def("get_files", []() {
        size_t count = 0;
        const fileStructure* ptr = getFiles(&count); // Get starting RAM address + count

        py::list result;
        if (ptr != nullptr) {
            for (size_t i = 0; i < count; ++i) {
                result.append(ptr[i].name); // return file name string only
            }
        }
        return result; // Returns a native Python list of tuples (name, size)
    }, "Returns a list of scanned files"); 
}
