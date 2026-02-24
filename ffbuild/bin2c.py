#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2023 L. E. Segovia <amy@centricular.com>
# SPDX-License-Identifier: BSD-3-Clause

from argparse import ArgumentParser
from io import StringIO
import os
from pathlib import Path
import re
import shutil

if __name__ == '__main__':
    parser = ArgumentParser(description='Converts a blob into a C array')
    parser.add_argument('input', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('name', nargs='?')

    args = parser.parse_args()

    input = args.input
    output = args.output
    name = args.name

    if args.name is None:
        name = re.sub(r'[^a-zA-Z0-9]', '_', output.stem)

    tmp = StringIO()

    with input.open('rb') as i:
        length = os.path.getsize(input)
        tmp.write(f"const unsigned char ff_{name}_data[] = {{")
        while (byte := i.read(1)):
            tmp.write(f"0x{byte.hex()}, ")
        tmp.write("0x00 };\n")
        tmp.write(f"const unsigned int ff_{name}_len = {length};\n")

    tmp.seek(0)
    shutil.copyfileobj(tmp, output.open('w', encoding='utf-8'), -1)
