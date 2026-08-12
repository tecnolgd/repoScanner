import os

try:
    import libcvault
    LIBCVAULT_AVAILABLE = True
except Exception:
    libcvault = None
    LIBCVAULT_AVAILABLE = False

_last_populated_root = None


def populate_data(root_path):
    global _last_populated_root

    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")

    if _last_populated_root != root_path:
        libcvault.populate_data(root_path)
        _last_populated_root = root_path


def ensure_populated(root_path):
    """Ensure libcvault data is loaded for the requested root."""
    populate_data(root_path)


def get_files():
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")

    raw = libcvault.get_files()
    if raw is None:
        return []

    return [item if isinstance(item, str) else item[0] for item in raw]


def sort_file_on_byte():
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")

    libcvault.sort_file_on_byte()
    results = []
    for i in range(libcvault.get_file_count()):
        name = libcvault.get_file_name(i)
        size = libcvault.get_file_size(i)
        results.append((size, name))
    return results


def get_file_count():
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.get_file_count()


def get_file_name(index):
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.get_file_name(index)


def get_file_size(index):
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.get_file_size(index)


def max_file():
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.max_file()


def search_file(filename):
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.search_file(filename)


def get_total_bytes():
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.get_total_bytes()


def line_count(file_path):
    if not LIBCVAULT_AVAILABLE:
        raise RuntimeError("libcvault is not available")
    return libcvault.line_count(file_path)
