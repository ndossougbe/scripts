mdtree
======

## Requirements

	* Python 3
	* [Markdown](http://packages.python.org/Markdown) for python3

## Usage

```
usage: treemd.py [-h] [-m md-output] [--no-html] [--css STYLESHEET] [dir]

Display the file tree in markdown and html.

positional arguments:
  dir               directory to scan

optional arguments:
  -h, --help        show this help message and exit
  -m md-output      markdown output file
  --no-html         disable HTML output. The markdown will be printed instead
  --css STYLESHEET  CSS stylesheet to use for the HTML output. Will be
                    embedded in it.

```