from setuptools import setup

ext_modules = []
cmdclass = {}

try:

    from pybind11.setup_helpers import Pybind11Extension, build_ext

    ext_modules = [
        Pybind11Extension(
            "libcvault",
            sources=["vendor/bridge.cpp", "vendor/libcvault/main.cpp"],
            include_dirs=["vendor/libcvault"],
            cxx_std=17,
        ),
    ]
    cmdclass={"build_ext": build_ext},
except(ImportError, Exception):
    # fallback for source installs without a C++ compiler
    pass

setup(
    ext_modules = ext_modules,
    cmdclass = cmdclass
)
