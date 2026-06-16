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

if __name__ == '__main__':
    main()

def main():
    p = {
            "segfile_paths": FargvPositional(default=[], description="A JSON line segmentation file (e.g <prefix>.lines.pred.json)."),
            "overwrite_existing": (False, "Do not overwrite existing output file"),
            "repair": (False, "If True, fix semantic errors in the segmentation (line-to-region assignment, region boundaries)."),
            "diagnose": (True, "If True, detect potential issue with the segmentation data, with a dry-run of json_doctor."),
            "validate": False,
            "output_format": FargvChoice(['', 'json', 'page'], description="Output format (if empty: JSON on standard output."),
            "output_suffix": ('',"If empty, output file's suffix is determined by output format (.json or .xml)"),
            "verbose": True,
    }
    args, _ = fargv.parse( p )

    for segfile_path_str in args.segfile_paths:

        if args.verbose:
            print(f"{segfile_path_str}:", end='')
        segdict = None
        segmentation_format = sgf.get_format( segfile_path_str )
        if segmentation_format == sgf.SegFormat.Unknown:
            print("Could not determine input format. Skipping.")
            continue 
        if segmentation_format == sgf.SegFormat.JSON:
            with open(segfile_path_str) as seg_if:
                segdict = json.load( seg_if )
        elif segmentation_format == sgf.SegFormat.PAGE:
            segdict = sgf.segmentation_dict_from_page_xml( segfile_path_str )
        elif segmentation_format == sgf.SegFormat.ALTO:
            segdict = sgf.segmentation_dict_from_page_xml( sgf.alto_to_page_xml_string( segfile_path_str ))

        if not segdict:
            print(f"Could not parse a dictionary from {segfile_path}. Skipping.")
            continue

        if args.diagnose and not args.repair:
            segdict = sgf.json_doctor( segdict, dry_run=True )
            continue

        if args.repair:
            segdict = sgf.json_doctor( segdict )

        if args.validate:
            if not sgf.json_validate( segdict ):
                continue

        segdict_str = json.dumps( segdict, indent=2 )
        if not args.output_format:
            print( segdict_str )
            continue

        replacement_suffix = ('.json' if args.output_format=='json' else '.xml') if not args.output_suffix else args.output_suffix
        output_path = re.sub(r'\.[^.]+$', r'{}'.format(replacement_suffix), segfile_path_str ) 
        if not args.overwrite_existing and Path(output_path).exists():
            if args.verbose:
                print( " (file exists)")
            continue
        if args.output_format == 'json':
            with open(output_path, 'w') as json_outf:
                json_outf.write( segdict_str )
        elif args.output_format == 'page':
            sgf.page_xml_from_segmentation_dict( segdict, output_file=output_path )

        if args.verbose:
            print(f"→ {output_path}")

