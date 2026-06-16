#!/usr/bin/env python3
"""
Script for JSON -> PageXML conversion.

"""

import sys
import json
from pathlib import Path
from datetime import datetime

import fargv
from fargv import FargvChoice, FargvPositional

from . import segtformats as sgf


if __name__ == '__main__':
    main()


def main():

    p = {
        'file_paths': FargvPositional(default=[]),
        'polygon_key': 'coords',
        'output_format': FargvChoice(['xml', 'stdout']),
        'with_transcription': (True, "Extract line transcription, if it exists"),
        'overwrite_existing': (False, "Overwrite an existing output file."),
        'comment': ('',"A text string to be added to the <Comments> elt."),
        'verbose': (False, "Verbose output."),
    }

    args, _ = fargv.parse( p )

    for json_path in args.file_paths:
        json_path=Path( json_path )
        xml_path = json_path.with_suffix('.xml')

        with open( json_path, 'r') as json_if:
            if args.verbose:
                print( json_path )
            segdict = json.load( json_if )
            segdict['metadata'].update( {'created': str(datetime.now()), 'creator': __file__ })
            if args.comment:
                segdict['metadata']['comments']=args.comment

            if args.output_format == 'stdout':
                sgf.page_xml_from_segmentation_dict( segdict, '', polygon_key=args.polygon_key, with_text=args.with_transcription )
            else:
                if not args.overwrite_existing and xml_path.exists():
                    print("File {} exists: abort.".format( xml_path ))
                else:
                    sgf.page_xml_from_segmentation_dict( segdict, xml_path, polygon_key=args.polygon_key, with_text=args.with_transcription )

