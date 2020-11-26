#!/usr/bin/env python3
#-*- coding: utf-8 -*-

'''
没有用=_=
'''
import sys
from pathlib import Path
import numpy as np


target_locations = np.array([
    [0.70711, 0.70711, -0.70711, 0.70711, -308.753, -165.279],
    [1, 0, 0, 1, -44.831, 54.605]])


def match_location(location, target, epsilon=1e-5):
    # targe must be n*6 numpy matrix
    return np.any(np.abs(np.array([i.as_numeric() for i in location]) - target).max(axis=1) < epsilon)


def remove_watermark(wm_text, inputFile, outputFile):
    from PyPDF4 import PdfFileReader, PdfFileWriter
    from PyPDF4.pdf import ContentStream
    from PyPDF4.generic import TextStringObject, NameObject
    from PyPDF4.utils import b_
    
    with open(inputFile, "rb") as f:
        source = PdfFileReader(f, "rb")
        output = PdfFileWriter()

        print("水印内容为：", wm_text)

        for page in range(source.getNumPages()):
            page = source.getPage(page)
            content_object = page["/Contents"].getObject()
            content = ContentStream(content_object, source)
            for operands, operator in content.operations:
                # if operator == b_("Tj"):
                #     text = operands[0][0]
                #     if isinstance(text, TextStringObject) and text.startswith(wm_text):
                #         operands[0] = TextStringObject('')
                        
                if operator == b_("cm") and match_location(operands, target_locations):
                    operands[:] = []


            page.__setitem__(NameObject('/Contents'), content)
            output.addPage(page)

        with open(outputFile, "wb") as outputStream:
            output.write(outputStream)
            
if __name__ == "__main__":
    """ 
    命令行参数 第一个参数文件名 第二个参数文字水印内容
    """ 
    argc = len(sys.argv)
    if argc < 3 or argc > 3:
        print("必须输入文件名以及水印内容，不能输入更多的内容")
        sys.exit()

    filename = sys.argv[1] 
    wm_text = sys.argv[2]
    if not Path(filename).exists():
        print("输入的文件不存在")
        sys.exit()
        
    wm_text = "soso"

    inputFile = filename
    outputFile = r"output.pdf"
    remove_watermark(wm_text, inputFile, outputFile)
