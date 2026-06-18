#!/usr/bin/env python3
"""
ALTO → Page conversion tool with embedded XSL stylesheet.
"""

import sys
import re
from pathlib import Path

import fargv
from fargv import FargvPositional
from . import segtformats as sgf
from . import set_logging_level, logger

if __name__ == '__main__':
    main()

def main():

    p = {
         'file_paths': FargvPositional(default=[], description="Input file (ALTO)."),
         'input_suffix': ('.xml', "Input file suffix."),
         'output_suffix': ('', "Output file suffix; if empty, write on standard output"),
         'overwrite_existing': (False, "Overwrite an existing output file."),
         'verbosity': (2,"Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
    }

    args, _ = fargv.parse( p )

    set_logging_level( args.verbosity )

    for file_path in args.file_paths:

        if not args.output_suffix:
            sgf.alto_to_page_xml( file_path )
        else:
            output_filename = re.sub(r'{}$'.format( args.input_suffix ), args.output_suffix, file_path )
            if overwrite_existing or not Path( output_filename ).exists():
                sgf.alto_to_page_xml( file_path, pagexml_filename=output_filename )

    return 0
