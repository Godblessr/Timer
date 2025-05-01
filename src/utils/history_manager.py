# -*- coding: utf-8 -*-
"""
History management module
"""

import json
import os
from src.config.app_config import PathConfig

class HistoryManager:
    """History manager class"""
    
    def __init__(self, max_history=10):
        """Initialize history manager
        
        Args:
            max_history: Maximum number of history records
        """
        self.max_history = max_history
        self.history_file = PathConfig.get_history_file_path()
        self.history_items = self.load_history()
    
    def load_history(self):
        """Load history from JSON file
        
        Returns:
            list: History record list
        """
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Failed to load history: {e}")
                return []
        return []
    
    def save_history(self):
        """Save history to JSON file
        
        Returns:
            bool: Whether saving was successful
        """
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history_items, f, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Failed to save history: {e}")
            return False
    
    def add_history_item(self, hours, minutes, seconds):
        """Add history item
        
        Args:
            hours: Number of hours
            minutes: Number of minutes
            seconds: Number of seconds
            
        Returns:
            bool: Whether the addition was successful
        """
        # Check if record already exists
        for item in self.history_items:
            if (item.get("hours") == hours and 
                item.get("minutes") == minutes and 
                item.get("seconds") == seconds):
                return False  # Already exists, skip
        
        # Add new record
        self.history_items.append({
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds
        })
        
        # Limit history count
        if len(self.history_items) > self.max_history:
            self.history_items.pop(0)
        
        # Save records
        return self.save_history()
    
    def delete_history_item(self, hours, minutes, seconds):
        """Delete history item
        
        Args:
            hours: Number of hours
            minutes: Number of minutes
            seconds: Number of seconds
            
        Returns:
            bool: Whether deletion was successful
        """
        initial_count = len(self.history_items)
        
        # Find and delete matching records
        self.history_items = [item for item in self.history_items 
                             if not (item.get("hours") == hours and 
                                   item.get("minutes") == minutes and 
                                   item.get("seconds") == seconds)]
        
        # Check if any record was deleted
        if len(self.history_items) < initial_count:
            return self.save_history()
        
        return False
    
    def get_formatted_history(self):
        """Get formatted history list
        
        Returns:
            list: List of formatted history strings
        """
        formatted_items = []
        for item in self.history_items:
            h = item.get("hours", 0)
            m = item.get("minutes", 0)
            s = item.get("seconds", 0)
            formatted_items.append(f"{h:02d}:{m:02d}:{s:02d}")
        return formatted_items
    
    def parse_history_selection(self, selection):
        """Parse history selection
        
        Args:
            selection: String in format "00:00:00"
            
        Returns:
            tuple: Tuple of (hours, minutes, seconds), or None if parsing fails
        """
        try:
            h, m, s = map(int, selection.split(':'))
            return h, m, s
        except Exception as e:
            print(f"Failed to parse history: {e}")
            return None