from setuptools import Extension, setup

try:
    import pybind11
    pybind_include = pybind11.get_include()
except ImportError:
    pybind_include = ""

ext_modules = [
    Extension(
        "libcvault",
        sources=["vendor/bridge.cpp", "vendor/libcvault/main.cpp"],
        include_dirs=[pybind_include, "vendor/libcvault"],
        language="c++",
        extra_compile_args=["-O3", "-std=c++17"],
    )
]

setup(ext_modules=ext_modules)