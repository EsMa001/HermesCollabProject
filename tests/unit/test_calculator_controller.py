from src.calculator_demo.controller import CalculatorController


def test_controller_starts_with_zero_display() -> None:
    controller = CalculatorController()

    assert controller.display_text == '0'


def test_controller_calculates_simple_operation_and_reuses_result() -> None:
    controller = CalculatorController()

    controller.input_digit('2')
    controller.set_operator('+')
    controller.input_digit('3')
    controller.evaluate()

    assert controller.display_text == '5'

    controller.set_operator('*')
    controller.input_digit('4')
    controller.evaluate()

    assert controller.display_text == '20'


def test_controller_clear_resets_display_and_state() -> None:
    controller = CalculatorController()

    controller.input_digit('9')
    controller.set_operator('-')
    controller.input_digit('1')
    controller.clear()

    assert controller.display_text == '0'
    assert controller.pending_operator is None


def test_controller_reports_understandable_error_for_division_by_zero() -> None:
    controller = CalculatorController()

    controller.input_digit('8')
    controller.set_operator('/')
    controller.input_digit('0')
    controller.evaluate()

    assert controller.display_text == 'Fehler'
    assert controller.error_text == 'Division durch 0 ist nicht erlaubt.'
