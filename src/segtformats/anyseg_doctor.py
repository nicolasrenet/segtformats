#!/usr/bin/env python3
#
# Repair segmentation meta-data:
#  [ Alto, Page ] → [ JSON, Page ]
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
        'out': ('', "Output to filename <out>: set to 'auto' for output to filename <input stem>.<output_suffix>."),
        "output_suffix": ('',"If empty, output file's suffix is determined by output format (.json or .xml)"),
        "input_suffix": ('',"If empty, input file's suffix is determined by detected input format (.json or .xml)"),
        "overwrite_existing": (False, "Do not overwrite existing output file"),
        "repair": (False, "If True, fix semantic errors in the segmentation (line-to-region assignment, region boundaries)."),
        "diagnose": (True, "If True, detect potential issue with the segmentation data, with a dry-run of json_doctor."),
        "validate": False,
        "output_format": FargvChoice(['auto', 'json', 'page'], description="Output format; if empty, same as detected input format.)"),
        "verbosity": FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
    }
    args, _ = fargv.parse( p )

    set_logging_level( int(args.verbosity) )

    format_to_suffix = { sgf.SegFormat.PAGE: '.xml', sgf.SegFormat.ALTO: '.xml', sgf.SegFormat.JSON: '.json' }
    for file_path in args.file_paths:

        logger.info(f"{file_path}:")

        # we need an access to the segmentation format 
        segdict, segmentation_format = sgf.anyseg_to_dict( file_path )

        if not segdict:
            print(f"Could not parse a dictionary from {segfile_path}. Skipping.")
            continue

        if args.diagnose and not args.repair:
            segdict = sgf.json_doctor( segdict, dry_run=True )
            logger.info("Diagnosis only: set --repair for repairing the file.")
            continue

        if args.repair:
            segdict = sgf.json_doctor( segdict )

        if args.validate:
            if not sgf.json_validate( segdict ):
                continue

        segdict_str = json.dumps( segdict, indent=2 )
        if not args.out:
            print( segdict_str )
            continue

        output_format = None
        # What is the output format?
        if args.output_format == 'page':
            output_format = sgf.SegFormat.PAGE
        elif args.output_format == 'json':
            output_format = sgf.SegFormat.JSON
        elif args.output_format == 'auto':
            output_format = segmentation_format
        # What is the output file name?
        output_suffix = args.output_suffix if args.output_suffix else format_to_suffix[ output_format ]
        input_suffix = args.input_suffix if args.input_suffix else format_to_suffix[ segmentation_format ]
        out_path = ''
        if args.out == 'auto':
            if not re.search( r'{}$'.format( input_suffix ), Path( file_path ).name):
                logger.warning(f"Input file path '{Path(file_path).name}' does not match input suffix '{input_suffix}': output aborted.")
                continue
            out_path = re.sub(r'{}'.input_suffix, output_suffix, file_path )
        else:
            out_path = args.out
        logger.debug(f"Output file = {out_path}")

        if not args.overwrite_existing and Path(out_path).exists():
            logger.info( "File {} exists): skipping.".format(out_path))
            continue
        if output_format == sgf.SegFormat.JSON:
            with open(out_path, 'w') as json_outf:
                json_outf.write( segdict_str )
        elif output_format == sgf.SegFormat.PAGE:
            sgf.page_xml_from_segmentation_dict( segdict, output_file=out_path )

        logger.info(f"→ {out_path}")

    return 0

