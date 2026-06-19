"""Init hook for the app."""

import sgtk

HookBaseClass = sgtk.get_hook_baseclass()


class InitHook(HookBaseClass):
    """Hook that is executed when the app is initialized.

    Use this to setup any menu actions for the engine.
    """
