import subprocess
import IPython
import argparse
import pickle

def filter_to_successful(command_output_pairs):
	"""Filters the list of command output pairs to only the 
	ones that had zero exit codes."""

	return [ (x, y) for (x, y) in command_output_pairs
		if y == '0' ]

def filter_to_remove_ls(command_output_pairs):
	"""Filters the list of commands to remove stuff like ls
	that don't meaningfully affect container state."""

	remove_commands = [
		'ls',
		''
	] 

	return [ (x, y) for (x, y) in command_output_pairs if not x.split(' ')[0] in remove_commands ]

def connect_to_container():
	"""Opens a shell to the container, waits for it to exit (i.e. once the user is done providing input)
	and then returns the list of command & output code pairs
	from the run."""

	# start the shell
	subprocess.run([
		'/bin/bash',
	  'docker-observer.sh'
	]) 

	# parse output
	lines = open('observer_log.txt', 'r').readlines()

	command_output_pairs = []
	for i in range(0, len(lines), 2):
		command = ''.join(lines[i].strip().split("  ")[1:])
		output = lines[i+1].replace('OUTPUT: ', '').strip()

		command_output_pairs.append((command, output))

	return command_output_pairs

def main():
	parser = argparse.ArgumentParser(
		prog = 'DockerObserver',
		description = 'Start a shell in a docker container and observe all the commands.',
	)

	parser.add_argument('-s', '--successful', 
		action='store_true',
		help='Only print out the commands with successful exit codes.')
	parser.add_argument('-f', '--filter', 
		action='store_true',
		help='Filters out commands that *generally* do not affect container state meaningfully, e.g. `ls`') 
	parser.add_argument('-l', '--load',
		help="""Loads an observer output file (stored in the pickle format) and does not run a new container. Other
		options are applied to this file instead of generating a new output file.""")

	args = parser.parse_args()

	if args.load is not None:
		print('Loading: %s' % args.load)

		with open(args.load, 'rb') as fh:
			command_output_pairs = pickle.load(fh) 
	else:
		command_output_pairs = connect_to_container()

	if args.successful:
		command_output_pairs = filter_to_successful(command_output_pairs)
	if args.filter:
		command_output_pairs = filter_to_remove_ls(command_output_pairs)
	
	# by default, we want to save the output into a file that can be read later
	with open('observer_output.pickle', 'wb+') as fh:
		pickle.dump(command_output_pairs, fh)

	print(command_output_pairs)

if __name__ == '__main__':
	main()
