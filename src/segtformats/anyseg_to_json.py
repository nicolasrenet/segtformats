#!/usr/bin/env python3
#
# Convert segmentation meta-data:
#  [ Alto, Page ] → JSON
#
#

import sys
from pathlib import Path
import json
import re

import fargv
from fargv import FargvChoice, FargvPositional

from . import segtformats as sgf
from . import set_logging_level, logger


if __name__ == '__main__':
    main()

def main():

    p = {
        "file_paths": FargvPositional(default=[], description="A JSON line segmentation file (e.g <prefix>.lines.pred.json)."),
        'out': FargvChoice(['','auto'], description="Set to 'auto' for output to filename <input stem>.<output_suffix>; leave empty for standard output."),
        'output_suffix': '.json',
        "input_suffix": ('',"If empty, input file's suffix is determined by detected input format (.json or .xml)"),
        "overwrite_existing": (False, "Do not overwrite existing output file"),
        "repair": (False, "If True, fix semantic errors in the segmentation (line-to-region assignment, region boundaries)."),
        "validate": False,
        "output_format": FargvChoice(['json', 'stdout'], description="Output format"),
        "verbosity": FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"), 
    }

    args, _ = fargv.parse( p )
    
    set_logging_level( int(args.verbosity) )

    format_to_suffix = { sgf.SegFormat.PAGE: '.xml', sgf.SegFormat.ALTO: '.xml', sgf.SegFormat.JSON: '.json' }
    for file_path in args.file_paths:

        status_string=f"{file_path}: "

        segdict, _ = sgf.anyseg_to_dict( file_path )
        if not segdict:
            logger.info( status_string + '____' )
            continue
        status_string += 'C'

        if args.repair:
            segdict = sgf.json_doctor( segdict )
            status_string += 'R'

        if args.validate:
            if not sgf.json_validate( segdict ):
                logger.info( status_string + '__' )
                continue
            status_string += 'V'

        segdict_str = json.dumps( segdict, indent=2 )

        if not args.out:
            print( segdict_str )
            continue

        out_path = ''
        if args.out == 'auto':
            if not re.search( r'{}$'.format(args.input_suffix), Path(file_path).name):
                logger.warning(f"Input file path '{Path(file_path).name}' does not match input suffix '{args.input_suffix}': output aborted.")
                continue
            out_path = Path(re.sub(r'{}$'.format( args.input_suffix ), args.output_suffix, file_path )) 
        logger.debug(f"Output file = {out_path}")


        if not args.overwrite_existing and Path(out_path).exists():
            logger.info( status_string + "_ (file exists)".format( out_path ))
            continue
        with open(out_path, 'w') as json_outf:
            json_outf.write( segdict_str )
            logger.info( status_string + f"W → {json_path}")

    return 0
