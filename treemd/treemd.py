#!/usr/bin/env python3

import os
import inspect
import string
import markdown
import argparse


def _applyStyle(name, isTerminal):
	name = name.replace('[','\[') # Avoid names with square brackets to be parsed to links
	if isTerminal:
		return name
	else:
		return '**{}**'.format(name)


def build_markdown(root):
	output = '\n'
	rootDepth = len(os.path.dirname(root).split(os.sep))
	for path, dirs, files in os.walk(root):
		head, tail = os.path.split(path)
		
		padding = '\t' * (len(head.split(os.sep)) - rootDepth)
		name = _applyStyle(tail, len(dirs) is 0)

		output += '{}- {}\n'.format(padding, name)

	return output


def build_html(mdString, stylesheet, htmlTemplate):
	template = htmlTemplate.read()
	# template = ('<!DOCTYPE html>\n'
	# 			'<html>\n'
	# 			'<head>\n'
	# 			'	<title></title>\n'
	# 			'	<style type="text/css">\n'
	# 			'{}\n'
	# 			'	</style>\n'
	# 			'</head>\n'
	# 			'<body>\n'
	# 			'	<div class="tree">\n'
	# 			'{}\n'
	# 			'	</div>\n'
	# 			'</body>\n'
	# 			'</html>')

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
		html = build_html(markdown, args.stylesheet, args.htmlTemplate)
		open('output.html', 'w').write(html)
		print(html)



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
	args.htmlTemplate = open(os.path.join(scriptDir, 'template.html'),'r')
	
	_main(args)
