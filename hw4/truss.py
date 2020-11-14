import glob
import math
import matplotlib.pyplot as plt
import numpy
import os
import scipy.sparse as sprs
import sys
import time

class Truss:


	def __init__(self, joint_file, beam_file):
		beam_raw_data = numpy.loadtxt(beam_file)
		joint_raw_data = numpy.loadtxt(joint_file)
		print(beam_raw_data)
		print(joint_raw_data)
		joints = dict()
		for row in joint_raw_data:
			joints[int(row[0])] = tuple(float(v) for v in row[1:])
		beams = dict()
		for row in beam_raw_data:
			beams[int(row[0])] = tuple(int(v) for v in row[1:])

		self.joints = joints
		self.beams = beams

		self.calc_force()


	def calc_force(self):
		connections = dict()
		for beam_num, joint_list in self.beams.items():
			ja = joint_list[0]
			jb = joint_list[1]
			if ja in connections.keys():
				# print(connections)
				connections[ja].append(jb)
			else:
				connections.update({ja:[jb]})
			if jb in connections.keys():
				connections[jb].append(ja)
			else:
				connections.update({jb:[ja]})

		M = sprs.csc_matrix((len(self.joints)*2,len(self.joints)*2),
			dtype=numpy.float32)
		for joint, connectors in connections.items():
			for ji in connectors:
				M[(joint - 1)*2, (ji - 1)*2] = 1
				M[(joint - 1)*2 + 1, (ji - 1)*2 + 1] = 1
		print(M.todense())



	def PlotGeometry(self):
		lines = []
		for beam_num, joint_list in self.beams.items():
			Ja = tuple(self.joints[joint_list[0]][0:2])
			Jb = tuple(self.joints[joint_list[1]][0:2])
			line = plt.Line2D(Ja, Jb, lw=1)
			plt.gca().add_line(line)
		plt.axis('auto')
		plt.show()