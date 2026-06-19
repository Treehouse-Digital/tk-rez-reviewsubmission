"""Hook, settings and CLI runtime."""

from __future__ import annotations

import argparse
import dataclasses
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import TYPE_CHECKING

import sgtk

if TYPE_CHECKING:
    import shotgun_api3

HookBaseClass = sgtk.get_hook_baseclass()


@dataclasses.dataclass
class Settings:
    """Settings for the Nuke render color bars hook."""

    out_path: str
    out_settings: dict = dataclasses.field(default_factory=dict)
    color_bars_format: str = "256 256 0 0 256 256 1 square_256"
    color_bars_name: str = "ColorBars1"


class Hook(HookBaseClass):
    """Implement basic Nuke graph creation dispatch routines."""

    @property
    def settings_class(self) -> type:
        """Return the settings class to use for the app."""
        return Settings

    def in_required_rez_env(self) -> bool:
        """Whether the current process is running in the required Rez environment."""
        return {"nuke", "tk_core"} & set(self.current_rez_resolved_packages())

    def run_in_rez_subprocess(self, settings: Settings) -> None:
        """Spawn a new process in the required runtime with the given settings."""
        env: dict = self.env_with_run_context()
        cmd_args = ["rez", "env", "nuke-14.1", "tk_core", "--", "Nuke14.1", "-t"]

        with tempfile.NamedTemporaryFile(mode="w", suffix=".json") as temp_file:
            temp_file.write(json.dumps(dataclasses.asdict(settings)))
            temp_file.flush()

            cmd_args += [str(self.hook_file_path), str(Path(temp_file.name).resolve())]
            subprocess.run(cmd_args, check=True, capture_output=True, env=env)

    def run(self, settings: Settings) -> None:
        """Run the main routine with the given settings and app's context."""
        return main(settings, self.parent.context)


def main(settings: Settings, context: sgtk.Context) -> None:
    """Run main runtime routine."""
    import nuke  # noqa: PLC0415  # in-case this file was imported outside Nuke

    tk: sgtk.Sgtk = context.sgtk
    sg: shotgun_api3.Shotgun = tk.shotgun
    nuke.tprint(str(sg))

    color_bar_node = nuke.nodes.ColorBars(
        name=settings.color_bars_name, format=settings.color_bars_format
    )
    color_bar_node.seSelected(True)  # noqa: FBT003

    write_node = nuke.nodes.Write(name="WriteColorBars", file_type="mov")
    write_node.setInput(0, color_bar_node)
    write_node.seSelected(True)  # noqa: FBT003

    for knob_name, knob_value in settings.out_settings.items():
        knob = write_node.knob(knob_name)
        if isinstance(knob, nuke.Knob) and knob_value is not None:
            knob.setValue(knob_value)

    _, temp_file_path_str = tempfile.mkstemp(suffix=".nk")
    temp_file_path = Path(temp_file_path_str).resolve()
    try:
        nuke.nodeCopy(temp_file_path_str)
        nuke.tprint(temp_file_path.read_text())
    finally:
        temp_file_path.unlink(missing_ok=True)


def _cli() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("JSON_PATH", type=Path)
    args = parser.parse_args()

    settings = Settings(**json.loads(args.JSON_PATH.read_text()))
    context = sgtk.Context.deserialize(os.environ["TANK_CONTEXT"])
    main(settings, context)


if __name__ == "__main__":
    _cli()
