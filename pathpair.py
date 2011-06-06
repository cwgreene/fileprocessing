import os
import sys
import re

print "yo"
def pairwith(directory):
	extensions  = ["svg","txt"]
	files = {}
	for ext in extensions:
		files[ext] = []

	for file in os.listdir(directory):
		for ext in extensions:
			if re.match("[^\.]*\."+ext,file):
				files[ext].append(file)

	pairs = []
	for svgfile in files["svg"]:
		#get number
		print svgfile
		num,mag = re.findall("random([0-9]+)_(.*)\.svg",svgfile)[0]
		print svgfile,num,mag
		for txtfile in files["txt"]:
			if re.match("Random"+num+"_"+mag+"\.txt$",txtfile):
				pairs.append((svgfile,
						os.path.join(directory,txtfile)))
				break
	return pairs

def pixelsize(txtfile):
	for line in open(txtfile):
		if line.find("PixelSize") != -1:
			tag,value=line.split("=")
			return float(value)

if __name__ == "__main__":
	print map(pixelsize,pairwith(sys.argv[1]))
