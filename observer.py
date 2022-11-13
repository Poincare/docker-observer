import subprocess
import argparse
import pickle
import pathlib
import os

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

def connect_to_container(container_id):
	"""Opens a shell to the container, waits for it to exit (i.e. once the user is done providing input)
	and then returns as a tuple:
		* list of command & output code pairs from the run
		* the list of de-duplicated files that were checked in"""

	# start the shell
	subprocess.run([
		'/bin/bash',
	  'docker-observer.sh',
		container_id
	]) 

	# parse output (skip first line since it contains an extra "OUTPUT" listing because
	# of the way `trap DEBUG` works in bash)
	lines = open('observer_log.txt', 'r').readlines()[1:]

	command_output_pairs = []
	for i in range(0, len(lines)-1, 2):
		command = ''.join(lines[i].strip().split("  ")[1:])
		output = lines[i+1].replace('OUTPUT: ', '').strip()

		command_output_pairs.append((command, output))

	checked_in_file_lines = open('observer_checked_in_files.txt', 'r').readlines()
	checked_in_files = list(set([ x.strip() for x in checked_in_file_lines ]))

	return command_output_pairs, checked_in_files

def format_command_output_pairs(command_output_pairs):
	"""Returns the command output pairs as a single string."""
	return "\n".join([ '%s\t%s' % (command, output) 
		for command, output in command_output_pairs ])

def copy_files_from_container(container_id, checked_in_files, copy_to_directory="container_files"):
	"""Copies the checked in files from the container to a local directory."""

	try:
		os.mkdir(copy_to_directory)
	except FileExistsError:
		pass

	container_path_to_local_path = {
		filepath : (copy_to_directory + filepath)
		for filepath in checked_in_files
	}
	print(f'Container path to local path: {container_path_to_local_path}')

	# create the necessary directory structure in the target directory
	for _, localpath in container_path_to_local_path.items():
		print(f'Local path: {localpath}')
		# filepath starts with a "/"
		pathlib.Path(localpath).parent.mkdir(parents=True, exist_ok=True)

	# copy the files from the container to the local directory structure
	# TODO use the Docker API to do this, not subprocesses
	for filepath, localpath in container_path_to_local_path.items():
		subprocess.run([
			'docker',
			'cp',
			f'{container_id}:{filepath}',
			localpath
		])
		print(f'Copied {filepath} to {localpath}')

def main():
	parser = argparse.ArgumentParser(
		prog = 'DockerObserver',
		description = 'Start a shell in a docker container and observe all the commands.',
	)

	parser.add_argument('container', help='Container ID to connect to.') 
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
		command_output_pairs, checked_in_files = connect_to_container(args.container)

	if args.successful:
		command_output_pairs = filter_to_successful(command_output_pairs)
	if args.filter:
		command_output_pairs = filter_to_remove_ls(command_output_pairs)
	
	# by default, we want to save the output into a file that can be read later
	with open('observer_output.pickle', 'wb+') as fh:
		pickle.dump(command_output_pairs, fh)


	copy_files_from_container(args.container, checked_in_files)

	print(format_command_output_pairs(command_output_pairs))

if __name__ == '__main__':
	main()
