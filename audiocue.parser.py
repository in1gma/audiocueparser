import argparse
import re

def parse_args():
	parser = argparse.ArgumentParser(description='This program parse some raw audio info to CUE')
	parser.add_argument('--header', dest='header', action='store', help='Path to header of CUE', required=True)
	parser.add_argument('--raw', dest='raw', action='store', help='Path to raw autio info', required=True)
	parser.add_argument('--output', dest='output', action='store', help='Path to output', required=True)

	return parser.parse_args()

def parse_text(args):
	template = '\
	TRACK {number} AUDIO\n\
		TITLE "{title}"\n\
		PERFORMER "{performer}"\n\
		INDEX 01 {formatted_time}\n\
\n'

	output = open(args.output, 'w')
	with open(args.header, 'r') as header:
		output.write(header.read() + '\n')

	with open(args.raw, 'r') as raw:
		number = 1
		for line in raw:
			match  = re.search(r'(?P<title>.*?)\s?\\\\\s?(?P<performer>.*?)\s?(?P<time>((?P<hour>\d+):)*(?P<minute>\d+):(?P<second>\d+))', line)
			item = match.groupdict()

			item['number'] = number
			item['formatted_time'] = '{minute}:{second}:{milliseconds}'.format(minute=60*int(item['hour']) + int(item['minute']) if item['hour'] is not None else item['minute'],second=item['second'],milliseconds='00') # is's bad
			output.write(template.format(**item))
			number += 1

	output.close()

def main():
	args = parse_args()
	parse_text(args)

if __name__ == "__main__":
	main()