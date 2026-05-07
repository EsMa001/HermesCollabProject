from src.calculator_demo.ui import DISPLAY_LABELS, build_button_rows


def test_build_button_rows_exposes_digit_operator_and_control_labels() -> None:
    rows = build_button_rows()
    flat = [label for row in rows for label in row]

    for expected in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '-', '*', '/', '=', 'C']:
        assert expected in flat

    assert rows[-1][-2] == '+'
    assert rows[-1][-1] == '='


def test_display_labels_are_german_and_start_with_zero() -> None:
    assert DISPLAY_LABELS['title'] == 'Taschenrechner'
    assert DISPLAY_LABELS['initial_display'] == '0'
