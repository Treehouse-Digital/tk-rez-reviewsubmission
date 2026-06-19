"""Base Init hook for the app."""

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class InitHook(HookBaseClass):
    """Hook that is executed when the app is initialized.

    By default it does nothing.
    """

    def pre(self) -> None:
        """Run any routines pre settings/run hook creation (by default, nothing)."""

    def post(self) -> None:
        """Run any routines post settings/run hook creation (by default, nothing)."""
