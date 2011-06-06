#process svg documents and extract all lines,
#list their lengths in pixels
import sys
import os
import re

import numpy as np
import matplotlib.pyplot as plt

from lxml import etree
from math import sqrt


import pathpair

svgns = "http://www.w3.org/2000/svg"

class Line(object):
	def __init__(self,svgobject):
		points_string = svgobject.get("d")
		#get rid of leading "M "
		points_string = points_string[2:]
		pointslist = points_string.split(" ")
		self.points = [(float(x),float(y)) 
				for x,y in [point.split(",") 
						for point in pointslist]]
				

	def length(self):
		first = self.points[:-1]
		second = self.points[1:]
		return sum([sqrt((x2-x1)**2+(y2-y1)**2) 
			for x1,y1 in first
			for x2,y2 in second])


def get_lines(filename,state={'failures':0}):
	print filename
	tree = etree.parse(filename)
	lines = []
	for v in tree.findall("//{"+svgns+"}path"):
		try:
			lines.append(Line(v))
		except:
			state["failures"]+=1
			print state["failures"]
	return lines

def display(lines):
	plt.show()

#below is useful for working out how
#lxml represents various tag namespaces
def printtags(filename):
	tree = etree.parse(filename)
	print dir(tree)
	for v in tree.iter():
		print v.tag

def handle_directory(dirname):
	lines =[]
	print "HERE"
	print pathpair.pairwith(dirname)
	svgpairs = dict(pathpair.pairwith(dirname))
	print svgpairs

	
	files = [file for file in os.listdir(dirname)
			if re.match(".*\.svg$",file)]
	areas = []

	for filename in files:
		file = os.path.join(dirname,filename)
		pixellength=pathpair.pixelsize(svgpairs[filename])
		areas.append(640*480*pixellength**2)
		lines += [line.length() *pixellength*.001
				for line in get_lines(file)]
	if files == []:
		print "no files"
		return
	print np.mean(lines)
	plt.hist(lines,bins=30, normed=True,
			weights=np.ones(len(lines)))

def handle_directories(dirlist):
	i=0
	for dir in dirlist:
		handle_directory(dir)
		plt.savefig('test'+str(i)+'.png')
		i+=1
	plt.show()

handle_directories(sys.argv[1:])
