"""App definition for the Rez Review Submission app."""

import sgtk


class RezReviewSubmissionApp(sgtk.platform.Application):
    """Rez based app to render and submit a movie to SG for review."""

    def init_app(self) -> None:
        """Run init hook."""

    @property
    def context_change_allowed(self) -> bool:
        """Always allow context changes for this app."""
        return True
