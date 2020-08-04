#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def generate_webform(fields_list):
    generated_fields = "\n".join(
        map(
            lambda x: '{0}:<br><input type="text" name="{0}"><br>'.format(x),
            fields_list
        )
    )
    return "<form>{fields}</form>".format(fields=generated_fields)

def build_html_form(fields):
    with open("form_file.html", 'w') as f:
        f.write(
            "<html><body>{}</body></html>".format(generate_webform(fields))
        )

if __name__ == "__main__":
    fields = ["name", "age", "email", "telephone"]
    build_html_form(fields)

