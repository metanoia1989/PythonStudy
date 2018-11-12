#!/usr/bin/env python3
# -*- conding:utf8 -*-

charBox = {}
punctuation = ['，', '。', '；', '：', '“', "”"]
with open('./列子.txt', 'r') as f:
    while True:
        char = f.read(1)
        if not char:
            break
        if char == '\n' or char == '\r\n' or char == '\r':
            continue
        if char in punctuation:
            continue
        if char not in charBox:
            charBox[char] = 1
        else:
            charBox[char] += 1
charBox = dict(sorted(charBox.items(), key = lambda item: item[1], reverse = True))
print(charBox)