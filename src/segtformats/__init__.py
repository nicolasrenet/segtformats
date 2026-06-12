"""
Manipulating segmentation formats (Alto, Page, JSON)

Command-line utilities

- `alto_to_page_xml`: Alto → Page conversion. 
- `alto_to_json`: Page → JSON conversion. 
- `page_xml_to_json`: Page → JSON conversion. 
- `anyseg_to_json`: Detect input format and convert to JSON.
- `json_to_page_xml`: JSON → Page conversion.
- `json_to_json`: Various transformations on JSON metadata, including repairs (region boundaries, line-to-region assignments).
- `anyseg_to_ascii`: Render segmentation metadata on the terminal. 

Help on any command with:

```
python3 -m segtformats.<command> -h
```

How to use the library functions:

```
from segtformats import segtformats as sgf
help( sgf )
```

"""

