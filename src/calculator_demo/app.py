"""
Implements:
- SwR-014

Design:
- DDS-014
"""
from __future__ import annotations

import tkinter as tk

from .strings import DISPLAY_LABELS
from .ui import CalculatorApp


def create_root() -> tk.Tk:
    root = tk.Tk()
    root.title(DISPLAY_LABELS['title'])
    app = CalculatorApp(root)
    app.grid(sticky='nsew')
    return root


def main() -> None:
    root = create_root()
    root.mainloop()


if __name__ == '__main__':
    main()
