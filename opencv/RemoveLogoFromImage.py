import logging
import os

import cv2
import traceback

"""
配色单一的水印图片，直接将水印颜色填充替换为白色，从而实现水印的快速去除
project interpreter,添加opencv-python和opencv-contrib-python

"""
color_list = set(list())
try:
    # 读取图片

    img = cv2.imread('/Users/wucysh/Desktop/Tengern/Python/PyCat/com/pycat/opencv/images/source_code_logo_no_back.png', -1)  # 读取透明度
    # 获取图片大小
    x, y, z = img.shape
    for i in range(x):
        for j in range(y):
            varP = img[i, j]
            # print(sum(varP) - 700, end=',')
            # if varP[0] != 0 and varP[1] != 0 and varP[2] != 0:
            # color_list.add(''.join([str(hex(varP[0])).replace('0x',''), str(hex(varP[1]).replace('0x','')), str(hex(varP[2]).replace('0x',''))]))
            # color_list.add(','.join([str(varP[0]), str(varP[1]), str(varP[2])]))

            # 白色范围进行颜色统一
            if sum(varP) > 600:
                img[i, j] = [255, 255, 255, 0]

            # 蓝色 范围 进行颜色统一
            if 150 + 255 < sum(varP) < 180 + 255:
                color_list.add(','.join([str(varP[0]), str(varP[1]), str(varP[2])]))
                img[i, j] = [80, 60, 20, 255]
                # img[i, j] = [255, 60, 20, 255]

        # print('')
    cv2.imwrite('zmister_qushuiyin.png', img)

    # for varP in color_list:
    #     print(varP)
except Exception as e:
    logging.exception(e)
