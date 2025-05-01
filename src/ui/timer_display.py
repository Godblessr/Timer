# -*- coding: utf-8 -*-
"""
Timer display module
"""

import tkinter as tk
from src.config.app_config import UI_CONFIG, FONT_CONFIG

class TimerDisplay:
    """Timer display class"""
    
    def __init__(self, parent):
        """Initialize timer display component
        
        Args:
            parent: Parent container
        """
        display_container = tk.Frame(parent, bg=UI_CONFIG['bg_color'], pady=10)
        display_container.pack(fill="x")
        
        # Timer display
        self.time_label = tk.Label(display_container,
                                  text="00:00:00",
                                  font=FONT_CONFIG['display_font'],
                                  bg=UI_CONFIG['bg_color'],
                                  fg=UI_CONFIG['accent_color'],
                                  width=8)
        self.time_label.pack(pady=5)
    
    def update_display(self, remaining_seconds):
        """Update display
        
        Args:
            remaining_seconds: Remaining seconds
        """
        # Calculate hours, minutes, seconds
        hours, remainder = divmod(remaining_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        # Update display
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        # Change color based on remaining time
        if remaining_seconds <= 60:  # Less than 1 minute
            display_color = UI_CONFIG['danger_color']  # Red
        elif remaining_seconds <= 300:  # Less than 5 minutes
            display_color = UI_CONFIG['warning_color']  # Orange/Yellow
        else:
            display_color = UI_CONFIG['accent_color']
            
        self.time_label.config(text=time_str, fg=display_color)