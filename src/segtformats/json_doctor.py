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
from fargv import FargvPositional, FargvChoice

from . import segtformats as sgf
from . import set_logging_level, logger


if __name__ == '__main__':
    main()

def main():

    p = {
        'file_paths': FargvPositional(default=[], description="Input file (JSON)."),
        'out': ('', "Output to filename <out>: set to 'auto' for output to filename <input stem>.<output_suffix>."),
        'input_suffix': '.lines.pred.json',
        'output_suffix': '.json', 
        'overwrite_existing': (False, "Overwrite an existing output file."),
        'drop_transcription': (False, "Remove line transcription, if it exists."),
        'repair': (False, "Repair a faulty dictionary: re-assign lines to their proper regions; expand regions to include every pixel of the line polygon."),
        'diagnose': (False, "Run a diagnosis, scanning for potential issues."),
        #'delete_line_features': FargvPositional(default=[], description="Line items to be removed (use with caution!)"),
        'verbosity': FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
        "comment": ('',"A text string to be added to the <Comments> elt."),
    }

    args, _ = fargv.parse( p )

    set_logging_level( int(args.verbosity) )

    for file_path in args.file_paths:
        json_path = Path( file_path )

        if sgf.get_format( json_path ) != sgf.SegFormat.JSON:
            logger.warning(f"{file_path} is not a valid JSON file: skipping.")
            continue

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
        else:
            out_path = args.out
        logger.debug(f"Output file = {out_path}")

        if not args.overwrite_existing and Path(out_path).exists():
            logger.info("File {} exists: skipping.".format( out_path ))
            continue
        with open(out_path, 'w') as json_outf:
            json_outf.write( segdict_str )
    return 0

