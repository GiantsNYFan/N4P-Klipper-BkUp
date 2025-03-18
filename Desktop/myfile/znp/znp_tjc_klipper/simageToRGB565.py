import sys
import numpy as np
from PIL import Image, ImageOps
from io import BytesIO
import ctypes
import time
import base64
import os

def simage_to_base64(simage_data,thumb_path):
    if os.path.exists(thumb_path):
        print(f"缩略图{thumb_path}已存在")
    else:
        with open(simage_data,'r+') as fs:
            simage = fs.read()
        with open(thumb_path, "wb") as f:                       ##"with"语句用于自动管理文件的打开和关闭
            f.write(base64.b64decode(simage.encode()))
        print(f"输出缩略图{thumb_path}完毕")

def convert_to_rgb565(so_path, image_path, tjc_path, size=200):
    image = Image.open(image_path)
    ratio_image = resize_to_square(image, size)
    ratio_image = ratio_image.convert("RGB")
    mks_lib = ctypes.CDLL(so_path)
    pixel_values = np.array(ratio_image.getdata(), dtype=np.uint16)
    r = (pixel_values[:, 0] >> 3) & 0x1F
    g = (pixel_values[:, 1] >> 2) & 0x3F
    b = (pixel_values[:, 2] >> 3) & 0x1F

    rgb565_pixel_values = (r << 11) | (g << 5) | b

    rgb16_data = rgb565_pixel_values.flatten().astype(np.uint16).tobytes()
    
    # 调用外部函数处理RGB16数据
    outputdata = bytearray(ratio_image.size[0] * ratio_image.size[1] * 10)
    outputdata_buffer = ctypes.create_string_buffer(len(outputdata))
    outputdata_buffer.raw = outputdata
    outputdata_ptr = ctypes.cast(outputdata_buffer, ctypes.POINTER(ctypes.c_char))
    mks_lib.ColPic_EncodeStr(rgb16_data, ratio_image.size[0], ratio_image.size[1], outputdata_ptr, ratio_image.size[0] * ratio_image.size[1] * 10, 1024)
    
    # 写入输出文件
    with open(tjc_path, 'w') as tjc:
      tjc.write(outputdata_buffer.raw.decode('utf-8').rstrip('\x00'))

def resize_to_square(image, size):
    width, height = image.size
    if width > height:
        ratio = size / width
    else:
        ratio = size / height

    if ratio > 1:
        ratio = 1
    
    new_width = int(width * ratio)
    new_height = int(height * ratio)

    resized_image = image.resize((new_width, new_height))

    square_image = Image.new('RGB', (size, size), (0, 0, 0))

    # 计算在正方形图像中居中的起始位置
    # x = (size - new_width) // 2
    # y = (size - new_height) // 2

    # square_image.paste(resized_image, (x, y))
    # square_image.show()
    square_image = ImageOps.pad(resized_image, (size, size))
    return square_image

# 从命令行获取参数
if len(sys.argv) < 6:
    print("请提供simage数据路径、缩略图输出路径、文件输出路径、输出尺寸、so库路径作为命令行参数")
else:
    start_time = time.time()

    image_data = sys.argv[1]
    out_thumb_path = sys.argv[2]
    tjc_path = sys.argv[3]
    simage_size = sys.argv[4]
    so_path = sys.argv[5]
    # print(f"参数1 image_data 是 {sys.argv[1]}\n参数2 out_thumb_path 是 {sys.argv[2]}\n参数3 tjc_path 是 {sys.argv[3]}\n参数4 simage_size 是 {sys.argv[4]}\n参数5 so_path 是 {sys.argv[5]}")
    try:
        size = int(simage_size)
    except ValueError:
        size = 200
    
    simage_to_base64(image_data,out_thumb_path)
    convert_to_rgb565(so_path, out_thumb_path, tjc_path, size)
    end_time = time.time()
    run_time = end_time - start_time
    print("转化完毕,程序运行时间 {run_time}", run_time, "秒")

