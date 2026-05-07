from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def test_codex_preflight_check_only_passes_on_branch() -> None:
    env = os.environ.copy()
    env['HERMES_BRANCH_OVERRIDE'] = 'hermes/test-swr-gate'
    result = subprocess.run(
        [sys.executable, 'tools/run_codex_for_swr.py', '--swr', 'SwR-001', '--check-only'],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert 'Preflight passed for: SwR-001' in result.stdout
    generated = REPO_ROOT / 'prompts' / 'generated_swr-001.md'
    assert generated.exists()
    content = generated.read_text(encoding='utf-8')
    assert 'SwR-001: Load run configuration from explicit file path' in content
    assert 'Linked Tests: TC-SwR-001-001' in content


def test_codex_execute_fails_cleanly_when_cli_missing() -> None:
    env = os.environ.copy()
    env['PATH'] = '/usr/bin:/bin'
    env['HERMES_BRANCH_OVERRIDE'] = 'hermes/test-swr-gate'
    result = subprocess.run(
        [sys.executable, 'tools/run_codex_for_swr.py', '--swr', 'SwR-001'],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
        check=False,
        env=env,
    )
    assert result.returncode == 1
    assert 'ERROR: codex CLI not found in PATH' in result.stdout
