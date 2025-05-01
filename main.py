#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Countdown Timer Application
Main entry point
"""

import tkinter as tk
from src.ui.main_window import CountdownTimerApp


def main():
    """Main function to launch the application"""
    root = tk.Tk()
    app = CountdownTimerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
