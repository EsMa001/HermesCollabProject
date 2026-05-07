#!/usr/bin/env python3
from __future__ import annotations

from collections import defaultdict

from _vmodel_common import REPO_ROOT, load_requirement_sets, trace_links, write_text, main_guard


def generate() -> int:
    data = load_requirement_sets()
    stakeholder = {item['id']: item for item in data['stakeholder']}
    system = {item['id']: item for item in data['system']}
    software = {item['id']: item for item in data['software']}
    syr_by_str = defaultdict(list)
    swr_by_syr = defaultdict(list)
    dds_by_swr = defaultdict(list)
    code_by_swr = defaultdict(list)
    tests_by_req = defaultdict(list)
    for link in trace_links():
        src, dst, typ = link['from'], link['to'], link['type']
        if typ == 'derives' and src in system and dst in stakeholder:
            syr_by_str[dst].append(src)
        elif typ == 'derives' and src in software and dst in system:
            swr_by_syr[dst].append(src)
        elif typ == 'implements' and str(src).startswith('DDS-') and dst in software:
            dds_by_swr[dst].append(src)
        elif typ == 'implements' and str(src).endswith('.py') and dst in software:
            code_by_swr[dst].append(src)
        elif typ in {'verifies', 'validates'}:
            tests_by_req[dst].append(src)
    lines = [
        '# Traceability Matrix',
        '',
        '| StR | SyR | SwR | DDS | Code | Test | Status |',
        '| --- | --- | --- | --- | ---- | ---- | ------ |',
    ]
    for str_id in stakeholder:
        for syr_id in syr_by_str.get(str_id, ['-']):
            for swr_id in swr_by_syr.get(syr_id, ['-']):
                dds = ', '.join(dds_by_swr.get(swr_id, ['-'])) if swr_id != '-' else '-'
                code = ', '.join(code_by_swr.get(swr_id, ['-'])) if swr_id != '-' else '-'
                tests = ', '.join(sorted(set(tests_by_req.get(str_id, []) + tests_by_req.get(syr_id, []) + tests_by_req.get(swr_id, [])))) or '-'
                status = software[swr_id]['status'] if swr_id != '-' else system[syr_id]['status']
                lines.append(f'| {str_id} | {syr_id} | {swr_id} | {dds} | {code} | {tests} | {status} |')
    write_text(REPO_ROOT / 'vmodel/traceability/generated_trace_matrix.md', '\n'.join(lines) + '\n')
    print('Traceability matrix generated.')
    return 0


if __name__ == '__main__':
    main_guard(generate)
