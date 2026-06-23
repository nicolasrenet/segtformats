#!/usr/bin/env python3
"""
Alto -> JSON conversion.
"""

import sys
import json
import re
from pathlib import Path

import fargv
from fargv import FargvPositional, FargvChoice
from jsonschema import validate

from . import segtformats as sgf
from . import set_logging_level, logger


if __name__ == '__main__':
    main()

def main():

    p = {
        'file_paths': FargvPositional(default=[]),
        'out': FargvChoice(['','auto'], description="Set to 'auto' for output to filename <input stem>.<output_suffix>; leave empty for standard output."),
        'input_suffix': '.xml',
        'output_suffix': '.json',
        'overwrite_existing': (False, "Overwrite an existing file."),
        "comment": ('',"A text string to be added to the <Comments> elt."),
        "verbosity": FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
        "repair": (False, "Repair a faulty dictionary (reassign lines to regions, fix region bounding boxes"),
        "validate": (False, "Validate against a JSON schema."),
    }

    args, _ = fargv.parse( p )

    set_logging_level( int(args.verbosity) )

    for file_path in args.file_paths:

        logger.debug(file_path)

        segdict = sgf.alto_to_segmentation_dict( file_path )

        if args.repair:
            segdict = sgf.json_doctor( segdict, verbose=args.verbose )

        # Raise an exception if invalid
        if args.validate:
            sgf.json_validate( segdict )

        segdict_str = json.dumps( segdict, indent=2 )
        if not args.out:
            print( segdict_str )
            continue

        out_path = ''
        if args.out == 'auto':
            if not re.search( r'{}$'.format(args.input_suffix), Path(file_path).name):
                logger.warning(f"Input file path '{Path(file_path).name}' does not match input suffix '{args.input_suffix}': output aborted.")
                continue
            out_path = re.sub(r'{}$'.format( args.input_suffix ), args.output_suffix, file_path )
            logger.debug(f"Output file = {out_path}")


        if not args.overwrite_existing and Path(out_path.exists():
            logger.info("File {} exists: skipping.".format( out_path ))
            continue
        with open(out_path, 'w') as json_outf:
            json_outf.write( segdict_str )
    return 0
