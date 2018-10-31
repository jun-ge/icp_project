#!/usr/bin/python
# coding: utf-8
import logging
import timeit, random, time, requests, os
from PIL import Image, ImageDraw
from PIL import ImageEnhance
from PIL import ImageFilter
import pytesseract
from Crack import *

GET_PATH = "./img_data/"  # 下载图片保存路径
GET_URL = ""
GET_NUMBER = 10  # 下载图片数量
EDIT_PATH = './Edit/'  # 灰度图目录
EDIT_NAME = ''  # 保存灰度图名称
MODIF = './MODIF/'  # 去掉干扰线后保存路径
VAL_IMG = 0  # 去掉干扰线后保存名称
CUTTING = './Cutting/'  # 临时保存
Iconset = './Record/'  # 数据存储
ico = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
       'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


class Img(object):
    """
    处理图片，灰度。二值化，去噪点，并切割后放入临时的./Cutting/文件下
    """
    def get_img_code(self):
        '''
        获取验证码图片
        :return: None
        '''
        get_img_start = time.time()
        if os.path.isdir(GET_PATH):
            pass
        else:
            mkdir = os.makedirs(GET_PATH)
            print('下载目录不存在，创建目录中----------')
            print('下载目录创建成功，目录名->' + GET_PATH)
        if GET_URL != '':
            print("获取下载链接成功---------")
            print("开始下载验证码")
            for i in range(0, GET_NUMBER):
                print("下载第" + str(i) + "张验证码")
                filePath = GET_PATH + str(i) + '.jpg'
                Get_img = requests.get(GET_URL)
                with open(filePath, 'bw') as f:
                    f.write(Get_img.content)
            get_img_end = time.time()
            print("已完成，共下载" + str(GET_NUMBER) + "张验证码---------")
            print("执行时间 %f m" % (get_img_end - get_img_start))

        else:
            print('验证码下载地址为空')
            exit()

    def handle_verify(self):
        '''
        获取图片并开始处理图片，灰度，二值化验证码图片
        :return:
        '''
        info_len = 0
        han_img_start = time.time()
        print('开始处理图片')
        threshold = 140
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)

        img_list = os.listdir(GET_PATH)
        print("获取图片总数，-》" + str(len(img_list)))
        if os.path.isdir(EDIT_PATH):
            pass
        else:
            mkdir = os.makedirs(EDIT_PATH)
            print('保存灰度图目录不存在，创建目录中----------')
            print('保存灰度图目录创建成功，目录名->' + EDIT_PATH)
        for i in range(0, len(img_list)):
            info_len += 1
            print("正在处理第" + str(i + 1) + '张验证码')
            ini_time = int(time.time())
            edit_img_name = random.randint(0, ini_time)

            im = Image.open(GET_PATH + img_list[i])
            imgry = im.convert('L')
            out = imgry.point(table, '1')
            EDIT_NAME = EDIT_PATH + str(edit_img_name) + '.jpg'
            # 灰度处理，二值化处理后，存放在edit目录下
            out.save(EDIT_NAME)
            # 获取生产的心图片，并处理
            self.resize_img(EDIT_NAME)
            # self.MODIFyImg(EDIT_NAME)
        han_img_end = time.time()
        print("图片转换完成，耗时 %f m， 共转换 %s 张" % (han_img_end - han_img_start, info_len))

    def modify_img(self, img_name):
        """
        修改图片，去除验证码中的线条等
        :param img_name: 图片地址
        :return:
        """

        global VAL_IMG
        # 为即将要去除干扰线的文件定名称。已1,2，3，。。数字命名
        VAL_IMG += 1
        if VAL_IMG <= 1:
            print('准备去除验证码干扰线----------')
            if os.path.isdir(MODIF):
                pass
            else:
                mkdir = os.makedirs(MODIF)
                print('保存去除验证码图片目录不存在，创建目录中----------')
                print('保存去除验证码图片目录创建成功，目录名->' + MODIF)
        else:
            pass

        img = Image.open(img_name)
        # 中值滤波滤镜处理后，使某一像素中的值更加接近该点邻域中的值
        img = img.filter(ImageFilter.MedianFilter())
        # 曾强图像的对比度，
        enhancer = ImageEnhance.Contrast(img)
        # 0.1--2表示对比度由依次增大
        img = enhancer.enhance(2)
        # 灰度公式L = 0.299 R +  0.587 G + 0.114 B
        # PIL中有九种不同模式，分别为1，L，P，RGB，RGBA，CMYK，YCbCr，I，F
        # 模式为1 时 0表示黑，255表示白色，每个像素8bit
        img = img.convert('1')

        width, height = img.size
        data = []
        # 遍历像素，获取[[0,1,0,1,0],[],[],[]]类似的二维数组，白色标记为1，黑色标记为0
        for i in range(height):
            tmp = []
            for j in range(width):
                if (img.getpixel((j, i)) == 255):
                    tmp.append(1)
                else:
                    tmp.append(0)
            data.append(tmp)
        # 创建一张图片P，尺寸为img.size, color=255白色
        img2 = Image.new("P", img.size, 255)
        for y in range(height):
            # data
            for a in range(len(data[y])):
                o = y + 1
                t = y + 2
                # s = y+3
                z = a + 1
                x = a + 2
                try:
                    # 判断该像素点周围的像素点对应的值，如果，都是0则设置为1
                    # 可以增加这个判断and data[s][a] == 0条件
                    if data[o][a] == 0 and data[t][a] == 0 and data[y][z] == 0 and data[y][x] == 0:
                        # and data[s][a] == 0
                        # 设置像素点的值为1
                        img2.putpixel((a, y), 1)
                        # 以数字为文件名保存
                        img2.save(MODIF + str(VAL_IMG) + '.png')
                except Exception as e:
                    logging.info(' setting pixel, or save file:', e)
                    pass
        img2_path = MODIF + str(VAL_IMG) + '.png'
        # 打开保存的文件
        image = Image.open(img2_path)
        # 灰度处理
        image = image.convert("L")
        # 去除噪点53：像素参照值，4：比参照值小的个数的阀值
        self.clearNoise(image, 53, 4, 8)
        # 保存文件（覆盖）
        image.save(img2_path)
        # image.show()
        # 切割文件
        self.img_cutting(img2_path)

    def img_cutting(self, img_name):
        global VAL_IMG
        if VAL_IMG <= 1:
            if os.path.isdir(CUTTING):
                pass
            else:
                mkdir = os.makedirs(CUTTING)
                print('临时保存目录不存在，创建目录中----------')
                print('临时保存图目录创建成功，目录名->' + CUTTING)

        inletter = False
        foundletter = False
        start = 0
        end = 0
        # 字母列表集
        letters = []

        # 打开 灰度，和二值化处理的图片
        img = Image.open(img_name)

        # 创建灰度直方图
        his = img.histogram()
        values = {}
        for i in range(0, len(his)):
            values[i] = his[i]
        temp = sorted(values.items(), key=lambda x: x[1], reverse=True)

        # 获取每个点的像素值，至上而下，从左往右，最小宽度切割，
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pix = img.getpixel((x, y))
                # 找到第一个像素值不为255的点，
                if pix != 255:
                    inletter = True
                    break
            if foundletter == False and inletter == True:
                foundletter = True
                # 保存起始位置
                start = x
            # 如果没有很黑的，保存结束点
            if foundletter == True and inletter == False:
                foundletter = False
                end = x
                # 记录，图片某一个字母左右切割的范围
                letters.append((start, end))

            inletter = False

        for letter in letters:
            ini_time = int(time.time())
            code_img_name = random.randint(0, ini_time)
            # 截图，（起始点的横坐标，起始点的纵坐标，宽度，高度）
            img2 = img.crop((letter[0], 0, letter[1], img.size[1]))
            save_path = CUTTING + str(code_img_name) + '.png'
            # 将截图保存下来
            img2.save(save_path)

    def resize_img(self, img_path):
        '''
        重新处理图片的尺寸，设置图片地产宽度280，高度根据原始图片等比例缩放
        :param img_path: 图片地址
        :return:
        '''
        img = Image.open(img_path)
        width, height = img.size
        new_width = 280
        new_height = int(height * new_width / width)
        # 等b比例重新定义图片大小
        out = img.resize((new_width, new_height), Image.ANTIALIAS)
        # 获取文件拓展名
        ext = os.path.splitext(img_path)[1]
        out.save(img_path, quality=95)
        # 转变图片
        self.modify_img(img_path)

    def get_pixel(self, image, x, y, G, N):
        '''
        获取目标点的像素值G=53，N=4
        :param image:
        :param x:
        :param y:
        :param G：
        :param N:用来判断目标周围点的像素小于G的个数的阀值
        :return:
        '''
        L = image.getpixel((x, y))
        if L > G:
            L = True
        else:
            L = False

        nearDots = 0
        # 目标点周围8邻域，判断
        if L == (image.getpixel((x - 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x - 1, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x, y + 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y - 1)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y)) > G):
            nearDots += 1
        if L == (image.getpixel((x + 1, y + 1)) > G):
            nearDots += 1

        if nearDots < N:
            # 若是小与阀值N，则将目标上方点返回出去
            return image.getpixel((x, y - 1))
        else:
            return None

    def clearNoise(self, image, G, N, Z):

        '''
        清除噪点 self.clearNoise(image, 53, 4, 8)
        :param image:
        :param G:
        :param N:
        :param Z:
        :return:
        '''
        # 创建绘图工具
        draw = ImageDraw.Draw(image)
        for i in range(0, Z):
            for x in range(1, image.size[0] - 1):
                for y in range(1, image.size[1] - 1):
                    # 获取图像image（x, y）的颜色像素值0-255，
                    color = self.get_pixel(image, x, y, G, N)
                    if color != None:
                        #描点
                        draw.point((x, y), color)

    def class_dir(self):
        for j in range(len(ico)):
            file_name = Iconset + str(ico[j])
            os.mkdir(file_name)


if __name__ == '__main__':
    img = Img()
    # Img.get_img_code()
    img.handle_verify()
    # Img.class_dir()
