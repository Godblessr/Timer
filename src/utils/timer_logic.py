# -*- coding: utf-8 -*-
"""
Timer core logic
"""

import threading
import time
from datetime import datetime, timedelta

class TimerController:
    """Timer controller class"""
    
    def __init__(self, on_tick=None, on_complete=None, on_hourly_reminder=None):
        """Initialize timer controller
        
        Args:
            on_tick: Callback function called every second with remaining time in seconds
            on_complete: Callback function called when timer completes
            on_hourly_reminder: Callback function for hourly reminders with remaining hours and minutes
        """
        self.on_tick = on_tick
        self.on_complete = on_complete
        self.on_hourly_reminder = on_hourly_reminder
        
        self.is_running = False
        self.thread = None
        self.remaining_time = 0
        self.target_time = None
        self.hourly_reminders = True
        
    def start(self, hours, minutes, seconds):
        """Start the timer
        
        Args:
            hours: Number of hours
            minutes: Number of minutes
            seconds: Number of seconds
            
        Returns:
            bool: Whether the timer was successfully started
        """
        if self.is_running:
            return False
        
        # Calculate total seconds
        total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
        
        # Set target time
        self.target_time = datetime.now() + timedelta(seconds=total_seconds)
        self.remaining_time = total_seconds
        
        # Set status
        self.is_running = True
        
        # Start thread
        self.thread = threading.Thread(target=self._run_timer)
        self.thread.daemon = True
        self.thread.start()
        
        return True
    
    def pause(self):
        """Pause the timer
        
        Returns:
            bool: Whether the timer was successfully paused
        """
        if not self.is_running:
            return False
        self.is_running = False
        return True
    
    def resume(self):
        """Resume the timer
        
        Returns:
            bool: Whether the timer was successfully resumed
        """
        if self.is_running:
            return False
        
        # Set new target time
        self.target_time = datetime.now() + timedelta(seconds=self.remaining_time)
        
        # Set status
        self.is_running = True
        
        # Start new thread
        self.thread = threading.Thread(target=self._run_timer)
        self.thread.daemon = True
        self.thread.start()
        
        return True
    
    def reset(self):
        """Reset the timer"""
        self.is_running = False
        self.remaining_time = 0
    
    def toggle_hourly_reminder(self, enabled):
        """Toggle hourly reminder setting
        
        Args:
            enabled: Whether to enable hourly reminders
        """
        self.hourly_reminders = enabled
    
    def _run_timer(self):
        """Timer thread function"""
        last_hour_reminder = datetime.now()
        
        while self.is_running and self.remaining_time > 0:
            # Calculate remaining time
            current_time = datetime.now()
            self.remaining_time = int((self.target_time - current_time).total_seconds())
            
            if self.remaining_time <= 0:
                self.remaining_time = 0
                self.is_running = False
            
            # Update display
            if self.on_tick:
                self.on_tick(self.remaining_time)
            
            # Check if hourly reminder is needed
            if self.hourly_reminders and self.is_running:
                time_since_last_reminder = (current_time - last_hour_reminder).total_seconds()
                if time_since_last_reminder >= 3600:  # 3600 seconds = 1 hour
                    if self.on_hourly_reminder:
                        remaining_hours = self.remaining_time // 3600
                        remaining_minutes = (self.remaining_time % 3600) // 60
                        self.on_hourly_reminder(remaining_hours, remaining_minutes)
                    last_hour_reminder = current_time
            
            # Sleep for one second
            time.sleep(1)
        
        # Countdown complete
        if self.remaining_time <= 0 and self.on_complete:
            self.on_complete()
    
    def get_time_parts(self):
        """Get time components
        
        Returns:
            tuple: Tuple of (hours, minutes, seconds)
        """
        hours, remainder = divmod(self.remaining_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        return hours, minutes, seconds