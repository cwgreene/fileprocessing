#process svg documents and extract all lines,
#list their lengths in pixels
import sys

from lxml import etree
from math import sqrt

svgns = "http://www.w3.org/2000/svg"

class Line(object):
	def __init__(self,svgobject):
		pointsstring = svgobject.get("d")
		#get rid of leading "M "
		pointsstring = pointstring[2:]
		pointslist = map(float,pointsstring.split(","))
		self.points = [(x,y) 	for x in pointslist[::2] 
					for y in pointslist[1::2]]

	def length(self):
		return sum([sqrt(x*x+y*y) for x,y in self.points])


def get_lines(filename):
	print filename
	tree = etree.parse(filename)
	lines = []
	print "tag",tree.getroot().tag
	for v in tree.findall("//{"+svgns+"}path"):
		print v.get("style")
#		lines.append(Line(v))
	return lines

#below is useful for working out how
#lxml represents various tag namespaces
def printtags(filename):
	tree = etree.parse(filename)
	print dir(tree)
	for v in tree.iter():
		print v.tag


printtags(sys.argv[1])
print [line.length() for line in get_lines(sys.argv[1])]
