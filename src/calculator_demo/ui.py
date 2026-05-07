"""
Implements:
- SwR-011
- SwR-014
- SwR-021
- SwR-024

Design:
- DDS-011
- DDS-014
- DDS-021
- DDS-024
"""
from __future__ import annotations

import tkinter as tk
from tkinter import ttk

from .controller import CalculatorController
from .strings import DISPLAY_LABELS


def build_button_rows() -> list[list[str]]:
    return [
        ['7', '8', '9', '/'],
        ['4', '5', '6', '*'],
        ['1', '2', '3', '-'],
        ['C', '0', '=', '+'],
    ]


class CalculatorApp(ttk.Frame):
    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, padding=8)
        self.controller = CalculatorController()
        self.display_var = tk.StringVar(master=master, value=DISPLAY_LABELS['initial_display'])
        self.error_var = tk.StringVar(master=master, value='')
        self._create_widgets()

    def _create_widgets(self) -> None:
        display = ttk.Entry(self, textvariable=self.display_var, justify='right', state='readonly')
        display.grid(row=0, column=0, columnspan=4, sticky='ew', pady=(0, 4))
        error_label = ttk.Label(self, textvariable=self.error_var)
        error_label.grid(row=1, column=0, columnspan=4, sticky='w', pady=(0, 4))
        for row_index, row in enumerate(build_button_rows(), start=2):
            for column_index, label in enumerate(row):
                ttk.Button(self, text=label, command=lambda current=label: self.handle_input(current)).grid(
                    row=row_index,
                    column=column_index,
                    sticky='nsew',
                    padx=2,
                    pady=2,
                )
        for column_index in range(4):
            self.columnconfigure(column_index, weight=1)

    def handle_input(self, label: str) -> None:
        if label.isdigit():
            self.controller.input_digit(label)
        elif label in {'+', '-', '*', '/'}:
            self.controller.set_operator(label)
        elif label == DISPLAY_LABELS['clear']:
            self.controller.clear()
        elif label == DISPLAY_LABELS['equals']:
            self.controller.evaluate()
        self.display_var.set(self.controller.display_text)
        self.error_var.set(self.controller.error_text or '')
