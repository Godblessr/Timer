# Countdown Timer / 倒计时提醒软件

A simple, bilingual (English/Chinese) countdown timer application with hourly reminders and history tracking.

一个简单的双语（英文/中文）倒计时应用程序，具有每小时提醒和历史记录功能。

## Features / 功能

- ⏱️ Set custom countdown time / 设置自定义倒计时时间
- 🔔 Hourly reminders / 每小时提醒
- 💾 Save and load timer history / 保存和加载计时器历史记录
- ⏯️ Pause, resume and reset timer / 暂停、继续和重置计时器
- 🌐 English and Chinese language support / 支持英文和中文
- 🔊 Customizable sound options (beep or melody) / 可自定义声音选项（蜂鸣或旋律）
- 🎨 Light and dark theme options / 亮色和暗色主题选项
- 🎯 Color-coded timer display (changes color based on remaining time) / 颜色编码的计时器显示（根据剩余时间改变颜色）
- ⚙️ Customizable settings panel / 可自定义设置面板

## Screenshots / 截图

<div align="center" style="display: flex; justify-content: space-around; flex-wrap: wrap;">
  <div style="margin: 10px;">
    <p><strong>Chinese Interface / 中文界面</strong></p>
    <img src="/resources/images/screenshot_CN.png" alt="Chinese Interface" width="250"/>
  </div>
  
  <div style="margin: 10px;">
    <p><strong>English Interface / 英文界面</strong></p>
    <img src="/resources/images/screenshot_EN.png" alt="English Interface" width="250"/>
  </div>
</div>

## Installation / 安装

### From Source / 从源代码安装

1. Clone this repository / 克隆此仓库
   ```bash
   git clone https://github.com/Godblessr/Timer
   cd Timer
   ```

2. Install dependencies / 安装依赖项
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application / 运行应用程序
   ```bash
   python main.py
   ```

### Executable / 可执行文件

Download the latest release from the [Releases](https://github.com/Godblessr/Timer/releases) page.

从[发布页面](https://github.com/Godblessr/Timer/releases)下载最新版本。

## Requirements / 依赖项

- Python 3.6+
- tkinter (usually comes with Python)
- Platform-specific sound modules:
  - Windows: Built-in `winsound` module
  - macOS: System sounds via `afplay` command
  - Linux: `beep` command (may require installation)

## Building / 构建

To build the executable yourself / 自行构建可执行文件:

```bash
pyinstaller Timer.spec
```

## Application Features / 应用功能

### Timer Display / 计时器显示
- Displays remaining time in HH:MM:SS format / 以 HH:MM:SS 格式显示剩余时间
- Changes color based on remaining time / 根据剩余时间变化颜色
  - Red: Less than 1 minute / 红色：少于1分钟
  - Orange/Yellow: Less than 5 minutes / 橙色/黄色：少于5分钟
  - Blue (default): More than 5 minutes / 蓝色（默认）：超过5分钟

### History Tracking / 历史记录跟踪
- Automatically saves timer durations / 自动保存计时器持续时间
- Apply previous timer values quickly / 快速应用以前的计时器值
- Delete unwanted history entries / 删除不需要的历史记录条目

### Settings / 设置
- Toggle between light and dark themes / 在亮色和暗色主题之间切换
- Customize accent colors / 自定义强调色
- Configure sound settings / 配置声音设置
- Set maximum history entries / 设置最大历史记录条目数

## Contributing / 贡献

Contributions are welcome! Please feel free to submit a Pull Request.

欢迎贡献！请随时提交 Pull Request。

## License / 许可证

This project is licensed under the MIT License - see the LICENSE file for details.

本项目采用MIT许可证 - 详情请参阅LICENSE文件。
