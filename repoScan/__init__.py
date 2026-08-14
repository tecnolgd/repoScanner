# Version is automatically managed by setuptools_scm
try:
    from ._version import __version__
except ImportError:
    __version__ = "0.3.0.dev0"

__all__ = ["__version__"]
