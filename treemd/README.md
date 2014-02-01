mdtree
======

Writes the directory hierarchy in markdown and html

## Requirements

	* Python 3
	* [Markdown](http://packages.python.org/Markdown) for python3

## Usage

```
usage: treemd.py [-h] [-o output_dir] [-m] [--no-html]
                 [--html-template HTMLTEMPLATE] [--css STYLESHEET]
                 [dir]

Display the file tree in markdown and html. If enabled, the files tree.html
and tree.md will be created in [output_dir]

positional arguments:
  dir                   Directory to scan. Defaults to the current directory.

optional arguments:
  -h, --help            show this help message and exit
  -o output_dir         Output directory. Defaults to the current directory.
  -m, --markdown        Enable markdown output.
  --no-html             Disable HTML output.
  --html-template HTMLTEMPLATE
                        HTML skeleton. Requires two "{}" placeholders for the
                        generated css and the html
  --css STYLESHEET      CSS stylesheet to use for the HTML output. Will be
                        embedded in it.

```