"""
Implements:
- SwR-001

Design:
- DDS-001
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


def load_run_configuration(config_path: str | Path) -> dict[str, Any]:
    path = Path(config_path)
    with path.open('r', encoding='utf-8') as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError('Configuration root must be a mapping.')
    return data
