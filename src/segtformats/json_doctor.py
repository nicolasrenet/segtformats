#!/usr/bin/env python3
"""
JSON -> JSON conversion

Read a JSON segmentation file, with a choice of options:

+ repair a faulty file
+ remove transcription data
+ add a comment
"""

import sys
import json
import re
from datetime import datetime
from pathlib import Path

import fargv
from fargv import FargvPositional

from . import segtformats as sgf
from . import set_logging_level, logger


if __name__ == '__main__':
    main()

def main():

    p = {
        'file_paths': FargvPositional(default=[], description="Input file (JSON)."),
        'input_suffix': ('.lines.pred.json', "Input file suffix."),
        'output_suffix': ('', "Output file suffix; if empty, write on standard output"),
        'overwrite_existing': (False, "Overwrite an existing output file."),
        'drop_transcription': (False, "Remove line transcription, if it exists."),
        'repair': (False, "Repair a faulty dictionary: re-assign lines to their proper regions; expand regions to include every pixel of the line polygon."),
        'diagnose': (False, "Run a diagnosis, scanning for potential issues."),
        #'delete_line_features': FargvPositional(default=[], description="Line items to be removed (use with caution!)"),
        'verbosity': (2,"Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
        "comment": ('',"A text string to be added to the <Comments> elt."),
    }

    args, _ = fargv.parse( p )

    set_logging_level( args.verbosity )

    for file_path in args.file_paths:
        json_path = Path( file_path )

        segdict = None
        with open( json_path, 'r') as json_if:
            segdict = json.load( json_if )

            if args.diagnose:
                logger.info("File diagnosis")
                sgf.json_doctor( segdict, dry_run=True )
                continue

            if args.repair:
                logger.info("Repairing file")
                segdict = sgf.json_doctor( segdict )

            output_file_path = Path( file_path.replace( args.input_suffix, args.output_suffix )) if args.output_suffix else None
            logger.info(f'{file_path} → {output_file_path}')
            if output_file_path and not args.overwrite_existing and output_file_path.exists():
                logger.info(f"Existing {output_file_path}: skipping." )
                continue

            line_dicts = sgf.line_dicts_from_segmentation_dict( segdict )

            # delete unwanted features
#            if args.delete_line_features:
#                for line in line_dicts:
#                    for key in args.delete_line_features:
#                        if key not in line:
#                            continue
#                        del line[key]

            # remove transcriptions
            if args.drop_transcription:
                for line in line_dicts: 
                    if 'text' in line:
                        del line['text']

            # insert metadata at the top
            regions = segdict['regions']
            del segdict['regions']
            segdict['metadata'].update( {'created': str(datetime.now()), 'creator': __file__ })

            if args.comment:
                segdict['metadata']['comments']=args.comment
            segdict['regions']=regions

            # output
            if segdict is not None:
                if output_file_path:
                    with open( output_file_path,'w') as of:
                        of.write( json.dumps( segdict, indent=2))
                else:
                    print( json.dumps( segdict, indent=2 ))
    return 0

