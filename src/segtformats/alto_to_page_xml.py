#!/usr/bin/env python3
"""
ALTO → Page conversion tool with embedded XSL stylesheet.
"""

import sys
import re
from pathlib import Path

import fargv
from fargv import FargvPositional, FargvChoice
from . import segtformats as sgf
from . import set_logging_level, logger

if __name__ == '__main__':
    main()

def main():

    p = {
         'file_paths': FargvPositional(default=[], description="Input file (ALTO)."),
         'out': ('', "Output to filename <out>: set to 'auto' for output to filename <input stem>.<output_suffix>."),
         'input_suffix': ('.xml', "Input file suffix."),
         'output_suffix': ('.xml', "Output file suffix."),
         'overwrite_existing': (False, "Overwrite an existing output file."),
         "verbosity": FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
    }

    args, _ = fargv.parse( p )

    set_logging_level( int(args.verbosity) )

    for file_path in args.file_paths:

        if not args.out:
            sgf.alto_to_page_xml( file_path )
            continue
        
        out_path = ''
        if args.out == 'auto':
            if not re.search( r'{}$'.format(args.input_suffix), Path(file_path).name):
                logger.warning(f"Input file path '{Path(file_path).name}' does not match input suffix '{args.input_suffix}': output aborted.")
                continue
            out_path = re.sub(r'{}$'.format( args.input_suffix ), args.output_suffix, file_path )
        else:
            out_path = args.out
        logger.debug(f"Output file = {out_path}")

        if not args.overwrite_existing and Path(out_path).exists():
            logger.info("File {} exists: skipping.".format( out_path ))
            continue
        sgf.alto_to_page_xml( file_path, pagexml_filename=out_path )

    return 0
