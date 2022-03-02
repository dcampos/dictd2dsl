# dictd2dsl

Convert a dictd (*.dicd + *.index) dictionary to the DSL format

## How to

1. Download the dictd (e.g, from FreeDict) to the same directory as the script.
2. Install dictdlib:

```
pip install git+https://github.com/dcampos/dictdlib.git
```
3. Call `convert.py`. The file names are hardcoded right now.

## Limitations

* Formatting is hard-coded and was made for deu-eng from FreeDict.
* `dictdlib` is *very* slow for compressed (.dz) files. Uncompress first.
