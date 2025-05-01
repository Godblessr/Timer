# -*- coding: utf-8 -*-
"""
设置面板模块，提供应用程序设置界面
"""

import tkinter as tk
from tkinter import ttk, colorchooser, messagebox

from src.config.app_config import UI_CONFIG, FONT_CONFIG
from src.config.translations import TranslationManager

class SettingsPanel:
    """设置面板类，管理应用程序设置"""
    
    def __init__(self, parent, translation_manager, settings=None, on_settings_changed=None):
        """初始化设置面板
        
        Args:
            parent: 父窗口
            translation_manager: 翻译管理器实例
            settings: 当前设置，字典形式
            on_settings_changed: 设置变更回调函数
        """
        self.parent = parent
        self.translation = translation_manager
        self.on_settings_changed = on_settings_changed
        self.settings_window = None
        self.current_settings = settings or {}

    def show_settings(self):
        """显示设置面板"""
        if self.settings_window is not None and self.settings_window.winfo_exists():
            self.settings_window.focus_force()
            return
            
        # 创建设置窗口
        self.settings_window = tk.Toplevel(self.parent)
        self.settings_window.title(self.translation.get_text("settings"))
        self.settings_window.geometry("400x380")  # 稍微增加高度，避免内容挤压
        self.settings_window.resizable(False, False)
        self.settings_window.configure(bg=UI_CONFIG['bg_color'])
        self.settings_window.transient(self.parent)
        self.settings_window.grab_set()
        
        # 设置窗口关闭协议
        self.settings_window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # 设置打开位置为父窗口的中央
        x = self.parent.winfo_x() + (self.parent.winfo_width() - 400) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - 380) // 2
        self.settings_window.geometry(f"+{x}+{y}")
        
        # 创建设置面板内容
        self._create_settings_content()
        
        # 初始化设置值
        self._load_current_settings()

    def _on_window_close(self):
        """窗口关闭处理"""
        if messagebox.askyesno(
            self.translation.get_text("settings"),
            "关闭而不保存更改？"
        ):
            self.settings_window.destroy()

    def _load_current_settings(self):
        """加载当前设置"""
        if not self.current_settings:
            return
            
        # 加载语言设置
        if 'language' in self.current_settings:
            self.language_var.set(self.current_settings['language'])
            
        # 加载每小时提醒设置
        if 'hourly_reminder' in self.current_settings:
            self.hourly_reminder_var.set(self.current_settings['hourly_reminder'])
            
        # 加载最大历史记录数量
        if 'max_history' in self.current_settings:
            self.max_history_var.set(str(self.current_settings['max_history']))
            
        # 加载主题设置
        if 'theme' in self.current_settings:
            self.theme_var.set(self.current_settings['theme'])
            
        # 加载强调色
        if 'accent_color' in self.current_settings:
            self.color_var.set(self.current_settings['accent_color'])
            self.color_preview.config(bg=self.current_settings['accent_color'])
            
        # 加载声音设置
        if 'enable_sound' in self.current_settings:
            self.enable_sound_var.set(self.current_settings['enable_sound'])
            
        if 'sound_type' in self.current_settings:
            self.sound_type_var.set(self.current_settings['sound_type'])
            
        if 'volume' in self.current_settings:
            self.volume_var.set(self.current_settings['volume'])
            self._update_volume_label()

    def _create_settings_content(self):
        """创建设置面板内容"""
        main_frame = tk.Frame(self.settings_window, bg=UI_CONFIG['bg_color'], padx=20, pady=15)
        main_frame.pack(fill="both", expand=True)
        
        # 删除了标题标签
        
        # 创建选项卡
        tab_control = ttk.Notebook(main_frame)
        tab_control.pack(fill="both", expand=True)
        
        # 常规设置选项卡
        general_tab = self._create_general_tab(tab_control)
        tab_control.add(general_tab, text=self.translation.get_text("general_tab"))
        
        # 外观设置选项卡
        appearance_tab = self._create_appearance_tab(tab_control)
        tab_control.add(appearance_tab, text=self.translation.get_text("appearance_tab"))
        
        # 声音设置选项卡
        sound_tab = self._create_sound_tab(tab_control)
        tab_control.add(sound_tab, text=self.translation.get_text("sound_tab"))
        
        # 底部按钮区域
        button_frame = tk.Frame(main_frame, bg=UI_CONFIG['bg_color'], pady=15)
        button_frame.pack(fill="x")
        
        # 保存按钮 - 改进样式，增加视觉吸引力
        save_button = tk.Button(
            button_frame,
            text=self.translation.get_text("save_settings"),
            command=self._save_settings,
            bg=UI_CONFIG['accent_color'],
            fg="white",
            font=(FONT_CONFIG['main_font'][0], FONT_CONFIG['main_font'][1], "bold"),
            padx=25,
            pady=8,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            activebackground=UI_CONFIG['success_color'],
            activeforeground="white"
        )
        save_button.pack(side=tk.RIGHT, padx=10)
        
        # 为保存按钮添加悬停效果
        def on_enter(e):
            save_button['bg'] = UI_CONFIG['success_color']
        
        def on_leave(e):
            save_button['bg'] = UI_CONFIG['accent_color']
        
        save_button.bind("<Enter>", on_enter)
        save_button.bind("<Leave>", on_leave)
        
        # 取消按钮 - 改进样式
        cancel_button = tk.Button(
            button_frame,
            text=self.translation.get_text("cancel"),
            command=self.settings_window.destroy,
            bg=UI_CONFIG['secondary_color'],
            fg=UI_CONFIG['text_color'],
            font=FONT_CONFIG['main_font'],
            padx=20,
            pady=8,
            relief="flat",
            borderwidth=1,
            cursor="hand2"
        )
        cancel_button.pack(side=tk.RIGHT, padx=10)
        
    def _create_general_tab(self, parent):
        """创建常规设置选项卡"""
        tab = tk.Frame(parent, bg="white", padx=15, pady=15)
        
        # 语言设置 - 只保留切换按钮，移除标签和其他冗余元素
        lang_frame = tk.Frame(tab, bg="white")
        lang_frame.pack(fill="x", pady=5)
        
        # 创建语言切换按钮，显示另一种语言的名称
        self.language_var = tk.StringVar(value=self.translation.current_language)
        self.language_button = tk.Button(
            lang_frame,
            text=self.translation.get_text("language"),  # 显示另一语言的名称
            command=self._toggle_language,
            bg=UI_CONFIG['accent_color'],
            fg="white",
            font=FONT_CONFIG['main_font'],
            padx=15,
            pady=2,
            relief="flat",
            borderwidth=0,
            cursor="hand2"
        )
        self.language_button.pack(anchor="w")
        
        # 每小时提醒默认设置
        reminder_frame = tk.Frame(tab, bg="white")
        reminder_frame.pack(fill="x", pady=10)
        
        self.hourly_reminder_var = tk.BooleanVar(value=True)
        reminder_check = ttk.Checkbutton(reminder_frame,
                                      text=self.translation.get_text("default_hourly_reminder"),
                                      variable=self.hourly_reminder_var)
        reminder_check.pack(anchor="w")
        
        # 最大历史记录数量
        history_frame = tk.Frame(tab, bg="white")
        history_frame.pack(fill="x", pady=10)
        
        history_label = tk.Label(history_frame, 
                               text=self.translation.get_text("max_history"),
                               bg="white",
                               fg=UI_CONFIG['text_color'],
                               font=FONT_CONFIG['main_font'])
        history_label.pack(anchor="w")
        
        self.max_history_var = tk.StringVar(value="10")
        history_entry = tk.Entry(history_frame,
                               textvariable=self.max_history_var,
                               width=10)
        history_entry.pack(anchor="w", pady=5)
        
        # 添加输入验证 - 只能输入数字
        vcmd = (self.parent.register(self._validate_number_input), '%P')
        history_entry.config(validate="key", validatecommand=vcmd)
        
        return tab

    def _toggle_language(self):
        """切换语言"""
        # 切换语言
        new_language = self.translation.toggle_language()
        self.language_var.set(new_language)
        
        # 更新按钮文本为新语言下显示的另一语言名称
        self.language_button.config(text=self.translation.get_text("language"))
        
        # 更新所有标签和按钮文本
        self._update_ui_texts()

    def _update_ui_texts(self):
        """更新界面上的所有文本"""
        if not self.settings_window:
            return
        
        # 更新窗口标题
        self.settings_window.title(self.translation.get_text("settings"))
        
        # 更新选项卡文本
        tab_control = [w for w in self.settings_window.winfo_children()[0].winfo_children() 
                      if isinstance(w, ttk.Notebook)]
        if tab_control:
            tab_control = tab_control[0]
            tab_control.tab(0, text=self.translation.get_text("general_tab"))
            tab_control.tab(1, text=self.translation.get_text("appearance_tab"))
            tab_control.tab(2, text=self.translation.get_text("sound_tab"))
        
        # 更新底部按钮
        button_frame = [w for w in self.settings_window.winfo_children()[0].winfo_children() 
                        if isinstance(w, tk.Frame) and len(w.winfo_children()) >= 2]
        if button_frame:
            button_frame = button_frame[-1]  # 最后一个Frame应该是按钮Frame
            for child in button_frame.winfo_children():
                if isinstance(child, tk.Button):
                    if child.cget("text") == "保存" or child.cget("text") == "Save":
                        child.config(text=self.translation.get_text("save_settings"))
                    elif child.cget("text") == "取消" or child.cget("text") == "Cancel":
                        child.config(text=self.translation.get_text("cancel"))
        
        # 更新各选项卡内的文本
        self._update_general_tab_texts()
        self._update_appearance_tab_texts()
        self._update_sound_tab_texts()

    def _update_general_tab_texts(self):
        """更新常规选项卡的文本"""
        # 找到常规选项卡
        tab_control = [w for w in self.settings_window.winfo_children()[0].winfo_children() 
                      if isinstance(w, ttk.Notebook)]
        if not tab_control:
            return
            
        tab_control = tab_control[0]
        general_tab = tab_control.winfo_children()[0]
        
        # 更新语言标签
        for frame in general_tab.winfo_children():
            if not isinstance(frame, tk.Frame):
                continue
                
            for child in frame.winfo_children():
                if isinstance(child, ttk.Checkbutton):
                    child.config(text=self.translation.get_text("default_hourly_reminder"))
                elif isinstance(child, tk.Label) and (child.cget("text").startswith("最大历史") or 
                                                    child.cget("text").startswith("Maximum")):
                    child.config(text=self.translation.get_text("max_history"))

    def _update_appearance_tab_texts(self):
        """更新外观选项卡的文本"""
        tab_control = [w for w in self.settings_window.winfo_children()[0].winfo_children() 
                      if isinstance(w, ttk.Notebook)]
        if not tab_control:
            return
            
        tab_control = tab_control[0]
        if len(tab_control.winfo_children()) < 2:
            return
            
        appearance_tab = tab_control.winfo_children()[1]
        
        for frame in appearance_tab.winfo_children():
            if not isinstance(frame, tk.Frame):
                continue
                
            for child in frame.winfo_children():
                if isinstance(child, tk.Label) and (child.cget("text").startswith("主题") or 
                                                  child.cget("text").startswith("Theme")):
                    child.config(text=self.translation.get_text("theme"))
                elif isinstance(child, ttk.Radiobutton) and (child.cget("text") == "浅色" or 
                                                           child.cget("text") == "Light"):
                    child.config(text=self.translation.get_text("light_theme"))
                elif isinstance(child, ttk.Radiobutton) and (child.cget("text") == "深色" or 
                                                           child.cget("text") == "Dark"):
                    child.config(text=self.translation.get_text("dark_theme"))
                elif isinstance(child, tk.Label) and (child.cget("text").startswith("强调色") or 
                                                    child.cget("text").startswith("Accent")):
                    child.config(text=self.translation.get_text("accent_color"))
                elif isinstance(child, tk.Button) and (child.cget("text") == "选择颜色" or 
                                                     child.cget("text") == "Choose color"):
                    child.config(text=self.translation.get_text("choose_color"))

    def _update_sound_tab_texts(self):
        """更新声音选项卡的文本"""
        tab_control = [w for w in self.settings_window.winfo_children()[0].winfo_children() 
                      if isinstance(w, ttk.Notebook)]
        if not tab_control:
            return
            
        tab_control = tab_control[0]
        if len(tab_control.winfo_children()) < 3:
            return
            
        sound_tab = tab_control.winfo_children()[2]
        
        for frame in sound_tab.winfo_children():
            if not isinstance(frame, tk.Frame):
                continue
                
            for child in frame.winfo_children():
                if isinstance(child, ttk.Checkbutton):
                    child.config(text=self.translation.get_text("enable_sound"))
                elif isinstance(child, tk.Label) and (child.cget("text").startswith("提醒声音") or 
                                                    child.cget("text").startswith("Alert sound")):
                    child.config(text=self.translation.get_text("sound_type"))
                elif isinstance(child, ttk.Radiobutton) and (child.cget("text") == "蜂鸣声" or 
                                                           child.cget("text") == "Beep"):
                    child.config(text=self.translation.get_text("beep_sound"))
                elif isinstance(child, ttk.Radiobutton) and (child.cget("text") == "旋律" or 
                                                           child.cget("text") == "Melody"):
                    child.config(text=self.translation.get_text("melody_sound"))
                elif isinstance(child, tk.Label) and (child.cget("text") == "音量:" or 
                                                    child.cget("text") == "Volume:"):
                    child.config(text=self.translation.get_text("volume"))

    def _create_appearance_tab(self, parent):
        """创建外观设置选项卡
        
        Args:
            parent: 父容器
            
        Returns:
            tk.Frame: 外观设置选项卡
        """
        tab = tk.Frame(parent, bg="white", padx=15, pady=15)
        
        # 主题选择
        theme_frame = tk.Frame(tab, bg="white")
        theme_frame.pack(fill="x", pady=5)
        
        theme_label = tk.Label(theme_frame, 
                             text=self.translation.get_text("theme"),
                             bg="white",
                             fg=UI_CONFIG['text_color'],
                             font=FONT_CONFIG['main_font'])
        theme_label.pack(anchor="w")
        
        self.theme_var = tk.StringVar(value="light")
        light_radio = ttk.Radiobutton(theme_frame, 
                                   text=self.translation.get_text("light_theme"),
                                   variable=self.theme_var, 
                                   value="light")
        light_radio.pack(anchor="w", pady=2)
        
        dark_radio = ttk.Radiobutton(theme_frame, 
                                   text=self.translation.get_text("dark_theme"),
                                   variable=self.theme_var, 
                                   value="dark")
        dark_radio.pack(anchor="w")
        
        # 自定义颜色
        color_frame = tk.Frame(tab, bg="white")
        color_frame.pack(fill="x", pady=10)
        
        color_label = tk.Label(color_frame, 
                             text=self.translation.get_text("accent_color"),
                             bg="white",
                             fg=UI_CONFIG['text_color'],
                             font=FONT_CONFIG['main_font'])
        color_label.pack(anchor="w")
        
        self.color_var = tk.StringVar(value=UI_CONFIG['accent_color'])
        
        self.color_preview = tk.Frame(color_frame, 
                               bg=UI_CONFIG['accent_color'], 
                               width=30, 
                               height=30,
                               relief="solid",
                               borderwidth=1)
        self.color_preview.pack(side=tk.LEFT, padx=(0, 10), pady=5)
        
        # 使Frame可点击选择颜色
        self.color_preview.bind("<Button-1>", lambda e: self._choose_color(self.color_preview))
        
        color_button = tk.Button(color_frame,
                               text=self.translation.get_text("choose_color"),
                               command=lambda: self._choose_color(self.color_preview),
                               bg=UI_CONFIG['bg_color'],
                               fg=UI_CONFIG['text_color'],
                               relief="flat",
                               borderwidth=1)
        color_button.pack(side=tk.LEFT, pady=5)
        
        return tab
        
    def _create_sound_tab(self, parent):
        """创建声音设置选项卡
        
        Args:
            parent: 父容器
            
        Returns:
            tk.Frame: 声音设置选项卡
        """
        tab = tk.Frame(parent, bg="white", padx=15, pady=15)
        
        # 启用声音设置
        sound_frame = tk.Frame(tab, bg="white")
        sound_frame.pack(fill="x", pady=5)
        
        self.enable_sound_var = tk.BooleanVar(value=True)
        sound_check = ttk.Checkbutton(sound_frame,
                                    text=self.translation.get_text("enable_sound"),
                                    variable=self.enable_sound_var)
        sound_check.pack(anchor="w")
        
        # 提醒声音设置
        sound_type_frame = tk.Frame(tab, bg="white")
        sound_type_frame.pack(fill="x", pady=10)
        
        sound_type_label = tk.Label(sound_type_frame, 
                                  text=self.translation.get_text("sound_type"),
                                  bg="white",
                                  fg=UI_CONFIG['text_color'],
                                  font=FONT_CONFIG['main_font'])
        sound_type_label.pack(anchor="w")
        
        self.sound_type_var = tk.StringVar(value="beep")
        beep_radio = ttk.Radiobutton(sound_type_frame, 
                                   text=self.translation.get_text("beep_sound"),
                                   variable=self.sound_type_var, 
                                   value="beep")
        beep_radio.pack(anchor="w", pady=2)
        
        melody_radio = ttk.Radiobutton(sound_type_frame, 
                                     text=self.translation.get_text("melody_sound"),
                                     variable=self.sound_type_var, 
                                     value="melody")
        melody_radio.pack(anchor="w")
        
        # 音量设置
        volume_frame = tk.Frame(tab, bg="white")
        volume_frame.pack(fill="x", pady=10)
        
        volume_label = tk.Label(volume_frame, 
                              text=self.translation.get_text("volume"),
                              bg="white",
                              fg=UI_CONFIG['text_color'],
                              font=FONT_CONFIG['main_font'])
        volume_label.pack(anchor="w")
        
        self.volume_var = tk.IntVar(value=80)
        volume_scale = ttk.Scale(volume_frame,
                               from_=0,
                               to=100,
                               orient="horizontal",
                               variable=self.volume_var)
        volume_scale.pack(fill="x", pady=5)
        
        # 音量显示标签
        self.volume_value_label = tk.Label(volume_frame,
                                         text="80%",
                                         bg="white")
        self.volume_value_label.pack(anchor="e")
        
        # 绑定音量变化事件
        volume_scale.bind("<Motion>", self._update_volume_label)
        
        return tab
    
    def _update_volume_label(self, event=None):
        """更新音量显示标签"""
        self.volume_value_label.config(text=f"{self.volume_var.get()}%")
    
    def _choose_color(self, preview_frame):
        """选择自定义颜色
        
        Args:
            preview_frame: 颜色预览框架
        """
        color = colorchooser.askcolor(initialcolor=UI_CONFIG['accent_color'])
        if color[1]:  # 如果选择了颜色
            preview_frame.config(bg=color[1])
            self.color_var.set(color[1])
    
    def _validate_number_input(self, value):
        """验证输入是否为数字
        
        Args:
            value: 输入值
            
        Returns:
            bool: 是否为有效数字
        """
        return value.isdigit() or value == ""
    
    def _save_settings(self):
        """保存设置"""
        try:
            # 验证最大历史记录输入
            max_history = self.max_history_var.get()
            if not max_history or not max_history.isdigit():
                messagebox.showerror(
                    self.translation.get_text("settings"),
                    self.translation.get_text("invalid_number_error")
                )
                return
                
            # 这里将设置值保存起来
            settings = {
                'language': self.language_var.get(),
                'hourly_reminder': self.hourly_reminder_var.get(),
                'max_history': int(max_history),
                'theme': self.theme_var.get(),
                'accent_color': self.color_var.get(),
                'enable_sound': self.enable_sound_var.get(),
                'sound_type': self.sound_type_var.get(),
                'volume': self.volume_var.get()
            }
            
            # 保存当前设置
            self.current_settings = settings
            
            # 调用设置变更回调函数
            if self.on_settings_changed:
                self.on_settings_changed(settings)
                
                # 显示保存成功提示
                messagebox.showinfo(
                    self.translation.get_text("settings"),
                    "设置已保存成功！"
                )
            
            self.settings_window.destroy()
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror(
                self.translation.get_text("settings"),
                f"保存失败: {str(e)}"
            )