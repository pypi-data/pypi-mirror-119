# d2b-compile

compile-dcm2bids-config plugin for the d2b package.

[![PyPI Version](https://img.shields.io/pypi/v/d2b-compile.svg)](https://pypi.org/project/d2b-compile/)

## Installation

```bash
pip install d2b-compile
```

## Usage

After installation the `d2b run` command should have additional `compile`-subcommand:

```text
$ d2b --help
usage: d2b [-h] [-v] {run,scaffold,compile} ...

d2b - Organize data in the BIDS format

positional arguments:
  {run,scaffold,compile}

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
```

```text
$ d2b compile --help
usage: d2b compile [-h] [-o OUT_FILE] in_file [in_file ...]

positional arguments:
  in_file               The JSON config files to combine

optional arguments:
  -h, --help            show this help message and exit
  -o OUT_FILE, --out-file OUT_FILE
                        The file to write the combined config file to. If not specified outputs are written to stdout.
```

The `d2b compile` subcommand is a thin wrapper around `compile-dcm2bids-config`.
