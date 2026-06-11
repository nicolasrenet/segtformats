# Handling segmentation metadata: a toolbox


## Installation


  ```bash
  pip install segtformats
  ```

## Features

+ conversion between common segmentation metadata formats (Page, Alto)
+ use JSON as a bridge format, as documented in our [schema](doc/seg_schema.json).

```python
from segtformats import segtformats as sgf

print(sgf.anyseg_to_ascii('tests/data/btv1b84473026_f25.chocomufin.xml', lines=1, scale_hw=.8))
```


## Command-line utilities

+ `alto_to_page_xml`: Alto → Page conversion. Eg.

  ```bash
  python3 -m segtformats.alto_to_page_xml tests/data/217_d9c7f_default.alto.xml
  ```

+ `json_to_page`: JSON → Page conversion.
+ `page_xml_to_json`: Page → JSON conversion. Eg.

  ```bash
  python3 -m segtformats.page_xml_to_json tests/data/217_d9c7f_default.page.xml
  ```

+ `anyseg_to_json`: Detect input format and convert to JSON. Eg.

  ```bash
  python3 -m segtformats.anyseg_to_json --file_paths tests/data/*.xml
  ```

+ `json_to_json`: Various transformations on JSON metadata, including repairs (region boundaries, line-to-region assignments).
+ `anyseg_to_ascii`: Render segmentation metadata on the terminal. Eg.

  ```bash
  python3 -m segtformats.anyseg_to_ascii --file_paths tests/data/*.xml
  ```
## TODO:

+ Page → Alto: really?
+ + `alto_to_json`: Alto → JSON conversion.
