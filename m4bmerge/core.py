from pathlib import Path
import argparse, collections, logging, os
# Local imports
import audible_helper, config, helpers, m4b_helper

def main(inputs):
	logging.info(f"Working on: {inputs}")
	# Validate path, check if it's a directory or a file
	# This will also run find_extension to determine relevant filetype
	input_data = helpers.get_directory(inputs)
	
	# Validate ASIN input
	while True:
		try:
			asin = input("Audiobook ASIN: ")
			helpers.validate_asin(asin)
			break
		except Exception as e:
			print(str(e))
	
	# Create BookData object from asin response
	aud = audible_helper.BookData(asin)
	metadata = aud.parser()

	# Process metadata and run components to merge files
	m4b = m4b_helper.M4bMerge(input_data, metadata)
	m4b.run_merge()

# Only run call if using CLI directly
if __name__ == "__main__":
	# Setup global variables

	parser = argparse.ArgumentParser(
		description='Bragi Books merge cli'
		)
	parser.add_argument(
		"-i", "--inputs",
		help="Input paths to process",
		nargs='+',
		required=True,
		type=Path
		)
	parser.add_argument(
		"--log_level",
		help="Set logging level"
		)
	args = parser.parse_args()

	# Get log level from system or input
	if args.log_level:
		numeric_level = getattr(logging, args.log_level.upper(), None)
		if not isinstance(numeric_level, int):
			raise ValueError('Invalid log level: %s' % args.log_level)
		logging.basicConfig(level=numeric_level)
	else:
		logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
	# Run through inputs
	for inputs in args.inputs:
		if inputs.exists():
			main(inputs)
		else:
			logging.error(f"Input \"{inputs}\" does not exist")