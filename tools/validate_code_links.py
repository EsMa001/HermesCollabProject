#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

from _vmodel_common import REPO_ROOT, git_changed_files, production_files, print_errors, trace_links, main_guard

def has_metadata(path: Path) -> bool:
    text = path.read_text(encoding='utf-8')
    return 'Implements:' in text or 'Design:' in text

def linked_python_files() -> set[str]:
    linked: set[str] = set()
    for link in trace_links():
        if str(link.get('from', '')).endswith('.py'):
            linked.add(link['from'])
        if str(link.get('to', '')).endswith('.py'):
            linked.add(link['to'])
    return linked

def validate() -> int:
    changed, branch = git_changed_files()
    candidates = set(production_files())
    linked = linked_python_files()
    errors: list[str] = []
    if branch is None:
        files = candidates
    else:
        files = {path for path in changed if path in candidates} or candidates
        if branch == 'main':
            print('WARNING: current branch is main; implementation tasks should use a non-main branch')
    for rel in sorted(files):
        path = REPO_ROOT / rel
        if rel not in linked:
            errors.append(f'{rel} has no trace link to a SwR or DDS')
        if path.exists() and not has_metadata(path):
            errors.append(f'{rel} is missing Implements:/Design: metadata')
    return print_errors(errors, 'Code-link validation passed.')

if __name__ == '__main__':
    main_guard(validate)
