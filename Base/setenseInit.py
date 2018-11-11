#!/usr/bin/env python3
# -*- conding:utf8 -*-

# 以正确的宽度在居中的 “盒子” 内打印一个句子

sentence = input("Sentence: ")

screen_width = 80
text_width = len(sentence) 
box_width = text_width + 6
left_margin = (screen_width - box_width) // 2

print("\n")
print(" " * left_margin + "+" + "-" * (box_width - 2) + "+")
print(" " * left_margin + "| " + " " * text_width + "|")
print(" " * left_margin + "| " + sentence + "|")
print(" " * left_margin + "| " + " " * text_width + "|")
print(" " * left_margin + "+" + "-" * (box_width - 2) + "+")
print("\n")