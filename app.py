"""App definition for the Rez Review Submission app."""

import sgtk


class RezReviewSubmissionApp(sgtk.platform.Application):
    """Rez based app to render and submit a movie to SG for review."""

    def init_app(self) -> None:
        """Run init hook."""
        self.tk_rez_reviewsubmission = self.import_module("tk_rez_reviewsubmission")

        self.init_hook = self.create_hook_instance(
            "init_hook", base_class=self.tk_rez_reviewsubmission.base_hooks.InitHook
        )
        self.init_hook.pre()

        self.settings_hook = self.create_hook_instance("settings_hook")
        self.run_hook = self.create_hook_instance("run_hook")

        self.init_hook.post()

    @property
    def context_change_allowed(self) -> bool:
        """Always allow context changes for this app."""
        return True
