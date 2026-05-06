#!/usr/bin/env python3
from __future__ import annotations

from _vmodel_common import load_requirement_sets, print_errors, main_guard

def validate() -> int:
    data = load_requirement_sets()
    qp = data['quality_plan']['requirement_statuses']
    methods = set(data['quality_plan']['verification_methods'])
    errors: list[str] = []
    all_ids: set[str] = set()
    stakeholder = data['stakeholder']
    system = data['system']
    software = data['software']
    for items, allowed in [
        (stakeholder, set(qp['stakeholder'])),
        (system, set(qp['system_and_software'])),
        (software, set(qp['system_and_software'])),
    ]:
        for item in items:
            iid = item.get('id')
            if not iid:
                errors.append(f'missing id in {item}')
                continue
            if iid in all_ids:
                errors.append(f'duplicate id: {iid}')
            all_ids.add(iid)
            if item.get('status') not in allowed:
                errors.append(f'{iid} has invalid status {item.get("status")}')
            if item.get('version') is None:
                errors.append(f'{iid} missing version')
            if item.get('status') in {'accepted', 'accepted_by_agent', 'accepted_by_user'} and item.get('open_questions'):
                errors.append(f'{iid} is accepted but has open_questions')
            if iid.startswith(('SyR-', 'SwR-')):
                if not item.get('parent_ids'):
                    errors.append(f'{iid} missing parent_ids')
                if item.get('verification_method') not in methods:
                    errors.append(f'{iid} invalid verification method {item.get("verification_method")}')
    stakeholder_ids = {item['id'] for item in stakeholder}
    system_ids = {item['id'] for item in system}
    for item in system:
        for pid in item.get('parent_ids', []):
            if pid not in stakeholder_ids:
                errors.append(f"{item['id']} parent {pid} is not an StR")
    for item in software:
        for pid in item.get('parent_ids', []):
            if pid not in system_ids:
                errors.append(f"{item['id']} parent {pid} is not a SyR")
    return print_errors(errors, 'Requirements validation passed.')

if __name__ == '__main__':
    main_guard(validate)
