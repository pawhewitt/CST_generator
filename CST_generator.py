# CST generator

from optparse import OptionParser

def main():

	parser=OptionParser()
	parser.add_option("-f",dest="filename")

	(options, args)=parser.parse_args()

	# read coordinates
	Read(filename)
	print filename

	# compute the coefficients
	Compute_Coeff()

	# write output
	Write_File() 

	# re-mesh geometry
	Re_Mesh()

def Read():
	# check the type of file extension
	# if it's a SU2 config file then look for the mesh file listed in it
	# then read and store the surface points from this mesh file
	# If it's a dat file read and store the points.
	# Store these points in an array called Coords[][] make this Public is possible

def Compute_Coeff():

	def C_n1n2(): # Class function
	def shape function

def Write_File():

def Re_Mesh():

# this is only accessed if running from command prompt
if __name__ == '__main__':
    main()
