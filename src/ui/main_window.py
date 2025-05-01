# -*- coding: utf-8 -*-
"""
Main window module
"""

import tkinter as tk
from tkinter import messagebox, ttk
import webbrowser
import os  # Add this import

from src.config.app_config import UI_CONFIG, FONT_CONFIG, APP_VERSION
from src.config.translations import TranslationManager
from src.ui.timer_display import TimerDisplay
from src.ui.settings_panel import SettingsPanel
from src.utils.timer_logic import TimerController
from src.utils.history_manager import HistoryManager
from src.utils.sound_manager import SoundManager

class CountdownTimerApp:
    """Countdown Timer application main window class"""
    
    def __init__(self, root):
        """Initialize main window
        
        Args:
            root: tkinter root window
        """
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry(f"{UI_CONFIG['window_width']}x{UI_CONFIG['window_height']}")
        self.root.resizable(False, False)
        self.root.configure(bg=UI_CONFIG['bg_color'])
        
        # Set window icon
        icon_path = os.path.join('resources', 'images', 'timer.ico')
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except tk.TclError:
                print(f"Warning: Could not load icon file at {icon_path}")
        else:
            print(f"Warning: Icon file not found at {icon_path}")

        # Initialize components
        self.translation = TranslationManager()
        self.history_manager = HistoryManager()
        
        # Initialize settings panel
        self.settings_panel = SettingsPanel(
            self.root, 
            self.translation, 
            on_settings_changed=self._apply_settings
        )
        
        # Initialize timer controller and set callbacks
        self.timer = TimerController(
            on_tick=self._on_timer_tick,
            on_complete=self._on_timer_complete,
            on_hourly_reminder=self._on_hourly_reminder
        )
        
        # Create UI elements
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up UI interface"""
        # Configure ttk styles
        self._setup_styles()
        
        # Create menu bar
        self._create_menu_bar()
        
        # Main container
        main_container = tk.Frame(
            self.root, bg=UI_CONFIG['bg_color'], padx=20, pady=10)
        main_container.pack(fill="both", expand=True)
        
        # Time input card
        self._create_time_input_card(main_container)
        
        # History card
        self._create_history_card(main_container)
        
        # Timer display
        self.timer_display = TimerDisplay(main_container)
        
        # Hourly reminder checkbox
        self._create_reminder_checkbox(main_container)
        
        # Control buttons
        self._create_control_buttons(main_container)
        
        # Status display
        self._create_status_display(main_container)
        
        # Version info
        self._create_version_info()
    
    def _setup_styles(self):
        """Configure ttk styles"""
        self.style = ttk.Style()
        self.style.configure("TCombobox",
                            padding=6,
                            relief="flat",
                            background=UI_CONFIG['secondary_color'])

        self.style.configure("TCheckbutton",
                            background=UI_CONFIG['bg_color'],
                            font=FONT_CONFIG['main_font'])

        self.style.map("TCombobox",
                      fieldbackground=[("readonly", "white")],
                      selectbackground=[("readonly", UI_CONFIG['accent_color'])])
    
    def _create_menu_bar(self):
        """Create menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu items
        self.options_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Options", menu=self.options_menu)
        self.options_menu.add_command(label=self.translation.get_text("language"), command=self._toggle_language)
        self.options_menu.add_command(label=self.translation.get_text("settings"), command=self._show_settings)
        self.options_menu.add_separator()
        self.options_menu.add_command(label=self.translation.get_text("about"), command=self._show_about)
        self.options_menu.add_separator()
        self.options_menu.add_command(label=self.translation.get_text("github_info"), command=self._open_github)
    
    def _create_time_input_card(self, parent):
        """Create time input card
        
        Args:
            parent: Parent container
        """
        time_card = tk.Frame(parent,
                           bg="white",
                           relief="flat",
                           padx=15, pady=15,
                           highlightthickness=1,
                           highlightbackground="#E2E8F0")
        time_card.pack(fill="x", pady=5)
        
        # Time input frame
        time_frame = tk.Frame(time_card, bg="white")
        time_frame.pack(fill="x")
        
        # Hours input
        hour_container = tk.Frame(time_frame, bg="white")
        hour_container.pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        
        self.hour_label = tk.Label(hour_container,
                                  text=self.translation.get_text("hours"),
                                  bg="white",
                                  fg=UI_CONFIG['text_color'],
                                  font=FONT_CONFIG['main_font'])
        self.hour_label.pack(anchor="w")
        
        self.hour_var = tk.StringVar(value="0")
        self.hour_entry = tk.Entry(hour_container,
                                  textvariable=self.hour_var,
                                  width=5,
                                  font=("Segoe UI", 12),
                                  justify='center',
                                  relief="flat",
                                  bg="#F8FAFC",
                                  highlightthickness=1,
                                  highlightbackground="#CBD5E1")
        self.hour_entry.pack(fill="x", pady=5)
        
        # Minutes input
        minute_container = tk.Frame(time_frame, bg="white")
        minute_container.pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        
        self.minute_label = tk.Label(minute_container,
                                    text=self.translation.get_text("minutes"),
                                    bg="white",
                                    fg=UI_CONFIG['text_color'],
                                    font=FONT_CONFIG['main_font'])
        self.minute_label.pack(anchor="w")
        
        self.minute_var = tk.StringVar(value="0")
        self.minute_entry = tk.Entry(minute_container,
                                    textvariable=self.minute_var,
                                    width=5,
                                    font=("Segoe UI", 12),
                                    justify='center',
                                    relief="flat",
                                    bg="#F8FAFC",
                                    highlightthickness=1,
                                    highlightbackground="#CBD5E1")
        self.minute_entry.pack(fill="x", pady=5)
        
        # Seconds input
        second_container = tk.Frame(time_frame, bg="white")
        second_container.pack(side=tk.LEFT, expand=True, fill="x", padx=5)
        
        self.second_label = tk.Label(second_container,
                                    text=self.translation.get_text("seconds"),
                                    bg="white",
                                    fg=UI_CONFIG['text_color'],
                                    font=FONT_CONFIG['main_font'])
        self.second_label.pack(anchor="w")
        
        self.second_var = tk.StringVar(value="0")
        self.second_entry = tk.Entry(second_container,
                                    textvariable=self.second_var,
                                    width=5,
                                    font=("Segoe UI", 12),
                                    justify='center',
                                    relief="flat",
                                    bg="#F8FAFC",
                                    highlightthickness=1,
                                    highlightbackground="#CBD5E1")
        self.second_entry.pack(fill="x", pady=5)
    
    def _create_history_card(self, parent):
        """Create history card
        
        Args:
            parent: Parent container
        """
        history_card = tk.Frame(parent,
                              bg="white",
                              relief="flat",
                              padx=15, pady=15,
                              highlightthickness=1,
                              highlightbackground="#E2E8F0")
        history_card.pack(fill="x", pady=10)
        
        # History label
        self.history_label = tk.Label(history_card,
                                     text=self.translation.get_text("history"),
                                     bg="white",
                                     fg=UI_CONFIG['text_color'],
                                     font=FONT_CONFIG['main_font'])
        self.history_label.pack(anchor="w", pady=(0, 8))
        
        # History control frame
        history_control_frame = tk.Frame(history_card, bg="white")
        history_control_frame.pack(fill="x")
        
        # Modern dropdown
        self.history_var = tk.StringVar()
        self.history_combobox = ttk.Combobox(history_control_frame,
                                           textvariable=self.history_var,
                                           font=FONT_CONFIG['main_font'],
                                           style="TCombobox",
                                           state="readonly")
        self.history_combobox.pack(
            side=tk.LEFT, padx=(0, 5), fill="x", expand=True)
        self._update_history_combobox()
        
        # Bind dropdown selection event
        self.history_combobox.bind("<<ComboboxSelected>>", self._select_history)
        
        # History buttons frame
        history_btn_frame = tk.Frame(history_control_frame, bg="white")
        history_btn_frame.pack(side=tk.RIGHT)
        
        # Apply history button
        self.apply_button = tk.Button(history_btn_frame,
                                    text=self.translation.get_text("apply"),
                                    command=self._apply_history,
                                    bg=UI_CONFIG['accent_color'],
                                    fg="white",
                                    padx=10,
                                    font=FONT_CONFIG['main_font'],
                                    relief="flat",
                                    borderwidth=0,
                                    cursor="hand2",
                                    activebackground="#2563EB")
        self.apply_button.pack(side=tk.LEFT, padx=3)
        
        # Delete history button
        self.delete_button = tk.Button(history_btn_frame,
                                     text=self.translation.get_text("delete"),
                                     command=self._delete_history,
                                     bg=UI_CONFIG['danger_color'],
                                     fg="white",
                                     padx=10,
                                     font=FONT_CONFIG['main_font'],
                                     relief="flat",
                                     borderwidth=0,
                                     cursor="hand2",
                                     activebackground="#DC2626")
        self.delete_button.pack(side=tk.LEFT, padx=3)
    
    def _create_reminder_checkbox(self, parent):
        """Create hourly reminder checkbox
        
        Args:
            parent: Parent container
        """
        reminder_frame = tk.Frame(parent, bg=UI_CONFIG['bg_color'])
        reminder_frame.pack(fill="x", pady=5)
        
        self.hourly_reminder_var = tk.BooleanVar(value=True)
        self.reminder_check = ttk.Checkbutton(reminder_frame,
                                           text=self.translation.get_text(
                                               "hourly_reminder"),
                                           variable=self.hourly_reminder_var,
                                           command=self._toggle_hourly_reminder,
                                           style="TCheckbutton")
        self.reminder_check.pack(anchor="center")
    
    def _create_control_buttons(self, parent):
        """Create control buttons
        
        Args:
            parent: Parent container
        """
        button_container = tk.Frame(parent, bg=UI_CONFIG['bg_color'])
        button_container.pack(fill="x", pady=10)
        
        # Control buttons frame - using grid to make buttons equal size
        button_frame = tk.Frame(button_container, bg=UI_CONFIG['bg_color'])
        button_frame.pack()
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        button_frame.grid_columnconfigure(2, weight=1)
        
        # Start button
        self.start_button = tk.Button(button_frame,
                                    text=self.translation.get_text("start"),
                                    command=self._start_timer,
                                    bg=UI_CONFIG['success_color'],
                                    fg="white",
                                    width=10,
                                    height=2,
                                    font=FONT_CONFIG['main_font'],
                                    relief="flat",
                                    borderwidth=0,
                                    cursor="hand2",
                                    activebackground="#059669")
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Pause button
        self.pause_button = tk.Button(button_frame,
                                    text=self.translation.get_text("pause"),
                                    command=self._pause_timer,
                                    bg=UI_CONFIG['warning_color'],
                                    fg="white",
                                    width=10,
                                    height=2,
                                    font=FONT_CONFIG['main_font'],
                                    relief="flat",
                                    borderwidth=0,
                                    cursor="hand2",
                                    activebackground="#D97706",
                                    state=tk.DISABLED)
        self.pause_button.grid(row=0, column=1, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(button_frame,
                                    text=self.translation.get_text("reset"),
                                    command=self._reset_timer,
                                    bg=UI_CONFIG['danger_color'],
                                    fg="white",
                                    width=10,
                                    height=2,
                                    font=FONT_CONFIG['main_font'],
                                    relief="flat",
                                    borderwidth=0,
                                    cursor="hand2",
                                    activebackground="#DC2626")
        self.reset_button.grid(row=0, column=2, padx=5)
    
    def _create_status_display(self, parent):
        """Create status display
        
        Args:
            parent: Parent container
        """
        status_container = tk.Frame(parent, bg=UI_CONFIG['bg_color'])
        status_container.pack(fill="x", pady=10)
        
        status_inner_frame = tk.Frame(
            status_container, bg=UI_CONFIG['accent_color'], padx=2, pady=2)
        status_inner_frame.pack(anchor="center")
        
        self.status_label = tk.Label(status_inner_frame,
                                   text=self.translation.get_text("ready"),
                                   fg="white",
                                   bg=UI_CONFIG['accent_color'],
                                   font=FONT_CONFIG['main_font'],
                                   padx=15,
                                   pady=5)
        self.status_label.pack()
    
    def _create_version_info(self):
        """Create version info - now empty as version info is in About dialog"""
        pass
    
    def _update_history_combobox(self):
        """Update history dropdown box"""
        formatted_history = self.history_manager.get_formatted_history()
        self.history_combobox['values'] = formatted_history
    
    def _select_history(self, event):
        """Handle history selection event"""
        selection = self.history_var.get()
        if selection:
            result = self.history_manager.parse_history_selection(selection)
            if result:
                h, m, s = result
                self.hour_var.set(str(h))
                self.minute_var.set(str(m))
                self.second_var.set(str(s))
    
    def _apply_history(self):
        """Apply selected history to input fields"""
        selection = self.history_var.get()
        if selection:
            result = self.history_manager.parse_history_selection(selection)
            if result:
                h, m, s = result
                self.hour_var.set(str(h))
                self.minute_var.set(str(m))
                self.second_var.set(str(s))
    
    def _delete_history(self):
        """Delete selected history item"""
        selection = self.history_var.get()
        if selection:
            result = self.history_manager.parse_history_selection(selection)
            if result:
                h, m, s = result
                if self.history_manager.delete_history_item(h, m, s):
                    self._update_history_combobox()
                    self.history_var.set("")
                    messagebox.showinfo("Success", self.translation.get_text("delete_success"))
    
    def _toggle_hourly_reminder(self):
        """Toggle hourly reminder setting"""
        enabled = self.hourly_reminder_var.get()
        self.timer.toggle_hourly_reminder(enabled)
    
    def _toggle_language(self):
        """Toggle language"""
        self.translation.toggle_language()
        self._update_ui_text()
    
    def _show_settings(self):
        """Show settings panel"""
        self.settings_panel.show_settings()
    
    def _apply_settings(self, settings):
        """Apply settings
        
        Args:
            settings: Settings dictionary
        """
        # Apply language setting
        if self.translation.current_language != settings['language']:
            self.translation.current_language = settings['language']
            self._update_ui_text()
        
        # Apply hourly reminder setting
        self.hourly_reminder_var.set(settings['hourly_reminder'])
        self._toggle_hourly_reminder()
        
        # Apply history settings
        self.history_manager.max_history = settings['max_history']
        
        # Apply UI theme settings
        if settings['theme'] == 'dark':
            # Switch to dark theme
            UI_CONFIG['bg_color'] = "#1E293B"  # Dark blue-gray
            UI_CONFIG['text_color'] = "#F1F5F9"  # Light gray text
            UI_CONFIG['secondary_color'] = "#334155"  # Dark gray secondary elements
        else:
            # Switch to light theme
            UI_CONFIG['bg_color'] = "#F0F6FF"  # Light blue background
            UI_CONFIG['text_color'] = "#1E293B"  # Dark blue-gray text
            UI_CONFIG['secondary_color'] = "#F1F5F9"  # Light gray secondary elements
        
        # Apply accent color setting
        UI_CONFIG['accent_color'] = settings['accent_color']
        
        # Apply sound settings
        SoundManager.enable_sound = settings['enable_sound']
        SoundManager.sound_type = settings['sound_type']
        SoundManager.volume = settings['volume']
        
        # Refresh UI
        self._refresh_ui()
    
    def _refresh_ui(self):
        """Refresh UI to apply new theme settings"""
        # Update root window
        self.root.configure(bg=UI_CONFIG['bg_color'])
        
        # Update all frames and labels
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=UI_CONFIG['bg_color'])
        
        # Recreate UI
        self.root.after(100, self._update_ui_text)
    
    def _open_github(self):
        """Open GitHub repository page"""
        webbrowser.open("https://github.com/Godblessr/Timer")
    
    def _update_ui_text(self):
        """Update UI text"""
        self.root.title("Countdown Timer / 倒计时提醒软件")
        self.hour_label.config(text=self.translation.get_text("hours"))
        self.minute_label.config(text=self.translation.get_text("minutes"))
        self.second_label.config(text=self.translation.get_text("seconds"))
        self.history_label.config(text=self.translation.get_text("history"))
        self.apply_button.config(text=self.translation.get_text("apply"))
        self.delete_button.config(text=self.translation.get_text("delete"))
        self.reminder_check.config(text=self.translation.get_text("hourly_reminder"))
        self.start_button.config(text=self.translation.get_text("start"))
        
        if self.timer.is_running:
            pause_text = self.translation.get_text("pause")
        else:
            pause_text = self.translation.get_text("resume")
        self.pause_button.config(text=pause_text)
        
        self.reset_button.config(text=self.translation.get_text("reset"))
        
        if self.timer.is_running:
            status_text = self.translation.get_text("running")
        elif self.pause_button.cget("text") == self.translation.get_text("resume"):
            status_text = self.translation.get_text("paused")
        else:
            status_text = self.translation.get_text("ready")
        self.status_label.config(text=status_text)
        
        try:
            self.options_menu.entryconfigure(0, label=self.translation.get_text("language"))
            self.options_menu.entryconfigure(1, label=self.translation.get_text("settings"))
            self.options_menu.entryconfigure(3, label=self.translation.get_text("about"))
            self.options_menu.entryconfigure(5, label=self.translation.get_text("github_info"))
        except Exception as e:
            print(f"Menu update error: {e}")
    
    def _start_timer(self):
        """Start the timer"""
        try:
            hours = int(self.hour_var.get())
            minutes = int(self.minute_var.get())
            seconds = int(self.second_var.get())
            
            # Validate inputs
            if hours < 0 or minutes < 0 or seconds < 0:
                messagebox.showerror("Error", self.translation.get_text("negative_time_error"))
                return
            
            if hours == 0 and minutes == 0 and seconds == 0:
                messagebox.showerror("Error", self.translation.get_text("empty_time_error"))
                return
            
            # Add to history
            self.history_manager.add_history_item(hours, minutes, seconds)
            self._update_history_combobox()
            
            # Start timer
            if self.timer.start(hours, minutes, seconds):
                # Update button states
                self.start_button.config(state=tk.DISABLED)
                self.pause_button.config(state=tk.NORMAL)
                self.hour_entry.config(state=tk.DISABLED)
                self.minute_entry.config(state=tk.DISABLED)
                self.second_entry.config(state=tk.DISABLED)
                
                # Set status
                self.status_label.config(text=self.translation.get_text("running"))
                
        except ValueError:
            messagebox.showerror("Error", self.translation.get_text("invalid_number_error"))
    
    def _pause_timer(self):
        """Pause or resume the timer"""
        if not self.timer.is_running:
            # Resume timer
            if self.timer.resume():
                self.status_label.config(text=self.translation.get_text("running"))
                self.pause_button.config(text=self.translation.get_text("pause"))
        else:
            # Pause timer
            if self.timer.pause():
                self.status_label.config(text=self.translation.get_text("paused"))
                self.pause_button.config(text=self.translation.get_text("resume"))
    
    def _reset_timer(self):
        """Reset the timer"""
        # Stop timer
        self.timer.reset()
        
        # Reset UI
        self.timer_display.update_display(0)
        self.status_label.config(text=self.translation.get_text("ready"))
        
        # Reset button states
        self.start_button.config(state=tk.NORMAL)
        self.pause_button.config(state=tk.DISABLED, text=self.translation.get_text("pause"))
        self.hour_entry.config(state=tk.NORMAL)
        self.minute_entry.config(state=tk.NORMAL)
        self.second_entry.config(state=tk.NORMAL)
    
    def _on_timer_tick(self, remaining_seconds):
        """Timer tick callback function
        
        Args:
            remaining_seconds: Remaining seconds
        """
        self.timer_display.update_display(remaining_seconds)
    
    def _on_timer_complete(self):
        """Timer completion callback function"""
        # Play completion sound
        SoundManager.play_completion_sound()
        
        # Show completion message
        self.root.after(0, lambda: messagebox.showinfo("Completed", self.translation.get_text("completed_msg")))
        
        # Reset timer
        self.root.after(0, self._reset_timer)
    
    def _on_hourly_reminder(self, remaining_hours, remaining_minutes):
        """Hourly reminder callback function
        
        Args:
            remaining_hours: Remaining hours
            remaining_minutes: Remaining minutes
        """
        def show_message():
            # Play reminder sound
            SoundManager.play_reminder_sound()
            messagebox.showinfo(
                "Reminder", 
                self.translation.get_text("hourly_reminder_msg").format(remaining_hours, remaining_minutes)
            )
        
        self.root.after(0, show_message)
    
    def _show_about(self):
        """Show about dialog with version and author information"""
        about_content = self.translation.get_text("about_content").format(APP_VERSION)
        messagebox.showinfo(
            self.translation.get_text("about_title"), 
            about_content
        )