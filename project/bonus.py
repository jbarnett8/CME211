import glob
import matplotlib.animation as animation
import matplotlib.pyplot as plot
import numpy
import os
import postprocess
import sys


def print_help_text():
	print('')
	print('bonus.py: make movie of solutions.')
	print('-----------------------------------------------------------------')
	print('Input file: \ta file describing the physical parameters of problem')
	print('Solution prefix: \tprefix for solution .txt files')


if __name__ == '__main__':
	if (len(sys.argv) != 3):
		print('Incorrect number of input arguments.')
		print_help_text()
		sys.exit(1)

	# Grab the input file and then all of the solution files
	# which we sort in ascending order
	input_f = sys.argv[1]
	solution_prefix = sys.argv[2]
	sol_files = glob.glob(solution_prefix + '*.txt')
	sol_files.sort()

	if (len(sol_files) <= 0 or not os.path.exists(input_f)):
		print('One or more of the specified files does not exist.')
		print_help_text()
		sys.exit(1)

	# Store plot data in ims array which grabs Collection from plot output
	ims = []
	fig = plot.figure(figsize=(9, 3))
	for file in sol_files:
		X, Y, data, d_mean = postprocess.get_plot_data(input_f, file, False)
		res = plot.pcolor(X, Y, data, cmap='jet')
		print('file: {}, average temp: {}'.format(file, d_mean))
		ims.append((res,))

	# Feed the plotted data from above into animation function
	im_ani = animation.ArtistAnimation(fig, ims, interval=200, repeat_delay=1000)
	
	# Add the plot labelling
	plot.colorbar(fraction=0.03, pad=0.03, aspect=10)
	plot.xlabel('x')
	plot.ylabel('y')
	ax = plot.gca()
	ax.set_aspect(data.shape[0]/data.shape[1])
	plot.show()
