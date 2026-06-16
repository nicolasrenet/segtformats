#!/usr/bin/env python3
"""
ALTO → Page conversion tool with embedded XSL stylesheet.
"""

import sys
import re
from pathlib import Path

from . import segtformats as sgf

USAGE=f"USAGE: {sys.argv[0]} <alto file>.xml [<PageXML output file]"

if __name__ == '__main__':

    if len(sys.argv) < 2 or re.match(r'--?h', sys.argv[1]):
        print(USAGE)
        sys.exit()

    source_file = sys.argv[1]

    if len(sys.argv)>2:
        print(f"{sys.argv[1]} → {sys.argv[2]}")
        sgf.alto_to_page_xml( source_file, pagexml_filename=sys.argv[2] )
    else:
        sgf.alto_to_page_xml( source_file )
