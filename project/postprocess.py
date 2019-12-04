import matplotlib.figure as figure
import matplotlib.pyplot as plot
import numpy
import os
import sys


def print_help_text():
	"""
	Prints help text
	"""
	print('')
	print('postprocess.py: plot solution files from heat equation solution.')
	print('-----------------------------------------------------------------')
	print('Input file: \ta file describing the physical parameters of problem')
	print('Solution file: \tsolution from c++ script to plot')


def get_plot_data(input_f, solution_f, if_print = True):
	"""
	Processes the basic data provides easy to plot data

	Parameters:
	input_f (string): The name of the input file
	solution_f (string): The name of the solution file to look at
	if_print (bool): optional, True, whether or not to print results to console

	Returns:
	list(float): x coordinates
	list(float): y coordinates
	numpy.2Darray: temperature data
	float: average temperature 
	"""
	if (if_print):
		print('Input file processed: {}'.format(input_f))

	# Grab all of the necessary input file data
	with open(input_f, 'r') as f:
		line = f.readline().split()
		L = float(line[0])
		W = float(line[1])
		h = float(line[2])

	# We perform some basic pararmeters sanity checks
	if ((L < 0) or (W < 0) or (h < 0)):
		print('Inpute file has invalid parameters.')
		print_help_text()
		sys.exit(1)

	# Load data from text file and get average
	data = numpy.loadtxt(solution_f)
	d_mean = numpy.average(data.flatten())

	if (if_print):
		print('Mean Temperature: {:5f}'.format(d_mean))

	X = numpy.arange(0, L + h, h)
	Y = numpy.arange(0, W + h, h)[::-1]

	return X, Y, data, d_mean


if __name__ == '__main__':
	if (len(sys.argv) != 3):
		print('Incorrect number of input arguments.')
		print_help_text()
		sys.exit(1)

	input_f = sys.argv[1]
	solution_f = sys.argv[2]
	if (not os.path.exists(input_f) or not os.path.exists(solution_f)):
		print('One or more of the specified files does not exist.')
		print_help_text()
		sys.exit(1)

	# Get data, plot data with formatted plot
	plot.figure(figsize=(9, 3))
	X, Y, data, d_mean = get_plot_data(input_f, solution_f)
	plot.pcolor(X, Y, data, cmap='jet')
	plot.colorbar(fraction=0.03, pad=0.03, aspect=10)
	plot.contour(X, Y, data, [d_mean], colors='black', linewidths=2)
	plot.xlabel('x')
	plot.ylabel('y')
	plot.title(solution_f)
	ax = plot.gca()
	ax.set_aspect(data.shape[0]/data.shape[1])
	plot.show()