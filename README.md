# Tsinghua Auth GUI

清华大学校园网第三方客户端 V1.0

## Highlights

- 基于PyQt5，原生跨平台（Windows、Linux、MacOS）
- 整合net、auth4、auth6三种认证方式
- 最小化到托盘
- 自动断线重连（勾选后即可自动保持在线状态）

## 支持网络

- 可通过[net.tsinghua.edu.cn](http://net.tsinghua.edu.cn/)认证的校园网（Tsinghua、Tsinghua-5G无线网和部分有线网）
- 可通过[auth*.tsinghua.edu.cn](http://auth.tsinghua.edu.cn/)认证的校园网（Tsinghua-IPv4、Tsinghua-IPv6无线网和部分有线网）

## 不支持网络

- Tsinghua-Secure无线网

## 环境

Python版本>=3.6

测试环境：

- Windows 10 64-bit
- Ubuntu 18.04 Desktop 64-bit
- Raspbian Stretch with desktop

## 库

### six

使用pip安装：

```cmd
python3 -m pip install six
```

### PyQt5

在WIndows系统下可使用pip安装：

```cmd
python3 -m pip install PyQt5
```

在类Debian（含Ubuntu、Raspbian）系统下可使用apt-get安装：

```sh
$ sudo apt install python3-pyqt5
```

## 感谢

感谢[tunet-python](https://github.com/yuantailing/tunet-python)提供的认证库

