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
            "segfile_paths": FargvPositional(default=[], description="A JSON line segmentation file (e.g <prefix>.lines.pred.json)."),
            "overwrite_existing": (False, "Do not overwrite existing output file"),
            "repair": (False, "If True, fix semantic errors in the segmentation (line-to-region assignment, region boundaries)."),
            "validate": False,
            "output_format": FargvChoice(['json', 'stdout'], description="Output format"),
            'verbosity': (2,"Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
    }

    args, _ = fargv.parse( p )
    
    set_logging_level( args.verbosity )

    for segfile_path_str in args.segfile_paths:

        status_string=f"{segfile_path_str}: "

        segdict = sgf.anyseg_to_dict( segfile_path_str )
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
        if args.output_format == 'stdout':
            print( segdict_str )
        else:
            json_path = re.sub(r'\.[^.]+$', r'.json', segfile_path_str )
            if not args.overwrite_existing and Path(json_path).exists():
                logger.info( status_string + "_ (file exists)".format( json_path ))
                continue
            with open(json_path, 'w') as json_outf:
                json_outf.write( segdict_str )
                logger.info( status_string + f"W → {json_path}")

    return 0
