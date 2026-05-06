from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
VMODEL_ROOT = REPO_ROOT / 'vmodel'

def read_yaml(path: Path) -> Any:
    with path.open('r', encoding='utf-8') as handle:
        data = yaml.safe_load(handle)
    return data if data is not None else []

def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def load_requirement_sets() -> dict[str, Any]:
    return {
        'stakeholder': read_yaml(VMODEL_ROOT / 'requirements' / 'stakeholder_requirements.yaml'),
        'system': read_yaml(VMODEL_ROOT / 'requirements' / 'system_requirements.yaml'),
        'software': read_yaml(VMODEL_ROOT / 'requirements' / 'software_requirements.yaml'),
        'tests': read_yaml(VMODEL_ROOT / 'verification' / 'test_specifications.yaml'),
        'traceability': read_yaml(VMODEL_ROOT / 'traceability' / 'trace_links.yaml'),
        'changes': read_yaml(VMODEL_ROOT / 'change' / 'stakeholder_change_requests.yaml'),
        'design': read_yaml(VMODEL_ROOT / 'architecture' / 'design_decisions.yaml'),
        'quality_plan': read_yaml(VMODEL_ROOT / 'project' / 'quality_plan.yaml'),
    }

def trace_links() -> list[dict[str, Any]]:
    return load_requirement_sets()['traceability'].get('links', [])

def trace_waivers() -> list[dict[str, Any]]:
    return load_requirement_sets()['traceability'].get('waivers', [])

def git_changed_files() -> tuple[list[str], str | None]:
    try:
        branch = subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], cwd=REPO_ROOT, text=True).strip()
        output = subprocess.check_output(['git', 'status', '--porcelain'], cwd=REPO_ROOT, text=True)
    except Exception:
        return [], None
    changed: list[str] = []
    for line in output.splitlines():
        path = line[3:].strip()
        if ' -> ' in path:
            path = path.split(' -> ', 1)[1]
        changed.append(path)
    return changed, branch

def production_files() -> list[str]:
    files: list[str] = []
    root = REPO_ROOT / 'src'
    if root.exists():
        for path in sorted(root.rglob('*.py')):
            files.append(path.relative_to(REPO_ROOT).as_posix())
    return files

def print_errors(errors: list[str], success_message: str) -> int:
    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return 1
    print(success_message)
    return 0

def main_guard(fn):
    try:
        raise SystemExit(fn())
    except BrokenPipeError:
        raise SystemExit(1)
    except SystemExit:
        raise
    except Exception as exc:
        print(f'ERROR: unexpected exception: {exc}', file=sys.stderr)
        raise SystemExit(1)
