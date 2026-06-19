#!/usr/bin/env python3
"""
Script for JSON -> PageXML conversion.

"""

import sys
import json
import re
from pathlib import Path
from datetime import datetime

import fargv
from fargv import FargvChoice, FargvPositional

from . import segtformats as sgf
from . import set_logging_level, logger


if __name__ == '__main__':
    main()

def main():

    p = {
        'file_paths': FargvPositional(default=[]),
        'out': ('', "Output to filename <out>: set to 'auto' for output to filename <input stem>.<output_suffix>."),
        'input_suffix': ('.xml', "Input file suffix."),
        'output_suffix': ('.xml', "Output file suffix; if empty, write on standard output"),
        'with_transcription': (True, "Extract line transcription, if it exists"),
        'overwrite_existing': (False, "Overwrite an existing output file."),
        'comment': ('',"A text string to be added to the <Comments> elt."),
        'verbosity': FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
    }

    args, _ = fargv.parse( p )

    set_logging_level( int(args.verbosity) ) 

    for file_path in args.file_paths:
        file_path=Path( file_path )
        xml_path = file_path.with_suffix('.xml')

        with open( file_path, 'r') as json_if:
            logger.warning( file_path )
            segdict = json.load( json_if )
            segdict['metadata'].update( {'created': str(datetime.now()), 'creator': __file__ })
            if args.comment:
                segdict['metadata']['comments']=args.comment

            if not args.out:
                sgf.page_xml_from_segmentation_dict( segdict, '', with_text=args.with_transcription )
                continue

            out_path = ''
            if args.out == 'auto':
                if not re.search( r'{}$'.format(args.input_suffix), Path(file_path).name):
                    logger.warning(f"Input file path '{file_path.name}' does not match input suffix '{args.input_suffix}': output aborted.")
                    continue
                out_path = Path(re.sub(r'{}$'.format( args.input_suffix ), args.output_suffix, file_path )) 
            else:
                out_path = args.out
            logger.debug(f"Output file = {out_path}")

            if not args.overwrite_existing and out_path.exists():
                logger.info("File {} exists: skipping.".format( out_path ))
                continue
            sgf.page_xml_from_segmentation_dict( segdict, out_path, with_text=args.with_transcription ) 
            


    return 0
