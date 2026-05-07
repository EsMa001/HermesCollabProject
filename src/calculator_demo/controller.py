"""
Implements:
- SwR-012
- SwR-017
- SwR-018
- SwR-019
- SwR-025

Design:
- DDS-012
- DDS-017
- DDS-018
- DDS-019
- DDS-025
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .core import CalculationError, calculate_binary_operation, format_display_value, parse_decimal


@dataclass
class CalculatorController:
    display_text: str = '0'
    error_text: str | None = None
    pending_operator: str | None = None
    _stored_value: Decimal | None = None
    _clear_on_next_digit: bool = False

    def input_digit(self, value: str) -> None:
        if self._clear_on_next_digit or self.display_text == 'Fehler':
            self.display_text = '0'
            self._clear_on_next_digit = False
            self.error_text = None
        if self.display_text == '0':
            self.display_text = value
        else:
            self.display_text += value

    def set_operator(self, operator: str) -> None:
        if self.display_text == 'Fehler':
            return
        self._stored_value = parse_decimal(self.display_text)
        self.pending_operator = operator
        self._clear_on_next_digit = True

    def evaluate(self) -> None:
        if self.pending_operator is None or self._stored_value is None:
            return
        try:
            right = parse_decimal(self.display_text)
            result = calculate_binary_operation(self._stored_value, self.pending_operator, right)
        except CalculationError as exc:
            self.display_text = 'Fehler'
            self.error_text = str(exc)
            self.pending_operator = None
            self._stored_value = None
            self._clear_on_next_digit = True
            return
        self.display_text = format_display_value(result)
        self.error_text = None
        self._stored_value = result
        self.pending_operator = None
        self._clear_on_next_digit = True

    def clear(self) -> None:
        self.display_text = '0'
        self.error_text = None
        self.pending_operator = None
        self._stored_value = None
        self._clear_on_next_digit = False
