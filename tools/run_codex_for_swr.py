#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from _vmodel_common import REPO_ROOT, load_requirement_sets, trace_links, main_guard, write_text

ALLOWED_SWR_STATUS = {'accepted_by_agent', 'accepted_by_user'}
ALLOWED_SYR_STATUS = {'accepted_by_agent', 'accepted_by_user'}
ALLOWED_CR_STATUS = {'accepted', 'implemented'}


def build_indexes() -> dict[str, dict[str, dict]]:
    data = load_requirement_sets()
    return {
        'stakeholder': {item['id']: item for item in data['stakeholder']},
        'system': {item['id']: item for item in data['system']},
        'software': {item['id']: item for item in data['software']},
        'tests': {item['id']: item for item in data['tests']},
        'changes': {item['id']: item for item in data['changes']},
    }


def current_branch() -> str | None:
    override = os.environ.get('HERMES_BRANCH_OVERRIDE')
    if override:
        return override
    try:
        return subprocess.check_output(['git', 'branch', '--show-current'], cwd=REPO_ROOT, text=True).strip() or None
    except Exception:
        return None


def links_of_type(link_type: str) -> list[dict]:
    return [link for link in trace_links() if link.get('type') == link_type]


def parents_for(child_id: str, link_type: str = 'derives') -> list[str]:
    return [link['to'] for link in links_of_type(link_type) if link.get('from') == child_id]


def children_for(parent_id: str, link_type: str = 'derives') -> list[str]:
    return [link['from'] for link in links_of_type(link_type) if link.get('to') == parent_id]


def tests_for_requirement(requirement_id: str) -> list[str]:
    return sorted({link['from'] for link in links_of_type('verifies') if link.get('to') == requirement_id})


def impacts_for_swr(swr_id: str) -> list[str]:
    return sorted({link['from'] for link in links_of_type('impacts') if link.get('to') == swr_id})


def preflight(swr_ids: list[str]) -> tuple[list[str], dict[str, dict]]:
    indexes = build_indexes()
    errors: list[str] = []
    branch = current_branch()
    if branch is None:
        errors.append('git branch unavailable')
    elif branch == 'main':
        errors.append('current branch is main; Codex execution must run on a non-main branch')

    for swr_id in swr_ids:
        swr = indexes['software'].get(swr_id)
        if swr is None:
            errors.append(f'{swr_id} not found in software_requirements.yaml')
            continue
        if swr.get('status') not in ALLOWED_SWR_STATUS:
            errors.append(f'{swr_id} has disallowed status {swr.get("status")}')
        if swr.get('open_questions'):
            errors.append(f'{swr_id} has open_questions')
        if swr.get('assumptions'):
            errors.append(f'{swr_id} has unresolved assumptions: {swr.get("assumptions")}')
        linked_tests = tests_for_requirement(swr_id)
        if not linked_tests:
            errors.append(f'{swr_id} has no linked test specification')
        parent_syr_ids = parents_for(swr_id)
        if not parent_syr_ids:
            errors.append(f'{swr_id} has no parent SyR via traceability links')
        for syr_id in parent_syr_ids:
            syr = indexes['system'].get(syr_id)
            if syr is None:
                errors.append(f'{swr_id} parent {syr_id} missing from system requirements')
                continue
            if syr.get('status') not in ALLOWED_SYR_STATUS:
                errors.append(f'{swr_id} parent {syr_id} has disallowed status {syr.get("status")}')
            if syr.get('open_questions'):
                errors.append(f'{swr_id} parent {syr_id} has open_questions')
            if syr.get('assumptions'):
                errors.append(f'{swr_id} parent {syr_id} has unresolved assumptions: {syr.get("assumptions")}')
            parent_str_ids = parents_for(syr_id)
            if not parent_str_ids:
                errors.append(f'{swr_id} parent {syr_id} has no parent StR via traceability links')
            for str_id in parent_str_ids:
                st = indexes['stakeholder'].get(str_id)
                if st is None:
                    errors.append(f'{swr_id} ancestor {str_id} missing from stakeholder requirements')
                    continue
                if st.get('status') != 'accepted':
                    errors.append(f'{swr_id} ancestor {str_id} is not accepted (status={st.get("status")})')
        impacting_crs = impacts_for_swr(swr_id)
        if not impacting_crs:
            # allowed for greenfield SwR, but in this scaffold we expect at least trace lineage
            pass
        for cr_id in impacting_crs:
            cr = indexes['changes'].get(cr_id)
            if cr is None:
                errors.append(f'{swr_id} linked CR {cr_id} missing from change requests')
                continue
            if cr.get('status') not in ALLOWED_CR_STATUS:
                errors.append(f'{swr_id} linked CR {cr_id} has disallowed status {cr.get("status")}')
    return errors, indexes


