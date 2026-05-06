#!/usr/bin/env python3
from __future__ import annotations

from _vmodel_common import REPO_ROOT, load_requirement_sets, trace_waivers, write_text, main_guard


def generate() -> int:
    data = load_requirement_sets()
    lines = [
        '# Verification Report',
        '',
        '## Scope',
        '',
        '- Initial V-Model-light scaffold',
        '- Example change workflow `CR-StR-001-002`',
        '',
        '## Affected Requirements',
        '',
    ]
    for group in ('stakeholder', 'system', 'software'):
        for item in data[group]:
            lines.append(f"- `{item['id']}` — {item['title']} ({item['status']})")
    lines.extend(['', '## Specified Tests', ''])
    for test in data['tests']:
        targets = test.get('verifies') or test.get('validates') or []
        lines.append(f"- `{test['id']}` -> {', '.join(targets)} [{test.get('level', 'n/a')}]")
    lines.extend(['', '## Traceability Waivers', ''])
    for waiver in trace_waivers():
        lines.append(f"- `{waiver['requirement_id']}` — {waiver['rationale']}")
    lines.extend(['', '## Acceptance Recommendation', '', 'Process setup artifacts are ready for review. Do not start implementation before a concrete SwR slice is approved on a non-main branch.', ''])
    write_text(REPO_ROOT / 'vmodel/verification/verification_report.md', '\n'.join(lines))
    print('Verification report generated.')
    return 0


if __name__ == '__main__':
    main_guard(generate)
