#!/usr/bin/env python3
from __future__ import annotations

from _vmodel_common import REPO_ROOT, load_requirement_sets, trace_waivers, write_text, main_guard


def generate() -> int:
    data = load_requirement_sets()
    waivers = trace_waivers()
    lines = [
        '# Verification Report',
        '',
        '## Scope',
        '',
        '- Initial V-Model-light scaffold',
        '- Example change workflow `CR-StR-001-002`',
        '- Implemented minimal workflow slice for configuration loading and reproducibility metadata',
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
    if waivers:
        for waiver in waivers:
            lines.append(f"- `{waiver['requirement_id']}` — {waiver['rationale']}")
    else:
        lines.append('- None.')
    lines.extend([
        '',
        '## Acceptance Recommendation',
        '',
        'The current minimal workflow slice is ready for review with trace-linked implementation artifacts. Before acceptance of further changes, re-run the local validators and tests on the working tree. The next recommended increment is an end-to-end run entry point that exercises configuration loading, metadata persistence and report generation together.',
        '',
    ])
    write_text(REPO_ROOT / 'vmodel/verification/verification_report.md', '\n'.join(lines))
    print('Verification report generated.')
    return 0


if __name__ == '__main__':
    main_guard(generate)
