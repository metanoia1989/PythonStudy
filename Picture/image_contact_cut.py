#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
拼接图片
"""

from PIL import Image 
from pathlib import Path
import argparse
import sys

def get_concat_h_cut(img1, img2):
    dst = Image.new('RGB', (img1.width + img2.width, min(img1.height, img2.height)))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))
    return dst

def get_concat_v_cut(img1, img2):
    dst = Image.new('RGB', ( min(img1.width, img2.width), img1.height + img2.height) )
    dst.paste(img1, (0, 0))
    dst.paste(img2, (0, img1.height))
    return dst

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="图片拼接工具")
    parser.add_argument("-d", "--direct", default="v", help="拼接方向 h or v")
    parser.add_argument("-f1", "--file1", required=True,help="要拼接的图片1")
    parser.add_argument("-f2", "--file2", required=True, help="要拼接的图片2")
    parser.add_argument("-o", "--output_file", default="ouput.png", help="输出的图片名称")
    args = parser.parse_args()

    file1 = args.file1
    file2 = args.file2
    direction = args.direct
    output_name = args.output_file
    
    if not Path(file1).exists() or not Path(file2).exists():
        print("指定的图片文件不存在")
        sys.exit(1)
        
    img1 = Image.open(file1)
    img2 = Image.open(file2)
    
    if direction == "h":
        get_concat_h_cut(img1, img2).save(output_name) 
    elif direction == "v":
        get_concat_v_cut(img1, img2).save(output_name) 
    else:
        print("无效的方向")
        sys.exit(1)
        
    