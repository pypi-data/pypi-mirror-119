# tealprint

[![python](https://img.shields.io/pypi/pyversions/tealprint.svg)](https://pypi.python.org/pypi/tealprint)
[![Latest PyPI version](https://img.shields.io/pypi/v/tealprint.svg)](https://pypi.python.org/pypi/tealprint)
[![Downloads](https://pepy.tech/badge/tealprint)](https://pepy.tech/project/tealprint?right_color=orange)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/Senth/tealprint.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Senth/tealprint/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/Senth/tealprint.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/Senth/tealprint/context:python)

Prints messages to the console

## Features

- different verbosity levels: `none, error, warning, info, verbose, debug`
- Indent messages easily under a header
- Set color using the [colored](https://pypi.org/project/colored/) package

## Examples

### Indentation

```python
from tealprint import TealConfig, TealLevel, TealPrint

# Using push_indentation()
TealConfig.level = TealLevel.verbose
TealPrint.info("Header")
TealPrint.push_indent(TealLevel.info)
TealPrint.info("More information")
TealPrint.pop_indent()

# Push in header directly
TealPrint.info("Header 2", push_indent=True)
TealPrint.info("Information", push_indent=True)
TealPrint.verbose("Fine grained information")
TealPrint.pop_indent()
TealPrint.info("✅ Done")

# Skips hidden levels
TealPrint.info("Header 3", push_indent=True)
TealPrint.info("Saving all files...")
TealPrint.push_indent(TealLevel.debug)
TealPrint.debug("Saving file X") # Not displayed
TealPrint.info("Couldn't save file Y") # Only indented once, since push_indent(TealLevel.debug) was used
TealPrint.pop_indent()
TealPrint.info("✅ Saved all files")

# Same as above but with TealLevel.debug
TealConfig.level = TealLevel.debug
TealPrint.info("Header 4", push_indent=True)
TealPrint.info("Saving all files...")
TealPrint.push_indent(TealLevel.debug)
TealPrint.debug("Saving file X")
TealPrint.info("Couldn't save file Y") # Will be indented twice this time
TealPrint.pop_indent()
TealPrint.info("✅ Saved all files")
```

OUTPUT

```console
Header
    More information
Header 2
    Information
        Fine grained information
✅ Done
Header 3
    Saving all files...
    Couldn't save file Y
    ✅ Saved all files
Header 4
    Saving all files...
        Saving file X
        Couldn't save file Y
    ✅ Saved all files
```

### Color

```python
from tealprint import TealPrint
from colored import fg, attr

TealPrint.info("Header", color=attr("bold"), push_indent=True)
TealPrint.info("OK", color=fg("green"))
```

OUTPUT

![colored](examples/colored.png)

### Automatic color for errors and warnings

```python
from tealprint import TealPrint

TealPrint.error("Could not open file")
TealPrint.warning("Missing configuration for X")
```

OUTPUT

![error_and_warnings](examples/error_and_warnings.png)

## Authors

- Matteus Magnusson, senth.wallace@gmail.com