def build_prompt(swr_ids: list[str], indexes: dict[str, dict]) -> str:
    lines = [
        'You are working in a requirements-driven V-Model-light repository.',
        '',
        'Implement exactly the following approved Software Requirement scope:',
        '',
    ]
    for swr_id in swr_ids:
        swr = indexes['software'][swr_id]
        parent_syr_ids = parents_for(swr_id)
        parent_trace = []
        for syr_id in parent_syr_ids:
            parent_trace.append(syr_id)
            for str_id in parents_for(syr_id):
                parent_trace.append(str_id)
        linked_tests = tests_for_requirement(swr_id)
        lines.extend([
            f'{swr_id}: {swr["title"]}',
            f'Statement: {swr["statement"]}',
            f'Verification method: {swr["verification_method"]}',
            f'Parent Trace: {" -> ".join([swr_id] + parent_trace)}',
            f'Linked Tests: {", ".join(linked_tests) if linked_tests else "None"}',
            '',
        ])
    lines.extend([
        'Allowed scope:',
        '- Implement only behavior required by the listed SwR IDs.',
        '- Add or update only tests linked to those SwR IDs.',
        '- Update traceability only if needed for the listed requirement scope.',
        '- Do not implement speculative features.',
        '- Do not refactor unrelated code.',
        '- Do not modify unrelated requirements.',
        '',
        'Required checks:',
        '- python3 tools/validate_requirements.py',
        '- python3 tools/validate_traceability.py',
        '- python3 tools/validate_code_links.py',
        '- python3 tools/generate_trace_matrix.py',
        '- python3 tools/generate_verification_report.py',
        '- pytest',
        '',
        'Stop and report clarification_needed if:',
        '- any SwR is ambiguous',
        '- required input/output behavior is undefined',
        '- existing architecture conflicts with the requested implementation',
        '- the current branch is main',
        '',
    ])
    return '\n'.join(lines)


def run(args: argparse.Namespace) -> int:
    swr_ids = args.swr
    errors, indexes = preflight(swr_ids)
    if errors:
        for error in errors:
            print(f'ERROR: {error}')
        return 1

    prompt_text = build_prompt(swr_ids, indexes)
    prompt_path = Path(args.prompt_out) if args.prompt_out else REPO_ROOT / 'prompts' / f'generated_{"_".join(swr_ids).lower()}.md'
    write_text(prompt_path, prompt_text + '\n')
    print(f'Preflight passed for: {", ".join(swr_ids)}')
    print(f'Prompt written to: {prompt_path.relative_to(REPO_ROOT)}')

    if args.check_only:
        print('Check-only mode: Codex was not invoked.')
        return 0

    codex_path = shutil.which('codex')
    if codex_path is None:
        print('ERROR: codex CLI not found in PATH')
        return 1

    cmd = [codex_path, 'exec']
    if args.full_auto:
        cmd.append('--full-auto')
    cmd.append(prompt_text)
    print(f'Running: {" ".join(cmd[:-1])} <prompt>')
    completed = subprocess.run(cmd, cwd=REPO_ROOT)
    return completed.returncode


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Requirement-gated Codex launcher for approved SwR IDs')
    parser.add_argument('--swr', nargs='+', required=True, help='Approved SwR IDs to hand to Codex')
    parser.add_argument('--check-only', action='store_true', help='Run preflight and write prompt without invoking Codex')
    parser.add_argument('--full-auto', action='store_true', help='Pass --full-auto to Codex when executing')
    parser.add_argument('--prompt-out', default='', help='Optional prompt output path')
    main_guard(lambda: run(parser.parse_args()))
