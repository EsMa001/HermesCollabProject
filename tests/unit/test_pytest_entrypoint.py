from __future__ import annotations

import subprocess
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_pytest_console_script_can_import_repo_packages() -> None:
    result = subprocess.run(
        ['/opt/hermes/.venv/bin/pytest', 'tests/unit/test_calculator_ui_spec.py', '-q'],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert '2 passed' in result.stdout
