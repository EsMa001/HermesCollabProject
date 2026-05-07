"""
Implements:
- SwR-010
- SwR-015
- SwR-016
- SwR-023

Design:
- DDS-010
- DDS-015
- DDS-016
- DDS-023
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation


class CalculationError(ValueError):
    """Domain error raised for invalid calculator operations."""


def parse_decimal(text: str) -> Decimal:
    normalized = text.strip()
    try:
        return Decimal(normalized)
    except InvalidOperation as exc:
        raise CalculationError('Ungültige Zahleneingabe.') from exc


def calculate_binary_operation(left: Decimal, operator: str, right: Decimal) -> Decimal:
    if operator == '+':
        return left + right
    if operator == '-':
        return left - right
    if operator == '*':
        return left * right
    if operator == '/':
        if right == 0:
            raise CalculationError('Division durch 0 ist nicht erlaubt.')
        return left / right
    raise CalculationError('Operation wird nicht unterstützt.')


def format_display_value(value: Decimal) -> str:
    normalized = value.normalize()
    if normalized == normalized.to_integral():
        return str(normalized.quantize(Decimal('1')))
    text = format(normalized, 'f')
    return text.rstrip('0').rstrip('.')
