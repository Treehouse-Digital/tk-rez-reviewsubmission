"""App definition for the Rez Review Submission app."""

from typing import TypeAlias

import sgtk

Settings: TypeAlias = type


class RezReviewSubmissionApp(sgtk.platform.Application):
    """Rez based app to render and submit a movie to SG for review."""

    def init_app(self) -> None:
        """Run init hook."""
        self.tk_rez_reviewsubmission = self.import_module("tk_rez_reviewsubmission")
        self.hook = self.create_hook_instance(
            "hook", base_class=self.tk_rez_reviewsubmission.BaseHook
        )
        self.hook.app_init()

    @property
    def context_change_allowed(self) -> bool:
        """Always allow context changes for this app."""
        return True

    @property
    def settings_class(self) -> Settings:
        """Return the runtime settings class."""
        return self.hook.settings_class

    def submit(self, settings: Settings) -> object:
        """Run the submit hook."""
        return (
            self.hook.run(settings)
            if self.hook.in_required_runtime()
            else self.hook.run_in_rez_subprocess(settings)
        )
