<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot_plugin_matchreminder

_✨ NoneBot 插件简单描述 ✨_


<a href="./LICENSE">
    <img src="https://img.shields.io/github/license/zhuhiki/nonebot_plugin_matchreminder.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/nonebot_plugin_matchreminder">
    <img src="https://img.shields.io/pypi/v/nonebot_plugin_matchreminder.svg" alt="pypi">
</a>
<img src="https://img.shields.io/badge/python-3.8+-blue.svg" alt="python">

</div>

## 📖 介绍

算法比赛提醒，可以自动设置时间来为即将到来的算法比赛设置提醒(默认是赛前半小时,可以自己修改),同时也能查询今日在codeforces，牛客，atc上的比赛，让群友不再错过比赛(偷懒)

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot_plugin_matchreminder

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot_plugin_matchreminder
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot_plugin_matchreminder"]

</details>

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

| 配置项 | 必填 | 默认值 | 说明 |
|:-----:|:----:|:----:|:----:|
| SUPERUSERS | 是 | 无 | 有功能需要超级管理员权限 |

在插件里的config文件里填写需要定时发送的时间和群聊

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| /cf，/nc,/atc | 群员 | 否 | 群聊 | 返回对应的比赛信息 |
| /今日比赛 | 群员 | 否 | 群聊 | 返回今天的比赛 |
| /提醒比赛 | 超级管理员 | 否 | 群聊 | 手动定时提醒 |
| /开摆 | 超级管理员 | 否 | 群聊 | 清除所有定时任务 |
