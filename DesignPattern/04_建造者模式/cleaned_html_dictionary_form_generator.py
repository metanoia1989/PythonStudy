#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
将循环和条件语句堆加在各表单内部和之上将很快变得无法阅读和不可维护
取出每个字段的生成代码的主要部分，并且将之放入一个单独的函数，
这个函数使用词典并且返回一段该字段的HTML代码。
不用修改主函数的任何功能、输入或者输出。    
"""
def generate_webform(field_dict_list):
    generated_field_list = []

    for field_dict in field_dict_list:
        if field_dict["type"] == "text_field":
            field_html = generate_text_field(field_dict)

        elif field_dict["type"] == "checkbox":
            field_html = generate_checkbox(field_dict)

    generated_fields = "\n".join(generated_field_list)
    return "<form>{fields}</form>".format(fields=generated_fields)

def generate_text_field(text_field_dict):
    return '{0}:<br><input type="text" name="{1}"><br>'.format(
        field_dict["label"],
        field_dict["name"]
    )
    
def generate_checkbox(checkbox_dict):
    return '<label><input type="checkbox" id="{0}" value="{1}">{2}<br>'.format(
        field_dict["id"],
        field_dict["value"],
        field_dict["label"]
    )

def build_html_form(field_list):
    with open("form_file.html", "w") as f:
        f.write(
            "<html><body>{}</body></html>".format(
                generate_webform(field_list)
            )
        )

if __name__ == "__main__":
    field_list = [
        {
            "type": "text_field",
            "label": "Base text you have ever written",
            "name": "best_text"
        },
        {
            "type": "checkbox",
            "id": "check_it",
            "value": "1",
            "label": "Check for one"
        },
        {
            "type": "text_field",
            "label": "Another Text field",
            "name": "text_field2"
        },
    ]
    build_html_form(field_list)