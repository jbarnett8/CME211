import glob
import math
import numpy
import os
import sys
import time


def get_files(files):
	if (len(files) != 3):
		raise RuntimeError('Incorrect number of program arguments')

	maze_f = files[1]
	sol_f = files[2]

	# We read the file and store in maze
	with open(maze_f, 'r') as f:
		rows, cols = (int(x) for x in f.readline().split())
		maze = numpy.zeros((rows, cols), dtype=int)
		for line in f:
			r, c = (int(x) for x in line.split())
			maze[r, c] = 1

	# We store all the steps
	with open(sol_f, 'r') as f:
		sol = list()
		for line in f:
			r, c = (int(x) for x in line.split())
			sol.append((r, c))

	# We make sure the start and solution are even possible
	if ((sol[0][0] != 0) or (sol[-1][0] != (rows - 1))):
		print('Solution is invalid!')
		exit(1)

	# Make sure we don't go inside a wall
	for r, c in sol:
		if (maze[r, c] == 1):
			print('Solution is invalid!')
			exit(1)
	
	# We find the difference in steps to make sure we only take one step
	sol_diff = [(abs(x[0] - sol[i][0]), 
		abs(x[1] - sol[i][1])) for i, x in enumerate(sol[1:])]

	for r, c in sol_diff:
		if ((r + c) != 1):
			print((r, c))
			print('Solution is invalid!')

	print('Solution is valid!')


def print_help_text():
	print('This program tests if the solution to a maze is correct.')
	print('maze file: a file containing maze walls')
	print('solution file: a file containing the proposed solution')


if __name__ == '__main__':
	try:
		get_files(sys.argv)
	except RuntimeError as e:
		print('ERROR: {}'.format(e))
		print_help_text()
		sys.exit(2)