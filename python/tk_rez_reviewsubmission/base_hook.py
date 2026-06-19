"""Base Init hook for the app."""

from __future__ import annotations

import copy
import inspect
import os
from pathlib import Path
from typing import TYPE_CHECKING

import sgtk

if TYPE_CHECKING:
    from types import ModuleType

HookBaseClass = sgtk.get_hook_baseclass()


__all__ = ["BaseHook"]


class BaseHook(HookBaseClass):
    """Hook that is executed when the app is initialized.

    By default it does nothing.
    """

    @property
    def settings_class(self) -> type:
        """Return the settings class to use for the app."""
        raise NotImplementedError

    @property
    def _current_context(self) -> sgtk.Context | None:
        """Return the current context, or None if it's empty or can't be determined.

        Will attempt in order:

        1. App context
        2. Engine context
        3. Sgtk context from `.Sgtk.project_path`

        """
        result = None
        parent = self.parent
        empty_context = self.sgtk.context_empty()

        while parent and not result:
            if (
                isinstance(parent, sgtk.Sgtk)
                and (context := self.current_project_context(tk=parent))
            ) or (
                isinstance(parent, (sgtk.platform.Engine, sgtk.platform.Application))
                and (context := parent.context) != empty_context
            ):
                result = context

            if isinstance(parent, sgtk.platform.Application):
                parent = parent.engine
            elif isinstance(parent, sgtk.platform.Engine):
                parent = parent.sgtk
            else:
                parent = None

        return result

    @property
    def run_context(self) -> sgtk.Context:
        """Guaranteed context instance to run in.

        By default, it will return the current context if it's valid.
        """
        if not isinstance(context := self._current_context, sgtk.Context):
            msg = "Unable to determine a valid context to run in."
            raise TypeError(msg)

        return context

    def env_with_run_context(self) -> dict[str, str]:
        """Return a copy of the current environment with the context serialized.

        This is useful for spawning a new process with the same context as the current
        process.
        """
        env = copy.deepcopy(os.environ)
        env["TANK_CONTEXT"] = self.run_context.serialize(use_json=True)
        return env

    @property
    def tk_rez_reviewsubmission(self) -> ModuleType:
        """Return the tk-rez-reviewsubmission module."""
        return self.parent.tk_rez_reviewsubmission

    @property
    def hook_file_path(self) -> Path:
        """Return the tk-rez-reviewsubmission module."""
        if not (
            (hook_module := inspect.getmodule(self))
            and (file_str := inspect.getabsfile(hook_module))
        ):
            msg = f"Unable to determine file path of hook: {self!r}"
            raise RuntimeError(msg)

        return Path(file_str).resolve()

    def in_required_rez_env(self) -> bool:
        """Whether the current process is running in the required Rez environment."""
        raise NotImplementedError

    def in_required_runtime(self) -> bool:
        """Return True if the current process is running in the required runtime."""
        return self.in_required_rez_env()

    def app_init(self) -> None:
        """Initialise routine run when the app is initialized.

        This is called right after the hook instance is created.
        """
