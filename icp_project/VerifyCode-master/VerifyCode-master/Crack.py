#!/usr/bin/python
# -*- coding: utf-8 -*-
import pytesseract, math, hashlib, time
import timeit, random, requests, os
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import re

Cutting = "./Cutting/"
TRAIN = './Record/'

# letters = []
iconset = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
           'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class Crack(object):

    def get_crop_site(self, img):
        """
        获取截图所需要的四个点
        :param img_name:
        :return:
        """
        letters = []
        inletter_w = False
        inletter_h = False
        foundletter_w = False
        foundletter_h = False
        start = [0, 0]
        end = [0, 0]

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix = img.getpixel((x, y))
                if pix != 255:
                    inletter_w = True
            if foundletter_w == False and inletter_w == True:
                foundletter_w = True
                start[0] = x
            if foundletter_w == True and inletter_w == False:
                foundletter_w = False
                end[0] = x
                # 如果宽度太小，则跳过
                if end[0] - start[0] < 10:
                    continue
                # 当找到最小宽度后，再找最小高度
                for h in range(img.size[1]):
                    for w in range(start[0], end[0] + 1):
                        pix = img.getpixel((w, h))
                        if pix != 255:
                            inletter_h = True
                        if foundletter_h == False and inletter_h == True:
                            foundletter_h = True
                            start[1] = h
                        if foundletter_h == True and inletter_h == False:
                            foundletter_h = False
                            end[1] = h
                    inletter_h = False
                # 如果高度小于20 则跳过
                if end[1] - start[1] < 20:
                    continue
                # 如果宽度太宽，> 50 或者 > 90
                if end[0] - start[0] > 50:
                    # 分2块切割
                    width = (end[0] - start[0]) // 2
                    letters.extend([(start, [start[0] - width, end[1]]),
                                    ([start[0] - width, start[1]], end)])
                elif end[0] - start[0] > 90:
                    # 分3块切割
                    width = (end[0] - start[0]) // 3
                    letters.extend([(start, [start[0] + width, end[1]]),
                                    ([start[0] + width, start[1]], [start[0] + 2 * width, end[1]]),
                                    ([start[0] + 2 * width, start[1]], end)])
                else:
                    letters.append((start, end))
            inletter_w = False

        return letters

    def cutting(self, img_name):
        """
        切割图片
        :param img_name:
        :return:
        """
        # global letters
        # 初始化切割字符列表
        letters = []

        img = Image.open(img_name)
        # his = img.histogram()
        # values = {}
        # for i in range(0, len(his)):
        #     values[i] = his[i]
        # temp = sorted(values.items(), key=lambda x: x[1], reverse=True)

        img.show()

        # 从上至下，从左往右遍历像素点， 确定单个字符的切割起始位置

        # 根据各个点位的起始位置截图（切割）
        # count = 0
        # for letter in letters:
        #     img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
        #     # img2.save("./test/%s.png" % (count))
        #     count += 1

        # 结果点的形势[(起始点坐标,结尾点),([x1,y1]，[x2, y2])
        letters = self.get_crop_site(img)
        imageset = self.load_train()
        return self.crack_img(img_name, imageset, letters)

    def magnitude(self, concordance):
        total = 0
        for word, count in concordance.items():
            total += count ** 2
        return math.sqrt(total)

    def relation(self, concordance1, concordance2):
        topvalue = 0
        for word, count in concordance1.items():
            if word in concordance2:
                topvalue += count * concordance2[word]
        return topvalue / (self.magnitude(concordance1) * self.magnitude(concordance2))

    def buildvector(self, im):
        """
        创建矢量
        :param im: Image.Open()对象
        :return:
        """
        d1 = {}
        count = 0
        for i in im.getdata():
            d1[count] = i
            count += 1
        return d1

    def load_train(self):
        '''
        加载训练集
        :return:list 返回各个字母的应得矢量集
        '''
        import os
        imageset = []

        imageset = []
        for letter in iconset:
            # 获取训练集里面的图片名称
            for img in os.listdir(TRAIN + '%s/' % (letter)):
                temp = []
                if img != "Thumbs.db" and img != ".DS_Store":
                    # 处理图片   结果以[{'a':[]}]的形势存入imageset里面并返回
                    temp.append(self.buildvector(Image.open(TRAIN + "/%s/%s" % (letter, img))))
                imageset.append({letter: temp})
        return imageset

    def crack_img(self, img_name, imageset, letters):
        """

        :param img_name:图片地址
        :param imageset:字母对应矢量集合
        :param letters:字母起始位置（start, end）
        :return:
        """
        # global letters
        img = Image.open(img_name)
        coutn = 0
        data = []
        for letter in letters:
            # 获取单个字符截图
            img2 = img.crop((letter[0][0], letter[0][1], letter[1][0], letter[1][1]))
            guess = []
            for image in imageset:
                # iamge = {'a': [] }格式
                for x, y in image.items():
                    if len(y) != 0:
                        # y[0]矢量与img2矢量的对比的到一个相似度，相似度越接近1 的值即为预测值
                        guess.append((self.relation(y[0], self.buildvector(img2)), x))
            #
            # 对预测结果反向排序
            guess.sort(reverse=True)
            #
            data.append(guess[0][1])
            # print(guess[0])
            coutn += 1
        print(data)

        return ''.join(data)


if __name__ == "__main__":
    C = Crack()
    print(C.cutting("./Modif/7.png"))
