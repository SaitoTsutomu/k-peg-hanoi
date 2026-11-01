from importlib.metadata import metadata

from .core import hanoi, main, nmove, show_hanoi

_package_metadata = metadata(__package__)  # ruff: ignore[non-empty-init-module] # type: ignore[bad-argument-type]
__version__ = _package_metadata["Version"]
__author__ = _package_metadata.get("Author-email", "")
__all__ = ["hanoi", "main", "nmove", "show_hanoi"]
