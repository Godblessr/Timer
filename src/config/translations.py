# -*- coding: utf-8 -*-
"""
语言翻译模块，管理应用程序的多语言支持
"""

# 翻译字典
TRANSLATIONS = {
    "zh_CN": {
        "app_title": "倒计时提醒软件",
        "hours": "小时:",
        "minutes": "分钟:",
        "seconds": "秒:",
        "history": "历史记录:",
        "apply": "应用",
        "delete": "删除",
        "hourly_reminder": "每小时提醒",
        "start": "开始",
        "pause": "暂停",
        "resume": "继续",
        "reset": "重置",
        "ready": "准备就绪",
        "running": "倒计时进行中...",
        "paused": "倒计时已暂停",
        "negative_time_error": "时间不能为负数！",
        "empty_time_error": "请设置倒计时时间！",
        "invalid_number_error": "请输入有效的数字！",
        "hourly_reminder_msg": "已经过去一小时！\n还剩 {0} 小时 {1} 分钟",
        "completed_msg": "倒计时已结束！",
        "delete_success": "已删除选中的历史记录",
        "github_info": "访问 GitHub 获取最新版本",
        "language": "English",
        "about": "关于",
        "about_title": "关于倒计时提醒软件",
        "about_content": "倒计时提醒软件\n版本：{0}\n作者：Godblessr\n© 2025 版权所有",
        # 设置面板相关翻译
        "settings": "设置",
        "general_tab": "常规",
        "appearance_tab": "外观",
        "sound_tab": "声音",
        "save_settings": "保存",
        "cancel": "取消",
        "language_setting": "语言:",
        "default_hourly_reminder": "默认启用每小时提醒",
        "max_history": "最大历史记录数量:",
        "theme": "主题:",
        "light_theme": "浅色",
        "dark_theme": "深色",
        "accent_color": "强调色:",
        "choose_color": "选择颜色",
        "enable_sound": "启用声音",
        "sound_type": "提醒声音类型:",
        "beep_sound": "蜂鸣声",
        "melody_sound": "旋律",
        "volume": "音量:"
    },
    "en_US": {
        "app_title": "Countdown Timer",
        "hours": "Hours:",
        "minutes": "Minutes:",
        "seconds": "Seconds:",
        "history": "History:",
        "apply": "Apply",
        "delete": "Delete",
        "hourly_reminder": "Hourly Reminder",
        "start": "Start",
        "pause": "Pause",
        "resume": "Resume",
        "reset": "Reset",
        "ready": "Ready",
        "running": "Countdown running...",
        "paused": "Countdown paused",
        "negative_time_error": "Time cannot be negative!",
        "empty_time_error": "Please set countdown time!",
        "invalid_number_error": "Please enter valid numbers!",
        "hourly_reminder_msg": "One hour has passed!\n{0} hours {1} minutes remaining",
        "completed_msg": "Countdown completed!",
        "delete_success": "Selected history item deleted",
        "github_info": "Visit GitHub for latest version",
        "language": "中文",
        "about": "About",
        "about_title": "About Countdown Timer",
        "about_content": "Countdown Timer\nVersion: {0}\nAuthor: Godblessr\n© 2025 All rights reserved",
        # 设置面板相关翻译
        "settings": "Settings",
        "general_tab": "General",
        "appearance_tab": "Appearance",
        "sound_tab": "Sound",
        "save_settings": "Save",
        "cancel": "Cancel",
        "language_setting": "Language:",
        "default_hourly_reminder": "Enable hourly reminder by default",
        "max_history": "Maximum history items:",
        "theme": "Theme:",
        "light_theme": "Light",
        "dark_theme": "Dark",
        "accent_color": "Accent color:",
        "choose_color": "Choose color",
        "enable_sound": "Enable sound",
        "sound_type": "Alert sound type:",
        "beep_sound": "Beep",
        "melody_sound": "Melody",
        "volume": "Volume:"
    }
}

class TranslationManager:
    """翻译管理器类"""
    
    def __init__(self, default_language="zh_CN"):
        """初始化翻译管理器
        
        Args:
            default_language: 默认语言代码
        """
        self.current_language = default_language
        
    def get_text(self, key):
        """获取当前语言下的文本
        
        Args:
            key: 文本键名
            
        Returns:
            str: 对应的翻译文本
        """
        return TRANSLATIONS[self.current_language].get(key, key)
    
    def toggle_language(self):
        """切换语言"""
        if self.current_language == "zh_CN":
            self.current_language = "en_US"
        else:
            self.current_language = "zh_CN"
        return self.current_language