import glob
import math
import os
import sys
import time

class Airfoil:

	def __init__(self, inputdir):
		self.inputdir = inputdir

		if not os.path.exists(inputdir):
			raise RuntimeError("Directory {} does not exist".format(inputdir))

		x, y, name = self.get_xy_data()
		self.x = x
		self.y = y
		self.name = name
		alpha_cf = self.get_alpha_cf_data()
		self.alpha_cf = alpha_cf
		cord_len = self.calc_cord_len()
		self.cord_len = cord_len
		alpha_lift_coeffs = self.calc_lift_coeff()
		self.alpha_lift_coeffs = alpha_lift_coeffs
		alpha_stag = self.calc_stagnation()
		self.alpha_stag = alpha_stag


	def get_xy_data(self):
		xy_f = glob.glob(os.path.join(self.inputdir, 'xy.dat'))
		if (len(xy_f) > 1):
			raise RuntimeError("There are multiple xy.dat files")
		if (len(xy_f) == 0):
			raise RuntimeError("There is no xy.dat file")
		x = []
		y = []
		with open(xy_f[0],'r') as f:
			name = f.readline().strip()
			for line in f:
				xy = line.split()
				try:
					xf = float(xy[0])
					yf = float(xy[1])
				except:
					continue
				x.append(xf)
				y.append(yf)

		if (len(x) != len(y)) or (len(x) == 0):
			raise RuntimeError("There was an error in the content of \
				the xy.dat file. There were no numbers OR line(s) \
				contains only a single number.")

		return x, y, name

	def get_alpha_cf_data(self):
		alpha_fs = glob.glob(os.path.join(self.inputdir, 'alpha*.dat'))

		alpha_cf = dict()
		for alpha_f in alpha_fs:
			name = os.path.split(alpha_f)[1]
			try:
				angle = float(name[len('alpha'):-len('.dat')])
			except:
				raise RuntimeError("file {} in {} does not contain a \
					valid angle".format(name, inputdir))

			if angle in alpha_cf.keys():
				raise RuntimeError("angle {} occurs twice in {}".format(
					angle, inputdir))

			cfs = []
			with open(alpha_f,'r') as f:
				for line in f:
					if line.find('#') == -1:
						cfs.append(float(line))
			alpha_cf[angle] = cfs

		return alpha_cf

		
	def calc_cord_len(self):
		x_min = min(self.x)
		x_min_i = self.x.index(x_min)
		y_min = self.x[x_min_i]
		x_max = max(self.x)
		x_max_i = self.x.index(x_max)
		y_max = self.x[x_max_i]

		return math.sqrt((x_max - x_min)**2 + (y_max - y_min)**2)


	def calc_lift_coeff(self):
		cord = self.cord_len
		x = self.x
		y = self.y
		alpha_cf = self.alpha_cf

		lift_coeffs = dict()

		for alpha, cps in alpha_cf.items():
			cx = 0
			cy = 0
			for x1, y1, x2, y2, cp in zip(x[:-1], y[:-1], x[1:], y[1:], cps):
				dx = x2 - x1
				dy = y2 - y1
				cx += -cp*dy/cord
				cy += cp*dx/cord
			lift_coeffs[alpha] = cy*math.cos((math.pi/180)*alpha) \
							 	 - cx*math.sin((math.pi/180)*alpha)
		return lift_coeffs

	def calc_stagnation(self):
		alpha_cf = self.alpha_cf
		x = self.x
		y = self.y
		alpha_stag = dict()
		for alpha, cps in alpha_cf.items():
			temp = []
			for cp in cps:
				temp.append(abs(cp - 1))
			stag_point_i = temp.index(min(temp))

			loc_x = (x[stag_point_i + 1] + x[stag_point_i]) / 2
			loc_y = (y[stag_point_i + 1] + y[stag_point_i]) / 2

			alpha_stag[alpha] = (loc_x, loc_y, cps[stag_point_i])

		return alpha_stag

	def __str__(self):
		header = 'Test case: ' + self.name + '\n\n'
		header += 'alpha     cl           stagnation pt        \n'
		header += '-----  -------  ----------------------------\n'
		body = ''
		for alpha, cl in self.alpha_lift_coeffs.items():
			loc_x, loc_y, stag = self.alpha_stag[alpha]
			body += '{: .2f}  {: .4f}  ({: .4f},  {: .4f}  {: .4f})\n'.format(
					alpha, cl, loc_x, loc_y, stag)
		return header + body