# Tsinghua Auth GUI

同时支持GUI和命令行的清华校园网认证客户端

- auth_cl.py: 命令行
- auth_gui.py: GUI

## Highlights

- 同时支持GUI和命令行，原生跨平台（Windows、Linux、MacOS）
- 整合net、auth4、auth6三种认证方式
- 自动断线重连（勾选后即可自动保持在线状态）

## 支持网络

除Tsinghua-Secure以外的所有清华大学校园网认证，包括：

- 可通过[net.tsinghua.edu.cn](http://net.tsinghua.edu.cn/)认证的校园网（Tsinghua、Tsinghua-5G无线网和部分有线网）
- 可通过[auth*.tsinghua.edu.cn](http://auth.tsinghua.edu.cn/)认证的校园网（Tsinghua-IPv4、Tsinghua-IPv6无线网和部分有线网）

## 环境

Python版本>=3.6

测试环境：

- Windows 10 64-bit
- Ubuntu 18.04 Desktop 64-bit
- Raspbian Stretch with desktop

## 安装和使用

### 安装依赖库

#### six

使用pip安装：

```cmd
python3 -m pip install six
```

#### PyQt5（GUI选装）

在WIndows系统下可使用pip安装：

```cmd
python3 -m pip install PyQt5
```

在类Debian（包括Ubuntu、Raspbian）系统下可使用apt-get安装：

```sh
$ sudo apt install python3-pyqt5
```

### 使用

#### 命令行

第一次使用时会要求输入auth类型、用户名和密码，完成后会在当前目录下创建一个命令行和GUI通用的config.json文件，以后直接执行auth_cl.py文件就可以开始自动认证.

在Linux下推荐使用nohup或安装为service.

#### GUI

图形界面，目前比较坑的是关机的时候设置不会自动保存，点了叉之后才会保存，之后会改进这个问题.

## 感谢

感谢[tunet-python](https://github.com/yuantailing/tunet-python)提供的认证库

