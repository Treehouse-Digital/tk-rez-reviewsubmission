"""Python library for the Rez Review Submission app."""

from .base_hooks import Hook
from .rez_requirement import current_rez_resolved_packages

__all__ = ["Hook", "current_rez_resolved_packages"]
