#!/usr/bin/python
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

"""
GaussBayesPicSort - GUI
@author: zhengxiaoyao0716
"""

from functools import reduce
from tkinter import Tk, Label, Frame, Entry, Button, Canvas, filedialog, simpledialog, END

from PIL import Image, ImageTk, ImageDraw
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D as _


def choose_pic(root):
    """选择图片"""
    frame = Frame(root)
    frame.pack(padx=10, pady=10)
    Label(frame, text='图片路径：').pack(side='left')
    in_entry = Entry(frame, width='30')
    in_entry.pack(side='left')
    in_entry.insert(0, './assets/生活照-武.jpg')

    def load_pic(path):
        """载入图片"""
        try:
            image = Image.open(path)
        except IOError:
            return
        frame.destroy()
        choose_cate_points(root, image)
    in_entry.bind('<Return>', lambda e: load_pic(in_entry.get()))

    def choose_file():
        """选择文件"""
        path = filedialog.askopenfilename(title='打开图片',
                                          filetypes=[
                                              ('Image', '*.jpg *.png *.bmp'),
                                              ('All Files', '*'),
                                          ])
        if path != '':
            in_entry.delete(0, END)
            in_entry.insert(0, path)
    Button(frame, text='浏览', command=choose_file).pack(side='left')
    Button(
        frame,
        text='下一步',
        command=lambda: load_pic(in_entry.get())
    ).pack(side='right')


def choose_cate_points(root, image):
    """选择分类基准"""
    frame = Frame(root)
    frame.pack(padx=6, pady=6)
    factor = min(800 / image.size[0], 600 / image.size[1])
    raw_image = image
    image = image.resize(
        (int(image.size[0] * factor), int(image.size[1] * factor)))
    canvas = Canvas(frame, width=image.size[0], height=image.size[1])
    canvas.pack(side='left')
    canvas.image = ImageTk.PhotoImage(image)
    canvas.create_image(image.size[0] / 2,
                        image.size[1] / 2,
                        image=canvas.image)
    rframe = Frame(frame)
    rframe.pack()
    Label(rframe, text='已选择的分类基准点：').pack(side='top')
    cate_points = []

    def add_point(point, pos):
        """添加新的点"""
        if pos:
            x, y = pos
        else:
            x, y = (point[0] * image.size[0], point[1] * image.size[1])
        canvas.create_oval(x - 6, y - 6, x + 6, y + 6)
        cate_points.append(point)
        index = len(cate_points)
        if index == 2:
            def next_step():
                """下一步"""
                if 'ids' in dir(show_coords):
                    for id in show_coords.ids:
                        canvas.delete(id)
                canvas.unbind('<Motion>')
                canvas.unbind('<Button-1>')
                rframe.destroy()
                length, width = raw_image.size
                pixs = raw_image.load()
                categories = []
                for x, y in cate_points:
                    categories.append(pixs[x * (length - 1), y * (width - 1)])
                sort_pic(frame,
                         Image.new('RGB', raw_image.size, (255, 255, 255)),
                         pixs, categories, factor, canvas)
            Button(rframe, text='下一步', command=next_step).pack(side='bottom')
        canvas.create_text(x, y, text=str(index))
        Label(
            rframe,
            text='%d: %f, %f' % (index, point[0], point[1])
        ).pack(side='top')

    def show_coords(x, y, choose=False):
        """显示坐标"""
        point = (x / image.size[0], y / image.size[1])
        if reduce(lambda l, r: True if r < 0 or r > 1 else l, point, False):
            return
        if 'ids' in dir(show_coords):
            for id in show_coords.ids:
                canvas.delete(id)
        show_coords.ids = (
            canvas.create_text(
                x + 40 if x < image.size[0] - 80 else x - 30,
                y + 10 if y < image.size[1] - 20 else y - 10,
                text='(%f, %f)' % point
            ),
            canvas.create_line(0, y, image.size[0], y),
            canvas.create_line(x, 0, x, image.size[1]),
        )
        if choose:
            add_point(point, (x, y))
        canvas.update()
    canvas.bind('<Motion>', lambda e: show_coords(e.x, e.y))
    canvas.bind('<Button-1>', lambda e: show_coords(e.x, e.y, True))


def sort_pic(root, image, pixs, categories, factor, raw_canvas):
    """分类图片"""
    length, width = image.size
    drawer = ImageDraw.Draw(image)
    _image = image.resize(
        (int(image.size[0] * factor), int(image.size[1] * factor)))
    canvas = Canvas(root, width=_image.size[0], height=_image.size[1])
    canvas.pack(side='left')
    canvas.image = ImageTk.PhotoImage(_image)
    image_tk_id = canvas.create_image(_image.size[0] / 2,
                                      _image.size[1] / 2,
                                      image=canvas.image)
    p = 0
    for x in range(length):
        _p = int(x * 100 / length)
        if p != _p:
            p = _p
            canvas.delete(image_tk_id)
            _image = image.resize(
                (int(image.size[0] * factor), int(image.size[1] * factor)))
            canvas.image = ImageTk.PhotoImage(_image)
            image_tk_id = canvas.create_image(_image.size[0] / 2,
                                              _image.size[1] / 2,
                                              image=canvas.image)
            canvas.update()
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
            drawer.point((x, y), fill=categories[c])
    canvas.delete(image_tk_id)
    _image = image.resize(
        (int(image.size[0] * factor), int(image.size[1] * factor)))
    canvas.image = ImageTk.PhotoImage(_image)
    image_tk_id = canvas.create_image(_image.size[0] / 2,
                                      _image.size[1] / 2,
                                      image=canvas.image)
    canvas.update()
    analyze(raw_canvas, pixs, length, width)


def analyze(canvas, pixs, length, width):
    """分析图片"""
    step = simpledialog.askinteger(
        '请输入采样平方数量', '默认为100，即100的平方个点', initialvalue=100)
    ax = plt.figure().add_subplot(111, projection='3d')
    ax.set_xlabel('R')
    ax.set_ylabel('G')
    ax.set_zlabel('B')
    points = [[], [], []]
    line_id = canvas.create_line(0, 0, 0, width)
    for x in range(step):
        canvas.delete(line_id)
        p = x * length / step
        line_id = canvas.create_line(p, 0, p, width)
        canvas.update()
        for y in range(step):
            r, g, b = pixs[int(x / step * (length - 1)),
                           int(y / step * (width - 1))]
            points[0].append(r)
            points[1].append(g)
            points[2].append(b)
    canvas.delete(line_id)
    ax.scatter(*points)
    plt.show()


def main():
    """Entrypoint"""
    root = Tk()
    root.title('GaussBayesPicSort')
    choose_pic(root)
    root.mainloop()
if __name__ == '__main__':
    main()
