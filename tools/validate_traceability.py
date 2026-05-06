#!/usr/bin/env python3
from __future__ import annotations

from _vmodel_common import load_requirement_sets, trace_links, trace_waivers, print_errors, main_guard

def validate() -> int:
    data = load_requirement_sets()
    stakeholder = {item['id']: item for item in data['stakeholder']}
    system = {item['id']: item for item in data['system']}
    software = {item['id']: item for item in data['software']}
    tests = {item['id']: item for item in data['tests']}
    changes = {item['id']: item for item in data['changes']}
    design = {item['id']: item for item in data['design']['decisions']}
    waivers = {item['requirement_id'] for item in trace_waivers() if 'requirement_id' in item}
    known = set(stakeholder) | set(system) | set(software) | set(tests) | set(changes) | set(design)
    errors: list[str] = []
    for link in trace_links():
        src = link.get('from')
        dst = link.get('to')
        if not src or not dst or not link.get('type'):
            errors.append(f'incomplete trace link: {link}')
            continue
        if src not in known and not str(src).endswith('.py'):
            errors.append(f'unknown trace source: {src}')
        if dst not in known and not str(dst).endswith('.py'):
            errors.append(f'unknown trace target: {dst}')
    links = trace_links()
    def has_link(link_type: str, *, src: str | None = None, dst: str | None = None) -> bool:
        for link in links:
            if link['type'] != link_type:
                continue
            if src is not None and link['from'] != src:
                continue
            if dst is not None and link['to'] != dst:
                continue
            return True
        return False
    for iid, item in stakeholder.items():
        if item['status'] == 'accepted' and iid not in waivers and not has_link('derives', dst=iid):
            errors.append(f'{iid} has no downstream SyR link')
    for iid, item in system.items():
        if item['status'] in {'accepted_by_agent', 'accepted_by_user'} and iid not in waivers:
            if not has_link('derives', dst=iid):
                errors.append(f'{iid} has no downstream SwR link')
            if not has_link('verifies', dst=iid):
                errors.append(f'{iid} has no verifying test')
    for iid, item in software.items():
        if item['status'] in {'accepted_by_agent', 'accepted_by_user'} and iid not in waivers:
            if not has_link('verifies', dst=iid):
                errors.append(f'{iid} has no verifying test')
    return print_errors(errors, 'Traceability validation passed.')

if __name__ == '__main__':
    main_guard(validate)
