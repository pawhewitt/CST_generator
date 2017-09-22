# CST generator
import sys,os
from optparse import OptionParser
sys.path.append(os.environ['SU2_RUN'])
import SU2 # import all the python scripts in /usr/local/SU2_RUN/SU2_PY/SU2
import matplotlib.pyplot as plt

def main():

	parser=OptionParser()
	parser.add_option("-f",dest="filename",default="mesh_NACA0012_inv.su2")

	(options, args)=parser.parse_args()

	# read coordinates
	Read(options.filename) # mesh/DAT filename

	# compute the coefficients
	Compute_Coeff()

	# write output
	Write_File() 

	# plot the points showing how the foils differ and by how much
	Plot()

	# re-mesh geometry
	Re_Mesh()

def Read(filename):
	# check the type of file extension
	# if it's a SU2 config file then look for the mesh file listed in it
	# then read and store the surface points from this mesh file
	# If it's a dat file read and store the points.
	# Store these points in an array called Coords[][] make this Public is possible

	# Using the Su2 python scripts for reading mesh
		meshdata=SU2.mesh.tools.read(filename) # read the mesh
		# sort airfoil coords to be arrange clockwise from trailing edge
		points,loop=SU2.mesh.tools.sort_airfoil(meshdata,'airfoil')
		# get the points for the surface marker
		foil_points,foil_nodes=SU2.mesh.tools.get_markerPoints(meshdata,'airfoil')
		
		for i in range(len(points)):
			coords[i]=foil_points[points[i]]
		Plot(coords)
		
		return

def Compute_Coeff():

	def Bi_Coeff(): 
		#compute the binomial coeffient
		return
	def C_n1n2(): 
		# class function
		return
	def Shape(): 
		# shape function
		return
	def CST(): 
		# evaluate the CST function
		return
	def L2(): 
		# Calulate the current L2 norm 
		return
	def opt_L2(): 
		# Optimise the coeffient values to minimise the L2 norm value.
		return

def Write_File(): 
	# Write a file containing the coefficients 
	return
def Re_Mesh(): # Mesh the geometry according to the CST approximation.
	# for the SU2 option use the SU2_DEF code and for the dat file use the
	# gmesh generator 
	return 
def Plot(coords):
	plt.plot(coords[1],coords[2])
	plt.show()
	return
# this is only accessed if running from command prompt
if __name__ == '__main__':
    main()
