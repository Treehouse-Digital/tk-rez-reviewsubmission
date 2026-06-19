"""Library for parsing rez context and version requirements."""

import json
import os
from pathlib import Path

__all__ = ["current_rez_resolved_packages"]


def current_rez_resolved_packages() -> dict[str, str]:
    """Get currently resolved packages from the REZ_RXT_FILE, if any."""
    data: dict = (
        json.loads(Path(rxt_path_str).read_text())
        if (rxt_path_str := os.getenv("REZ_RXT_FILE"))
        else {}
    )
    return {
        name: version
        for pkg in data.get("resolved_packages", [])
        if isinstance(pkg_vars := pkg.get("variables"), dict)
        and (name := pkg_vars.get("name"))
        and (version := pkg_vars.get("version"))
    }
