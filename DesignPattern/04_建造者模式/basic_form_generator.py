#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def generate_webform(field_list):
    """
    生成表单的函数
    """
    generate_fields = "\n".join(
        map(
            lambda x: '{0}:<br><input type="text" name="{0}"/><br>'.format(x),
            field_list
        )
    )
    return "<form>{fields}</form>".format(fields=generate_fields)

if __name__ == "__main__":
    fields = ["name", "age", "email", "telephone"]
    print(generate_webform(fields))
