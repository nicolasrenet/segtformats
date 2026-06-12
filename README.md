# Handling segmentation metadata: a toolbox


## Installation


  ```bash
  pip install segtformats
  ```

## Features

+ conversion between common segmentation metadata formats (Page, Alto).
+ use [PageXML]("http://schema.primaresearch.org/PAGE/gts/pagecontent/2019-07-15") as a bridge format.
+ custom JSON representation documented in our [schema](doc/seg_schema.json): the dictionary allows for manipulating the structure (flattening, region and/or line extraction) or semantic transformations (line-to-region assignments, boundaries).
+ validation options
+ ASCII-rendition of a page segmentation

![](doc/formats_diagram.png)

## SegtFormats library: examples

```python
from segtformats import segtformats as sgf


# Alto to PageXML file
sgf.alto_to_page_xml('tests/data/217_d9c7f_default.alto.xml', output_file='217_d9c7f_default.alto.page.xml')

# Alto to JSON dictionary
segmentation_dict = sgf.alto_to_segmentation_dict('tests/data/217_d9c7f_default.alto.xml')
# validation
assert sgf.json_validate( segmentation_dict )

# ASCII rendition
print(sgf.anyseg_to_ascii('tests/data/btv1b84473026_f25.chocomufin.xml', lines=1, scale_hw=.8))
```


## Command-line utilities

+ `alto_to_page_xml`: Alto → Page conversion. Eg.

  ```bash
  python3 -m segtformats.alto_to_page_xml tests/data/217_d9c7f_default.alto.xml
  ```

+ `alto_to_json`: Page → JSON conversion. Eg.

  ```bash
  python3 -m segtformats.alto_to_json tests/data/217_d9c7f_default.alto.xml
  ```

+ `page_xml_to_json`: Page → JSON conversion. Eg.

  ```bash
  python3 -m segtformats.page_xml_to_json tests/data/217_d9c7f_default.page.xml
  ```

+ `anyseg_to_json`: Detect input format and convert to JSON. Eg.

  ```bash
  python3 -m segtformats.anyseg_to_json --file_paths tests/data/*.xml
  ```

+ `json_to_page_xml`: JSON → Page conversion.

  ```bash
  python3 -m segtformats.json_to_page_xml tests/data/217_d9c7f_default.json
  ```

+ `json_to_json`: Various transformations on JSON metadata, including repairs (region boundaries, line-to-region assignments).
+ `anyseg_to_ascii`: Render segmentation metadata on the terminal. Eg.

  ```bash
  python3 -m segtformats.anyseg_to_ascii --file_paths tests/data/*.xml
  ```

## TODO:

+ Page → Alto: really?
