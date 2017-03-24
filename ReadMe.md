# GaussBayesPicSort
## 模式识别大作业 - 图片的贝叶斯分类器分类

> 成品二进制包及文档请查看[gh-pages分支](https://github.com/zhengxiaoyao0716/GaussBayesPicSort/tree/gh-pages)，点这里查看[文档及展示](https://zhengxiaoyao0716.github.io/GaussBayesPicSort/)

***
### 一、环境与运行
第一步：安装Python3并配置好环境变量之类的，略

第二步：搭建运行环境
``` bash
# Windows
py -3 -m venv .env
# Linux
python3 -m venv .env
# Linux请将'Scripts'替换成'bin'，下同
.env\Scripts\pip install -r requirements.txt
```

第三步：选择版本并运行
``` bash
# 运行主程
.env\Scripts\python main.py
# 运行带UI界面的版本
.env\Scripts\python main-gui.py
```

### 二、编译与打包
第一步：安装开发环境依赖
``` bash
.env\Scripts\pip install -r requirements_dev.txt
```
第二步：选择工具打包
1. Pyinstaller: 对两个版本分别生成独立可执行二进制文件，大小约2 × 27MB
    ``` bash
    .env\Scripts\pyinstaller GaussBayesPicSort.spec & .env\Scripts\pyinstaller GaussBayesPicSort-gui.spec

    # Windows系统输出目录结构如下：
    # - dist/
    #   -- assets/...
    #   -- GaussBayesPicSort.exe
    #   -- GaussBayesPicSort-gui.exe
    ```

2. cx_Freeze: 生成一个包含两个版本入口可执行二进制文件和一堆依赖的绿色免安装的程序包，大小约1 × 36MB

    ``` bash
    .env\Scripts\python setup.py bdist

    # Windows系统输出目录结构如下：
    # - dist/GaussBayesPicSort-*.*.win32.zip
    ```