#process svg documents and extract all lines,
#list their lengths in pixels
import sys

from lxml import etree
from math import sqrt

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
		return sum([sqrt(x*x+y*y) for x,y in self.points])


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

#below is useful for working out how
#lxml represents various tag namespaces
def printtags(filename):
	tree = etree.parse(filename)
	print dir(tree)
	for v in tree.iter():
		print v.tag


print [line.length() for line in get_lines(sys.argv[1])]
