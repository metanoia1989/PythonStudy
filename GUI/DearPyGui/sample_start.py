#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from dearpygui import dearpygui

dearpygui.add_text("Hello World")
dearpygui.add_button("Save", callback="SaveCallback")
dearpygui.add_input_text("string")
dearpygui.add_slider_float("float")

def SaveCallback(sender, data):
    print("Save Clicked")

dearpygui.start_dearpygui()