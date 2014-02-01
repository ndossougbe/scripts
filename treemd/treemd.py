#!/usr/bin/env python3

import os
import inspect
import string
import markdown
import argparse


def _apply_style(name, isTerminal):
	name = name.replace('[','\[') # Avoid names with square brackets to be parsed to links
	if isTerminal:
		return name
	else:
		return '**{}**'.format(name)


def _is_folder_to_ignore(foldername):
	''' Returns false for hidden files (starting with '.') '''
	return not foldername or foldername[0] == '.'


def build_markdown(root):
	output = '\n'
	rootDepth = len(os.path.dirname(root).split(os.sep))

	for path, dirs, files in os.walk(root):
		# prepare the next step
		# print(dirs)
		dirs[:] = [d for d in dirs if not _is_folder_to_ignore(d)]
		dirs.sort()

		head, tail = os.path.split(path)

		if _is_folder_to_ignore(tail): continue  # top level directories are not affected by the 'dirs' modificaiton 

		padding = '\t' * (len(head.split(os.sep)) - rootDepth)
		name = _apply_style(tail, len(dirs) is 0)

		output += '{}- {}\n'.format(padding, name)

	return output


def build_html(mdString, args):
	template, style = '{}{}',''

	with open(args.htmlTemplate,'r', encoding='utf-8') as htmlFile:
		template = htmlFile.read()

	if args.stylesheet:
		with open(args.stylesheet, 'r', encoding='utf-8') as cssFile:
			style = cssFile.read()

	return template.format(css=style, tree=markdown.markdown(mdString, output_format='html5'), root=args.dir)


def _main(args):
	markdown = build_markdown(args.dir)

	if args.md_output_enabled:
		with open(os.path.join(args.output_dir, 'tree.md'),'w', encoding='utf-8') as markdown_output:
			markdown_output.write(markdown)

	if args.html_output_enabled:
		with open(os.path.join(args.output_dir, 'tree.html'),'w', encoding='utf-8') as html_output:
			html_output.write(build_html(markdown, args))


if __name__ == '__main__':

	scriptDir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

	parser = argparse.ArgumentParser(description='Display the file tree in markdown and html. If enabled, the files '
		'tree.html and tree.md will be created in [output_dir]')
	parser.add_argument('-o', dest='output_dir', metavar='output_dir', default='.', 
						help='Output directory. Defaults to the current directory.' )
	parser.add_argument('dir', nargs='?', default='.', help='Directory to scan. Defaults to the current directory.', )
	parser.add_argument('-m', '--markdown', action='store_true', dest='md_output_enabled',
						help='Enable markdown output.')
	parser.add_argument('--no-html', action='store_false', dest='html_output_enabled',
						help='Disable HTML output.')
	parser.add_argument('--html-template', dest='htmlTemplate', default=os.path.join(scriptDir, 'default.html'),
						help='HTML skeleton. Requires "{css}", "{tree}" and "{root}" placeholders')
	parser.add_argument('--css', dest='stylesheet', default=os.path.join(scriptDir, 'default.css'),
						help='CSS stylesheet to use for the HTML output. Will be embedded in it.')

	args = parser.parse_args()
	
	_main(args)
