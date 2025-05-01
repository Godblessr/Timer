# -*- coding: utf-8 -*-
"""
Application configuration module
"""

import os

# Application version
APP_VERSION = "1.0.0"

# UI configuration
UI_CONFIG = {
    "bg_color": "#F0F6FF",          # Light blue background
    "accent_color": "#3B82F6",      # Blue accent color
    "text_color": "#1E293B",        # Dark blue-gray text
    "secondary_color": "#F1F5F9",   # Light gray for secondary elements
    "success_color": "#10B981",     # Green (success)
    "warning_color": "#F59E0B",     # Orange (warning)
    "danger_color": "#EF4444",      # Red (danger)
    "window_width": 450,
    "window_height": 500,
}

# Font configuration
FONT_CONFIG = {
    "title_font": ("Segoe UI", 18, "bold"),
    "display_font": ("Segoe UI", 36, "bold"),
    "main_font": ("Segoe UI", 10),
}

# Files and paths configuration
class PathConfig:
    """Path configuration class"""
    
    @staticmethod
    def get_base_path():
        """Get application base path"""
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    @staticmethod
    def get_history_file_path():
        """Get history file path"""
        return os.path.join(PathConfig.get_base_path(), "timer_history.json")
    
    @staticmethod
    def get_resources_path():
        """Get resources folder path"""
        return os.path.join(PathConfig.get_base_path(), "resources")