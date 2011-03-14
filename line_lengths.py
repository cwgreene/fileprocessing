#process svg documents and extract all lines,
#list their lengths in pixels
from lxml import etree

def get_lines(filename="test.xml"):
	tree = etree.parse(filename)
	result = []
	for v in tree.findall("//line"):
		print v.tag
		print v.get("value")
get_lines()
