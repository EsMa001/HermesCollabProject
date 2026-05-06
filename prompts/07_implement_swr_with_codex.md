Implement exactly the explicitly approved `SwR-*` scope.

Constraints:
- Parent trace must exist: `SwR-* -> SyR-* -> StR-*`
- implement only listed `SwR-*`
- add/update only linked `TC-*`
- no speculative features
- no unrelated refactoring
- no work on `main`

Required checks:
- `python3 tools/validate_requirements.py`
- `python3 tools/validate_traceability.py`
- `python3 tools/validate_code_links.py`
- `python3 tools/generate_trace_matrix.py`
- `python3 tools/generate_verification_report.py`
- `pytest`
