#!/usr/bin/env python3

import os
import inspect
import string
import markdown
import argparse

def _applyStyle(name, isTerminal):
	name = name.replace('[','\[')
	if isTerminal:
		return name
	else:
		return '**{}**'.format(name)

def build_markdown(root):
	output = '\n'
	for path, dirs, files in os.walk(root):
		head, tail = os.path.split(path)
		
		padding = '\t' * (len(head.split(os.sep)) -1)
		name = _applyStyle(tail, len(dirs) is 0)

		output += '{}- {}\n'.format(padding, name)

	return output

def build_html(mdString, stylesheet):
	template = ('<!DOCTYPE html>\n'
				'<html>\n'
				'<head>\n'
				'	<title></title>\n'
				'	<style type="text/css">\n'
				'{}\n'
				'	</style>\n'
				'</head>\n'
				'<body>\n'
				'	<div class="tree">\n'
				'{}\n'
				'	</div>\n'
				'</body>\n'
				'</html>')

	if stylesheet:
		style = stylesheet.read()
	else:
		style = ''

	return template.format(style , markdown.markdown(mdString, output_format='html5'))

def _main(args):

	markdown = build_markdown(args.dir)

	if args.mdout:
		args.mdout.write(markdown)

	if args.no_html:
		print(markdown)
	else:
		print(build_html(markdown, args.stylesheet))



if __name__ == '__main__':

	scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

	parser = argparse.ArgumentParser(description='Display the file tree in markdown and html.')
	parser.add_argument('-m', dest='mdout', metavar='md-output', type=argparse.FileType('w'), 
						help='markdown output file' )
	parser.add_argument('dir', nargs='?', help='directory to scan', default='.')
	parser.add_argument('--no-html', action='store_true',
						help='disable HTML output. The markdown will be printed instead')
	parser.add_argument('--css', type=argparse.FileType('r'), dest='stylesheet', 
						default=open(os.path.join(scriptDir, 'default.css'),'r'),
						help='CSS stylesheet to use for the HTML output. Will be embedded in it.')

	args = parser.parse_args()
	
	_main(args)
