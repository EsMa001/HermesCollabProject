# Impact Analysis CR-StR-001-002

## Changed Stakeholder Requirement

- `StR-001`: Reproducible analysis run

## Change Summary

The user requested explicit persistence of run metadata:
- software version
- configuration version
- input data references

## Affected System Requirements

- `SyR-001`: Versioned run configuration loading
- `SyR-004`: Run metadata persistence

## Affected Software Requirements

- `SwR-001`: Load run configuration from explicit file path
- `SwR-007`: Persist run metadata
- `SwR-008`: Present run metadata in report output

## Assessment

- Implementation change required: **yes**
- Test update required: **yes**
- Architecture update required: **minor**
- Breaking change: **no**
- User approval required before implementation: **yes**

## Recommendation

Accept the change and update downstream requirements and tests before opening an implementation branch.

---

# Impact Analysis CR-StR-012-002

## Changed Stakeholder Requirement

- `StR-012`: Graphical user interface

## Change Summary

The user requested a GUI layout constraint for the calculator:
- the equals control shall be placed in the bottom-right corner
- this shall be made explicit already at stakeholder-requirement level
- the accepted interpretation is limited to the initial standard view
- the concrete UI change is the swap of `'+'` and `'='` within the existing 4x4 keypad layout

## Affected System Requirements

- `SyR-011`: Provide classical calculator GUI
- `SyR-018`: Provide clear and equals controls

## Affected Software Requirements

- `SwR-011`: Compose Tkinter calculator UI elements
- `SwR-018`: Implement Clear and equals actions

## Affected Architecture / Tests / Code

- `DDS-011`: Tkinter calculator widget composition
- `DDS-018`: Dedicated Clear and equals actions
- `TC-SyR-011-001`, `TC-SyR-018-001`
- `TC-SwR-011-001`, `TC-SwR-018-001`
- `src/calculator_demo/ui.py`
- `tests/unit/test_calculator_ui_spec.py`

## Assessment

- Implementation change required: **yes**
- Test update required: **yes**
- Architecture update required: **minor**
- Breaking change: **no functional change expected**
- User approval required before implementation: **completed**

## Resolved Clarifications

- Only the initial visual position is constrained.
- The intended implementation is the simple swap of `'+'` and `'='` within the existing 4x4 keypad layout.
- The layout constraint is mandatory for the first scope.

## Recommendation

Accept the change, update the affected downstream artifacts, implement the keypad layout adjustment, and verify it through requirements validation, traceability validation, code-link validation and focused GUI tests.
