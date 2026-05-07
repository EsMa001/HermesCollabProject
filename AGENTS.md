# AGENTS.md

## Process Model

This repository follows a tailored V-Model-light and requirements-as-code workflow.

Production code may only be created or modified if the change is traceable to at least one accepted Software Requirement ID.

## Requirement IDs

- Stakeholder Requirement: `StR-*`
- Stakeholder Change Request: `CR-StR-*`
- System Requirement: `SyR-*`
- Software Requirement: `SwR-*`
- Design Specification: `DDS-*`
- Verification Specification: `VSpec-*`
- Test Case: `TC-*`
- Acceptance Test Case: `ATC-*`
- Test Protocol: `TProt-*`
- Baseline: `BSL-*`

## Mandatory Rules

1. Do not implement functionality without an accepted `SwR-*`.
2. Do not create speculative behavior.
3. Do not modify `src/` without updating traceability.
4. Do not create tests without linking them to at least one requirement.
5. If a requirement is ambiguous, stop and create a clarification request.
6. Prefer small vertical slices.
7. Write or update tests before or together with implementation.
8. Run all validation commands before finishing.
9. Do not push directly to `main`.
10. Do not use secrets, credentials, production systems, or network access unless explicitly authorized.
11. Accepted stakeholder requirement changes must first create a CR and impact analysis before downstream implementation.
12. No accepted SwR -> no production code change.

## Required Checks

- `python3 tools/validate_requirements.py`
- `python3 tools/validate_traceability.py`
- `python3 tools/validate_code_links.py`
- `python3 tools/generate_trace_matrix.py`
- `python3 tools/generate_verification_report.py`
- `python3 tools/run_codex_for_swr.py --swr <SwR-ID> --check-only`
- `pytest`

## Codex-Specific Rule

Codex may only be invoked through the repository preflight gate:

- `python3 tools/run_codex_for_swr.py --swr <SwR-ID> [--check-only|--full-auto]`

The gate must reject execution when:
- branch is `main`
- `SwR-*` is not accepted
- parent `SyR-*` / `StR-*` chain is not accepted
- linked `TC-*` does not exist
- open questions or assumptions remain
