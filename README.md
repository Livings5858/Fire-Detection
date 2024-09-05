# 火灾检测

## 介绍

基于OpenCV框架，识别火灾。
通过MQTT发布数据，供给其他模块展示。

* OpenCV： https://opencv.org/
* Python Eclipse Paho://eclipse.dev/paho/index.php?page=clients/python/index.php

## 火焰颜色范围

<img src="images\image.png" />


## 目录结构

```
src/
...
├── CameraSimulator.py        // 相机模拟器，使用图片作为输入进行火灾检测，并将结果通过MQTT发布
├── FireDetection.py          // 火灾检测算法实现
├── HSVColorDisplay.py        // 查看火焰颜色范围
├── RealCameraDeal.py         // 接收相机通过MQTT发布过来的真实图像，进行火灾检测，并将结果通过MQTT发布
```

## 快速开始

### 创建虚拟环境

通过执行 `venv` 指令来创建一个虚拟环境:

```powershell
python -m venv /path/to/new/virtual/environment
```

### 激活虚拟环境

| 平台    | Shell      | 用于激活虚拟环境的命令                |
| :------ | :--------- | :------------------------------------ |
| POSIX   | bash/zsh   | `$ source <venv>/bin/activate`        |
| POSIX   | fish       | `$ source <venv>/bin/activate.fis`    |
| POSIX   | csh/tcsh   | `$ source <venv>/bin/activate.csh`    |
| POSIX   | PowerShell | `$ <venv>/bin/Activate.ps1`           |
| Windows | cmd.exe    | `C:\> <venv>\Scripts\activate.bat`    |
| Windows | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1` |

### 安装库：

```powershell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple opencv-python numpy paho-mqtt
```

### 运行

```powershell
python CameraSimulator.py
```

## 关联仓库

* MQTT 数据展示后端实现：https://github.com/Livings5858/test-server
* MQTT 数据展示前端实现：https://github.com/Livings5858/test-ui

