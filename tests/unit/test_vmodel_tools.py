from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def run_tool(path: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, path], cwd=REPO_ROOT, text=True, capture_output=True, check=False)


def test_validate_requirements_passes() -> None:
    result = run_tool('tools/validate_requirements.py')
    assert result.returncode == 0, result.stdout + result.stderr


def test_validate_traceability_passes() -> None:
    result = run_tool('tools/validate_traceability.py')
    assert result.returncode == 0, result.stdout + result.stderr


def test_generate_trace_matrix_creates_output() -> None:
    result = run_tool('tools/generate_trace_matrix.py')
    assert result.returncode == 0, result.stdout + result.stderr
    content = (REPO_ROOT / 'vmodel/traceability/generated_trace_matrix.md').read_text(encoding='utf-8')
    assert '| StR | SyR | SwR | DDS | Code | Test | Status |' in content
    assert 'src/workflow_demo/config_loader.py' in content


def test_generate_verification_report_creates_output() -> None:
    result = run_tool('tools/generate_verification_report.py')
    assert result.returncode == 0, result.stdout + result.stderr
    content = (REPO_ROOT / 'vmodel/verification/verification_report.md').read_text(encoding='utf-8')
    assert 'Acceptance Recommendation' in content
