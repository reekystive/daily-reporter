# daily-reporter

Auto daily reporter for SSPU HSM

Support WeChat push, multi-user, scheduled auto report

Support Google Chrome, Firefox, Microsoft Edge

[English](README.md) | [中文](README_zh-cn.md)

**Click Chinese above for more detailed instructions**

## Quick Start

This is the ready-to-use version for Windows: [reporter-win32.7z](https://github.com/ReekyStive/daily-reporter/releases/download/v1.5/reporter-win32.7z)

## Guide

- Install `Python 3.*`
  - Install `selenium`
  - Install `schedule`
  - Install `requests`
- Install `Chrome`
  - Download `Chrome WebDriver` and add it to `Path`
- Edit `config.py`
  - Edit `driver_path` (optional)
  - Edit `min_temperature` and `max_temperature` (optional)
  - Edit `timeout` (optional)
  - Edit `app_token` (get from [WxPusher](https://wxpusher.zjiecode.com/)) (optional)
  - Edit `users`
    - Edit `username` and `password`
    - Edit `uid` (get from [WxPusher](https://wxpusher.zjiecode.com/)) (optional)
- Change scheduled time in `scheduler.py` (optional)
- Run `daily_reporter.py` or `scheduler.py`
