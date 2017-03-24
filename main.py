#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
GaussBayesPicSort
@author: zhengxiaoyao0716
"""
import threading
from functools import reduce
from random import random
from sys import stdout

from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D as _
import colorama

colorama.init()


def print_progress(percent):
    """打印进度条"""
    if percent == 'OK':
        print(' : %s=> OK! |' % ''.join('=' for _ in range(100)))
    else:
        stdout.write(' : %s=> %s%02d%% |\r' % (
            ''.join('=' for _ in range(percent)),
            ''.join(' ' for _ in range(percent, 100)),
            percent
        ))


def is_ok():
    """确认是否可以"""
    line = input('这样可以吗？')
    return not ('否' in line or '不' in line or 'N' in line or 'n' in line)


def read_cate_points(csv_path):
    """读入分类采样点"""
    print("请输入分类的\033[1;34m基准坐标\033[0m")
    cate_points = []

    def read_line(line):
        """解析输入的坐标"""
        try:
            point = tuple(float(v) for v in line.split(','))
            if reduce(lambda l, r: l + 1 if r >= 0 and r <= 1 else l, point, 0) != 2:
                raise ValueError()
            cate_points.append(tuple(point))
        except:
            print("无效的输入！合法的格式为：\033[1;34mx, y\033[0m")
            print("取值范围为\033[1;34m[0, 1]\033[0m")
            print("您也可以或直接按下\033[1;34m回车\033[0m以结束输入")
    while True:
        size = len(cate_points)
        line = input('第%d类：' % (size + 1))
        if line == '':
            if size == 0:
                try:
                    with open(csv_path) as data_file:
                        while True:
                            line = data_file.readline()
                            if line == '':
                                break
                            else:
                                read_line(line)
                    print('从\033[1;34m%s\033[0m读取到分类：' % csv_path)
                except:
                    for _ in range(4):
                        cate_points.append((random(), random()))
                    print('随机取样分类：')
            elif size >= 2:
                print('输入完毕，您输入的数据为：')
            else:
                print('请至少输入\033[1;34m两组\033[0m分类的基准坐标！')
                continue
            # 打印输入的值并询问确认
            for point in cate_points:
                print('\t%f, %f' % point)
            # if is_ok():
            if True:
                break
            else:
                cate_points = []
        else:
            read_line(line)
    return cate_points


def main():
    """Entrypoint"""
    # 载入资源
    default_path = './assets/生活照-武.jpg'
    while True:
        path = input('请输入图片路径：(%s)\n' % default_path) or default_path
        try:
            image = Image.open(path)
        except IOError:
            print('读取图片失败，请检查图片路径')
        else:
            break
    csv_path = path[0:path.rfind('.')] + '.csv'
    length, width = image.size
    pixs = image.load()
    categories = []
    # 分类基准采样
    while True:
        new_image = image.copy()
        drawer = ImageDraw.Draw(new_image)
        i = 0
        for _x, _y in read_cate_points(csv_path):
            i += 1
            x, y = _x * (length - 1), _y * (width - 1)
            r = min(width, length) / 80
            drawer.ellipse(
                (x - r, y - r, x + r, y + r),
                outline=(0, 0, 0)
            )
            drawer.text(
                (x - r / 2, y - r), str(i), fill=(0, 0, 0),
                font=ImageFont.truetype(font='simhei', size=int(2 * r))
            )
            categories.append(pixs[x, y])
        threading.Thread(target=new_image.show, name='Preview').start()
        print('下面您将看到：用来分类的\033[1;34m基准点\033[0m的预览')
        if is_ok():
            break
        else:
            categories = []
            csv_path = ''
    # 图片分类
    print('\n正在分类，请稍候')
    new_image = Image.new('RGB', image.size, (255, 255, 255))
    drawer = ImageDraw.Draw(new_image)
    p = 0
    for x in range(length):
        _p = int(x * 100 / length)
        if p != _p:
            p = _p
            print_progress(p)
        for y in range(width):
            point = pixs[x, y]
            ds = tuple(
                (reduce(
                    lambda l, r: l + ((cate[r] - point[r]) / 255)**2,
                    range(3), 0
                ))**0.5
                for cate in categories
            )
            c = 0
            d = 1
            for i in range(len(ds)):
                if ds[i] <= d:
                    c = i
                    d = ds[i]
            # print((x, y), categories[c])
            drawer.point((x, y), fill=categories[c])
    print_progress('OK')
    threading.Thread(target=new_image.show, name='Preview').start()
    # 描绘特征
    while True:
        line = input("\n请输入采样平方数量：（默认为100，即100的平方个点）")
        if line == '':
            step = 100
            break
        try:
            step = int(line)
        except ValueError:
            print('无效的输入，请输入一个整数')
            continue
        else:
            break
    print('\n正在计算特征向量，请稍候')
    ax = plt.figure().add_subplot(111, projection='3d')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('gray')
    points = [[], [], []]
    p = 0
    for x in range(step):
        _p = int(x * 100 / step)
        if p != _p:
            p = _p
            print_progress(p)
        for y in range(step):
            r, g, b = pixs[int(x / step * (length - 1)),
                           int(y / step * (width - 1))]
            points[0].append(r)
            points[1].append(g)
            points[2].append(b)
    print_progress('OK')
    ax.scatter(*points)
    plt.show()
if __name__ == '__main__':
    main()
