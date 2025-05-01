# -*- coding: utf-8 -*-
"""
声音管理模块
"""

import platform
import os

class SoundManager:
    """声音管理器类"""
    
    # 类变量，用于设置
    enable_sound = True
    sound_type = "beep"  # beep 或 melody
    volume = 80  # 音量百分比 (0-100)
    
    @staticmethod
    def play_beep(frequency=1000, duration=500):
        """播放蜂鸣声
        
        Args:
            frequency: 蜂鸣频率（Hz）
            duration: 持续时间（毫秒）
        """
        # 如果声音被禁用，直接返回
        if not SoundManager.enable_sound:
            return
            
        # 根据音量调整频率或持续时间
        volume_factor = SoundManager.volume / 100.0
        
        system = platform.system()
        
        if system == "Windows":
            try:
                import winsound
                winsound.Beep(int(frequency), int(duration * volume_factor))
            except Exception as e:
                print(f"播放声音失败: {e}")
        elif system == "Darwin":  # macOS
            try:
                os.system(f"afplay /System/Library/Sounds/Tink.aiff")
            except Exception:
                # 回退到print
                print("\a")  # 系统beep
        else:  # Linux和其他系统
            try:
                os.system(f"beep -f {frequency} -l {int(duration * volume_factor)}")
            except Exception:
                # 回退到print
                print("\a")  # 系统beep
    
    @staticmethod
    def play_melody():
        """播放旋律声音"""
        # 如果声音被禁用，直接返回
        if not SoundManager.enable_sound:
            return
            
        system = platform.system()
        
        if system == "Windows":
            try:
                import winsound
                # 播放一个简短的旋律
                for freq in [523, 659, 784]:  # C5, E5, G5 (C大调和弦)
                    winsound.Beep(freq, 200)
            except Exception as e:
                print(f"播放声音失败: {e}")
        elif system == "Darwin":  # macOS
            try:
                os.system(f"afplay /System/Library/Sounds/Glass.aiff")
            except Exception:
                # 回退到print
                print("\a")  # 系统beep
        else:  # Linux和其他系统
            try:
                # 在Linux上尝试播放一个简短的旋律
                for freq in [523, 659, 784]:  # C5, E5, G5 (C大调和弦)
                    os.system(f"beep -f {freq} -l 200")
            except Exception:
                # 回退到print
                print("\a")  # 系统beep
    
    @staticmethod
    def play_completion_sound():
        """播放完成声音"""
        if SoundManager.sound_type == "melody":
            SoundManager.play_melody()
        else:  # 默认为beep
            SoundManager.play_beep(1000, 1000)
    
    @staticmethod
    def play_reminder_sound():
        """播放提醒声音"""
        if SoundManager.sound_type == "melody":
            SoundManager.play_melody()
        else:  # 默认为beep
            SoundManager.play_beep(1000, 500)