#!/usr/bin/env python3
from __future__ import annotations

import argparse

from generate_trace_matrix import generate as generate_trace_matrix
from generate_verification_report import generate as generate_verification_report
from validate_code_links import validate as validate_code_links
from validate_requirements import validate as validate_requirements
from validate_traceability import validate as validate_traceability


def review_and_verify() -> int:
    for fn in [validate_requirements, validate_traceability, validate_code_links, generate_trace_matrix, generate_verification_report]:
        rc = fn()
        if rc != 0:
            return rc
    print('Review and verify workflow completed successfully.')
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('workflow', choices=['review_and_verify'])
    args = parser.parse_args()
    if args.workflow == 'review_and_verify':
        return review_and_verify()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
