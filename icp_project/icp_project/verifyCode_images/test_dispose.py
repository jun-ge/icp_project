import os
import random
import time

import numpy
from PIL import Image
import pytesseract
import cv2


# 选定阀值，二值化
def get_assign_binary_iamge(image, threshold=160):
    # image = Image.open(file_path)

    # 转化到灰度图片
    image.save('new_' + str(int(time.time())) + str(random.randint(10, 99)) + '.png')
    image = image.convert('L')
    # 二值化
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    image = image.point(table, '1')
    return image


# 简单图像验证码转str
def img_dispose_to_str(image):
    """

    :param image: 图片对象
    :return:
    """
    return pytesseract.image_to_string(image,
                                       config='--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"')


class ImageDispose:
    def __init__(self, im, file_path=None):
        self.file_path = file_path
        # 读取文件，并灰值化
        im = get_assign_binary_iamge(im, threshold=200)
        if file_path:
            temp_path = file_path.replace('\\', '\\temp_')
            im = Image.open(file_path)
        else:
            temp_path = 'temp_' + str(int(time.time())) + str(random.randint(100, 999)) + '.jpg'
            im = get_assign_binary_iamge(im, threshold=200)
        im.save(temp_path)
        self._im = cv2.cvtColor(cv2.imread(temp_path), cv2.COLOR_BGR2GRAY)
        # os.remove(temp_path)
        # opnCv 矩阵图点x. y是反的
        self._height, self._width = self._im.shape[:2]

    def save(self, output_path, im):
        """
        保存文件
        :param output_path: 输出路径
        :param im: 图片对象
        :return:
        """
        cv2.imwrite(output_path, im)

    def get_adaptive_binary_image(self):
        """
        自适应阀值，二值化
        :return:
        """
        self._im = cv2.adaptiveThreshold(self._im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)

    def clear_border(self, border_width=2):
        """
        去除图像的边框,默认像素宽度border_width=2
        :return:
        """
        for y in range(self._width):
            for x in range(self._height):
                if y < border_width or y > self._width - border_width:
                    self._im[x, y] = 255
                if x < border_width or x > self._height - border_width:
                    self._im[x, y] = 255

    def clear_interference_line1(self, threshold=245):
        """
        干扰线降噪，颜色阀值threshold=245,判断标准：目标周围上下左右4邻域
        :return:
        """
        for y in range(1, self._width - 1):
            for x in range(1, self._height - 1):
                count = 0

                if self._im[x, y - 1] > threshold:
                    count += 1
                if self._im[x - 1, y - 1] > threshold:
                    count += 1
                if self._im[x - 1, y + 1] > threshold:
                    count += 1
                if self._im[x + 1, y + 1] > threshold:
                    count += 1
                if self._im[x + 1, y - 1] > threshold:
                    count += 1
                if self._im[x, y + 1] > threshold:
                    count += 1
                if self._im[x - 1, y] > threshold:
                    count += 1
                if self._im[x + 1, y] > threshold:
                    count += 1
                #    若是白点数量大于6，则将目标点变白
                if count > 5:
                    self._im[x, y] = 255

    def clear_interference_line2(self, threshold=245):
        """
        干扰线降噪，颜色阀值threshold=245,判断标准：目标周围上下左右4邻域
        :return:
        """
        for y in range(2, self._width - 2):
            for x in range(2, self._height - 2):
                count = 0
                # 处理 25格区域内的情况
                # '''内圈8格'''

                if self._im[x, y - 1] > threshold:
                    count += 1
                if self._im[x - 1, y - 1] > threshold:
                    count += 1
                if self._im[x - 1, y + 1] > threshold:
                    count += 1
                if self._im[x + 1, y + 1] > threshold:
                    count += 1
                if self._im[x + 1, y - 1] > threshold:
                    count += 1
                if self._im[x, y + 1] > threshold:
                    count += 1
                if self._im[x - 1, y] > threshold:
                    count += 1
                if self._im[x + 1, y] > threshold:
                    count += 1
                # 外圈16格
                if self._im[x - 2, y - 2] > threshold:
                    count += 1
                if self._im[x - 1, y - 2] > threshold:
                    count += 1
                if self._im[x, y - 2] > threshold:
                    count += 1
                if self._im[x + 1, y - 2] > threshold:
                    count += 1
                if self._im[x + 2, y - 2] > threshold:
                    count += 1
                if self._im[x - 2, y - 1] > threshold:
                    count += 1
                if self._im[x - 2, y] > threshold:
                    count += 1
                if self._im[x - 2, y + 1] > threshold:
                    count += 1
                if self._im[x + 2, y - 1] > threshold:
                    count += 1
                if self._im[x + 2, y] > threshold:
                    count += 1
                if self._im[x + 2, y + 1] > threshold:
                    count += 1
                if self._im[x - 2, y + 2] > threshold:
                    count += 1
                if self._im[x + 1, y + 2] > threshold:
                    count += 1
                if self._im[x, y + 2] > threshold:
                    count += 1
                if self._im[x - 1, y + 2] > threshold:
                    count += 1
                if self._im[x - 2, y + 2] > threshold:
                    count += 1
                if count > 14:
                    self._im[x, y] = 255

    def clear_interference_line3(self, threshold=245):
        for y in range(1, self._width - 3):
            for x in range(1, self._height - 3):
                if self._im[x, y] > threshold:
                    continue
                if self._im[x + 2, y] > threshold and self._im[x - 1, y] > threshold or \
                        self._im[x, y + 2] > threshold and self._im[x, y - 1] > threshold:
                    self._im[x, y] = 255

    def clear_interference_point(self, threshold=245):
        """
        干扰点降噪，目标周围3， 5，8三种情况的邻域判断
        :param threshold: 颜色阀值255为最大阀值白色，
        :return:
        """
        for y in range(self._width - 1):
            for x in range(self._height - 1):
                if self._im[x, y] > threshold:
                    continue
                # 最上
                if y == 0:
                    # 左上顶点，4域
                    if x == 0:
                        if int(self._im[x, y]) + int(self._im[x + 1, y]) + int(self._im[x + 1, y + 1]) + int(
                                self._im[x, y + 1]) > 2 * threshold:
                            self._im[x, y] = 255
                    # 右上顶点， 4域
                    elif x == self._height - 1:
                        if int(self._im[x, y]) + int(self._im[x - 1, y]) + int(self._im[x - 1, y + 1]) + int(
                                self._im[x, y + 1]) > 2 * threshold:
                            self._im[x, y] = 255
                    # 最上非顶点，6域
                    else:
                        if int(self._im[x, y]) + int(self._im[x - 1, y]) + int(self._im[x - 1, y + 1]) + int(
                                self._im[x, y + 1]) + int(self._im[x + 1, y + 1]) + int(
                            self._im[x + 1, y]) > 3 * threshold:
                            self._im[x, y] = 255
                # 最下
                elif y == self._width - 1:
                    # 左下顶点， 4域
                    if x == 0:
                        if int(self._im[x, y]) + int(self._im[x + 1, y]) + int(self._im[x + 1, y - 1]) + int(
                                self._im[x, y - 1]) > 2 * threshold:
                            self._im[x, y] = 255
                    # 右下顶点 4域
                    elif x == self._height - 1:
                        if int(self._im[x, y]) + int(self._im[x - 1, y]) + int(self._im[x - 1, y - 1]) + int(
                                self._im[x, y - 1]) > 2 * threshold:
                            self._im[x, y] = 255
                    # 最下非顶点 6域
                    else:
                        if int(self._im[x, y]) + int(self._im[x - 1, y]) + int(self._im[x - 1, y - 1]) + int(
                                self._im[x, y - 1]) + int(self._im[x + 1, y - 1]) + int(
                            self._im[x + 1, y]) > 3 * threshold:
                            self._im[x, y] = 255
                # 其他
                else:
                    # 最左非顶点 6域
                    if x == 0:
                        if int(self._im[x, y]) + int(self._im[x, y - 1]) + int(self._im[x + 1, y - 1]) + int(
                                self._im[x + 1, y]) + int(self._im[x + 1, y + 1]) + int(
                            self._im[x, y + 1]) > 3 * threshold:
                            self._im[x, y] = 255
                    # 最右 非顶点 6域
                    elif x == self._height - 1:
                        if int(self._im[x, y]) + int(self._im[x, y - 1]) + int(self._im[x - 1, y - 1]) + int(
                                self._im[x - 1, y]) + int(self._im[x - 1, y + 1]) + int(
                            self._im[x, y + 1]) > 3 * threshold:
                            self._im[x, y] = 255
                    # 非边界点 9域
                    else:
                        if int(self._im[x, y]) + int(self._im[x - 1, y - 1]) + int(self._im[x, y - 1]) + int(
                                self._im[x + 1, y - 1]) + int(self._im[x - 1, y]) + int(self._im[x + 1, y]) + int(
                            self._im[x - 1, y + 1]) + int(self._im[x, y + 1]) + int(
                            self._im[x + 1, y + 1]) > 5 * threshold:
                            self._im[x, y] = 255

    def dispose(self, border=False, line=True, point=True):
        if border:
            self.clear_border()
        if line:
            # self.clear_interference_line2()

            # cv2.imshow('Image',self._im)
            self.clear_interference_line3()
            self.clear_interference_line1()
            # cv2.imshow('Image', self._im)
            cv2.imwrite('result_' + str(int(time.time())) + str(random.randint(100, 999)) + '.jpeg', self._im)
        if point:
            self.clear_interference_point()
            # cv2.imshow('Image', self._im)

        cv2.imwrite('dispose_ima.jpg', self._im)
        tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'
        try:
            result = pytesseract.image_to_string('dispose_ima.jpg', config=tessdata_dir_config).replace(' ',
                                                                                                        '').replace(
                '“', '').replace('(', "").replace(')', '').replace(',', "").replace('\'', '').replace('.', '').replace(
                '’', '').replace('‘', '').replace('”', '').replace(':', '').replace('\"', '')
            os.remove('dispose_ima.jpg')
        except Exception as e:
            print('image_to_string:', e)
        print(result)
        return result


if __name__ == '__main__':
    pass
