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
        '- Current repository requirement, traceability and verification artifacts',
        '- Initial worked example `CR-StR-001-002`',
    ]
    if any('calculator' in ' '.join([
        str(item.get('title', '')),
        str(item.get('statement', '')),
        str(item.get('rationale', '')),
    ]).lower() for item in data['stakeholder']):
        lines.append('- Calculator requirement derivation slice on the active branch')
    lines.extend([
        '',
        '## Affected Requirements',
        '',
    ])
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
        'The active branch artifacts are ready for review at their current derivation depth. Any requirement items still listed under Traceability Waivers need downstream lifecycle artifacts in a subsequent step before final implementation acceptance.',
        '',
    ])
    write_text(REPO_ROOT / 'vmodel/verification/verification_report.md', '\n'.join(lines))
    print('Verification report generated.')
    return 0


if __name__ == '__main__':
    main_guard(generate)
