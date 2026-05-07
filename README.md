# HermesCollabProject

Requirements-driven repository scaffold using a tailored **V-Model-light** workflow.

## Goal

This repository is prepared so that stakeholder changes flow through:

`StR -> CR -> Impact Analysis -> SyR -> SwR -> Design -> Test Spec -> Code -> Verification -> Acceptance`

## Repository Structure

```text
.
├── AGENTS.md
├── README.md
├── pyproject.toml
├── src/
├── tests/
├── tools/
├── prompts/
└── vmodel/
```

## Primary User Workflow

1. Edit or add stakeholder requirements in `vmodel/requirements/stakeholder_requirements.yaml`.
2. Create or update a `CR-StR-*` entry in `vmodel/change/stakeholder_change_requests.yaml`.
3. Review `vmodel/traceability/impact_analysis.md`.
4. Approve the stakeholder change.
5. Derive `SyR-*`, `SwR-*`, tests, and trace links.
6. Only then implement on a non-main branch.
7. Run verification and acceptance.

## Validation Commands

```bash
python3 tools/validate_requirements.py
python3 tools/validate_traceability.py
python3 tools/validate_code_links.py
python3 tools/generate_trace_matrix.py
python3 tools/generate_verification_report.py
python3 -m pytest tests -q
```

## Codex Integration

Yes, using Codex for implementation from approved requirements makes sense **if Codex is constrained by the requirements chain**.

Recommended flow in this repo:

1. approve stakeholder change
2. derive `SyR-*` and `SwR-*`
3. add linked `TC-*`
4. work on a non-main branch
5. run Codex only for explicit `SwR-*` scope

Preflight and prompt generation:

```bash
python3 tools/run_codex_for_swr.py --swr SwR-001 --check-only
```

If Codex CLI is installed and configured:

```bash
python3 tools/run_codex_for_swr.py --swr SwR-001 --full-auto
```

This tool checks branch, requirement status, traceability and linked tests before allowing Codex execution.

## Example Change Flow Included

The repository contains an initial worked example for:

- `StR-001` Reproducible analysis run
- `CR-StR-001-002`
- derived `SyR-*` and `SwR-*`
- test specifications
- traceability matrix
- verification report

## Calculator Example Branch Note

On branch `hermes/calculator-example`, the calculator-specific stakeholder
requirement set from the earlier chat is stored separately in:

- `vmodel/requirements/calculator_stakeholder_requirements.yaml`

This keeps the original worked example intact while the calculator-specific
requirement chain is derived in the next steps.
