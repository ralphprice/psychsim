"""modular -- the neutral plug-in module system (psychology-free platform infra)."""
from .registry import Module, discover_modules

__all__ = ["Module", "discover_modules"]
