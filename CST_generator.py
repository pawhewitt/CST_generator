# CST generator
import sys,os
from optparse import OptionParser
sys.path.append(os.environ['SU2_RUN'])
import SU2 # import all the python scripts in /usr/local/SU2_RUN/SU2_PY/SU2
import numpy as np
from math import factorial as fac
import matplotlib.pyplot as plt

def main():

	parser=OptionParser()
	parser.add_option("-f",dest="Filename",default="mesh_NACA0012_inv.su2")
	parser.add_option("-o",dest="Order",default="3")
	parser.add_option("--n1",dest="n1",default="0.5")
	parser.add_option("--n2",dest="n2",default="1.0")
	(options, args)=parser.parse_args()
	
	Order=int(options.Order)
	Filename=options.Filename
	n1=float(options.n1)
	n2=float(options.n2)
	# read coordinates
	Coords=Read(options.Filename) # mesh/DAT filename

	# compute the coefficients
	Au,Al,CST_Upper=Compute_Coeffs(Coords,Order,n1,n2)

	# # write output
	# Write_File() 

	# # plot the points showing how the foils differ and by how much
	#Plot(CST_Upper)

	# # re-mesh geometry
	# Re_Mesh()

def Read(Filename):
	# check the type of file extension
	# if it's a SU2 config file then look for the mesh file listed in it
	# then read and store the surface points from this mesh file
	# If it's a dat file read and store the points.
	# Store these points in an array called Coords[][] make this Public is possible

	# Using the Su2 python scripts for reading mesh
	Meshdata=SU2.mesh.tools.read(Filename) # read the mesh
	
	# sort airfoil coords to be arrange clockwise from trailing edge
	Points,Loop=SU2.mesh.tools.sort_airfoil(Meshdata,'airfoil')
	
	# get the points for the surface marker
	Foil_Points,Foil_Nodes=SU2.mesh.tools.get_markerPoints(Meshdata,'airfoil')
	
	# Get the sorted points 
	Coords=np.zeros([200,2])
	for i in range(len(Points)):
		Coords[i][0]=Foil_Points[Points[i]][0]
		Coords[i][1]=Foil_Points[Points[i]][1]
	return Coords

def Compute_Coeffs(Coords,Order,n1,n2):
	# initial coefficents set for upper (u) and lower (l) surfaces
	Au=np.ones(Order+1) # one more than the order
	Al=np.ones(Order+1)*-1 

	# Split Coords into Upper and Lower surfaces
	U_Coords,L_Coords=Split(Coords)

	# Evalulate the CST function for each surface at the given x locations
	CST_Upper=CST(U_Coords,Au,n1,n2)
	CST_Lower=CST(L_Coords,Al,n1,n2)

	return Au,Al,CST_Upper,CST_Lower#,CST_Lower # See how to group this together 

def Bi_Coeff(A): 
	#compute the binomial coefficient
	K=np.zeros(len(A))
	Order=len(K)-1
	for i in range(len(K)):
		K[i]=fac(Order)/(fac(i)*(fac(Order-i)))
	return K


def C_n1n2(Coords,n1,n2): 
	# class function
	C=np.zeros(len(Coords))
	for i in range(len(C)):
		C[i]=(Coords[i][0]**n1)*(1-Coords[i][0]**n2)
	return C

def Total_Shape(Coords,A): 
	# Total shape function
	S=np.zeros(len(Coords))
	# Component Shape Function
	S_c=Comp_Shape(Coords,A)
	x=[]
	# for i in range(len(A)): # order loop 
	# 	for j in range(len(Coords)): # point loop
	#  		S[j]=S[j]+A[i]*S_c[i][j]

	# for i in range(len(Coords)): # point loop
	# 	for j in range(len(A)):
	# 		S[i]+=A[j]*S_c[j][i]



	# for j in range(len(A)):
	# 	S+=np.dot(A,S_c[j]) # Does this make sense?

	
	#for i in range(len(A)):
	#	S=sum(A[]*S_c[i])
	S_c=np.transpose(S_c)
	for  i in range(len(Coords)):
		S[i]+=np.dot(A,S_c[i])

	print np.shape(A)
	print np.shape(S_c)
	# for i in range(len(Coords)):
	# 	x.append(Coords[i][0])
	# Plot(x,S)
	# plt.plot(S)
	# plt.show()
	return S

def Comp_Shape(Coords,A):
	# Component Shape function
	K=Bi_Coeff(A)
	x=[]
	# compute the Binomial Coefficient
	S_c=np.zeros([len(A),len(Coords)])
	for i in range(len(A)): # order loop
		for j in range(len(Coords)): # point loop
			S_c[i][j]=(K[i]*Coords[j][0]**i)*(1-Coords[j][0])**(len(A)-i)
	
	# for i in range(len(Coords)):
	# 	x.append(Coords[i][0])
	# Plot(x,S_c[0])
	return S_c

def CST(Coords,A,n1,n2): 
	CST_vals=np.zeros(len(Coords))
	# Compute Class Function
	C=C_n1n2(Coords,n1,n2)

	# Compute the Shape Function
	S=Total_Shape(Coords,A)
	# evaluate the CST function
	for i in range(len(Coords)):
		CST_vals[i]=C[i]*S[i]

	plt.plot(CST_vals)
	plt.show()

	return CST_vals

def L2(): 
	# Calculate the current L2 norm 
	return

def Opt_L2(): 
	# Optimise the coeffient values to minimise the L2 norm value.
	return

def Split(Coords):
		# Spilt the surfaces according to the z component of there normal
		# TODO split based on normal
		# Might have to added 0,0 point to lower surface
	U_Coords=[]
	L_Coords=[]
	for i in range(len(Coords)):
		if Coords[i][1]<0:
			L_Coords.append(Coords[i])
		else:
			U_Coords.append(Coords[i])

	# Convert to numpy array
	L_Coords=np.array(L_Coords)
	U_Coords=np.array(U_Coords)

	return U_Coords,L_Coords

def Write_File(): 
	# Write a file containing the coefficients 
	return

def Re_Mesh(): # Mesh the geometry according to the CST approximation.
	# for the SU2 option use the SU2_DEF code and for the dat file use the
	# gmesh generator 
	return 

def Plot(x,y):
	plt.plot(x,y)
	plt.show()

	return
# this is only accessed if running from command prompt
if __name__ == '__main__':
    main()
