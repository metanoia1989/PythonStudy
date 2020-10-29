#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pikepdf
from pathlib import Path

pdf_path = Path("./pdf")
pdfs = [ x.absolute() for x in pdf_path.iterdir() if x.is_file()]
for path in pdfs:
    with pikepdf.open(path) as f:
        new_name = path.stem + "_unlock" + path.suffix
        f.save(new_name)