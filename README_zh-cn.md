# daily-reporter

上海第二工业大学健康管理系统每日一报自动报送工具

支持**微信推送报送结果**、**多用户**、**定时自动报送**

体温在用户定义的区间内使用正态分布随机生成。

[English](README.md) | [中文](README_zh-cn.md)

## 如果你不想折腾

这里有为 Windows 打包好的版本，开箱即用。

[reporter-win.7z](https://github.com/ReekyStive/daily-reporter/releases/download/v1.3/reporter-win.7z)

其中包含

- 本项目源代码
- Chrome
- ChromeDriver
- Python 解释器
- 依赖包

## 安装 Google Chrome

使用这个自动报送工具之前，你需要安装 [Google Chrome](https://www.google.com/chrome/)。

## 下载 ChromeDriver

在 Google Chrome 中进入 `chrome://version` 查看 Google Chrome 版本，并下载对应版本的 [ChromeDriver](https://chromedriver.chromium.org/downloads)。

下载 ChromeDriver 后，你需要将可执行文件所在的目录加入 `PATH` 环境变量中。你也可以跳过此步，但如果跳过此步，你需要将 ChromeDriver 可执行文件的路径写入 `config.py` 中。

## 安装 Python

[下载](https://www.python.org/downloads/)并安装 `Python 3.x`。

请在安装时勾选 `Add to PATH`。如果不勾选此项，你需要将后文中的 `pip` 和 `python` 替换为完整路径。

## 安装 pip 依赖

``` bash
pip install selenium schedule requests
```

## 编辑配置文件

### 编辑基础配置

如果你在没有图形化桌面的服务器上使用此脚本，请将 `headless` 设为 `True`。使用 `headless` 模式将不会显示 Google Chrome 界面。在没有图形化桌面的服务器上使用此脚本时若不使用 `headless` 模式可能会引发错误。

你可以设定随机生成的体温的最小值 `min_temperature` 和最大值 `max_temperature`，单位为摄氏度。体温将在设定的区间（闭区间）中使用正态分布随机生成。

`timeout` 为每个用户在提交时的最长等待时间，单位为秒 `second(s)`。网络拥堵时提交可能需要等待较长时间。若超过设定的时间仍未成功即视为报送失败，将结束当次报送。默认值为 `600`。

`driver_path` 为 ChromeDriver 可执行文件所在路径。若指定了 ChromeDriver 路径，则使用指定的可执行文件。若设置为 `auto` ，则会在 `PATH` 中寻找 ChromeDriver。默认值为 `'auto'`。

### 用户信息配置

你可以在 `users` 中添加多个用户。你需要为每个用户提供 `username` 和 `password`。

``` python
users = [
    {
        'username': '20201234567',
        'password': '123456',
        'use_wechat': True,
        'uid': 'UID_ABCDEF0123456789abcdef012345'
    }
]
```

### 配置微信推送

如果你不使用微信推送，请将 `app_token` 设置为 `None`。事实上，当不使用微信推送时你可将该项设置为任意值。

所有用户共享同一个 `app_token`，但你可对每一个用户分别设定是否使用微信推送。无论是否使用微信推送，每个用户都必须有 `user_wechat` 配置。当某一用户的 `use_wechat` 为 `False` 时，该用户的 `uid` 则可为任意值，但推荐设置为 `None`。

该工具使用 [WxPusher](https://wxpusher.zjiecode.com/) 进行微信推送。关于如何获取 `app_token` 和 `uid`，参见 [WxPusher](https://wxpusher.zjiecode.com/)。

### 更改定时时间

在 `scheduler.py` 中修改

``` python
schedule.every().day.at('00:30').do(job)
schedule.every().day.at('07:30').do(job)
```

以自定义报送时间。

报送会在到达指定时间时按 `config.py` 中的用户顺序依次进行。

## 运行

若要立即对所有用户执行一次报送，请运行 `daily_reporter.py`。程序会在本次报送结束后退出。

``` bash
python daily_reporter.py
```

若要开始定时程序，请运行 `scheduler.py`。程序会一直运行，并在每次到达指定时间点时都对所有用户执行一次报送。

``` bash
python scheduler.py
```
