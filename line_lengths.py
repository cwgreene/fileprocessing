#process svg documents and extract all lines,
#list their lengths in pixels
import lxml

def get_lines(filename="test.xml"):
	tree = lxml.ElementTree.parse(filename)
	result = []
	for v in tree.findall("//line"):
		print v.value
get_lines()
