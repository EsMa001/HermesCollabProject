from decimal import Decimal

import pytest

from src.calculator_demo.core import CalculationError, calculate_binary_operation, format_display_value, parse_decimal


def test_calculate_binary_operation_supports_four_basic_operations() -> None:
    assert calculate_binary_operation(Decimal('2'), '+', Decimal('3')) == Decimal('5')
    assert calculate_binary_operation(Decimal('7'), '-', Decimal('2')) == Decimal('5')
    assert calculate_binary_operation(Decimal('4'), '*', Decimal('2.5')) == Decimal('10')
    assert calculate_binary_operation(Decimal('9'), '/', Decimal('3')) == Decimal('3')


def test_parse_decimal_accepts_integer_and_decimal_input() -> None:
    assert parse_decimal('42') == Decimal('42')
    assert parse_decimal('3.5') == Decimal('3.5')


def test_calculate_binary_operation_rejects_division_by_zero() -> None:
    with pytest.raises(CalculationError, match='Division durch 0 ist nicht erlaubt.'):
        calculate_binary_operation(Decimal('1'), '/', Decimal('0'))


def test_format_display_value_removes_unnecessary_trailing_decimals() -> None:
    assert format_display_value(Decimal('5.0')) == '5'
    assert format_display_value(Decimal('5.250')) == '5.25'
