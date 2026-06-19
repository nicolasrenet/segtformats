#!/usr/bin/env python3
"""
PageXML -> JSON conversion.
"""

import sys
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
        'overwrite_existing': (True, "Overwrite an existing file."),
        'comment': ('',"A text string to be added to the <Comments> elt."),
        'verbosity': FargvChoice(['2','0','1','3'], description="Verbosity levels: 0 (quiet), 1 (WARNING), 2 (INFO-default), 3 (DEBUG)"),
    }

    args, _ = fargv.parse( p )

    set_logging_level( int(args.verbosity) )

    for file_path in args.file_paths:

        logger.info(file_path)

        created=sgf.page_xml_split( file_path, overwrite_existing=args.overwrite_existing )
        filenames = '\n'.join(created)
        logger.info(f"Created:\n{filenames}")
