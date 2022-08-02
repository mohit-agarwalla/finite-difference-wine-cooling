# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from graphing import SurfacePlot_3D, ContourPlot, TempDistnAtPoint
from solver import FDM
from shape import WineBottle

# Solving a PDE of wine bottle inside a cooler
# Heat diffusion equation: T_t = alpha(u_xx + u_yy) 

# Define wine bottle constants (lengths in mm)
# length = 300
# out_diam = 75
# in_diam = 25
# body_length = 200
# initial_wine_temp = 25

# PDE constants
alpha = 0.392 # thermal diffusivity of wine (mm2/s)
# alpha = 0.1
k = 1 # time step
h = 4 # x and y step
r = alpha*k/h**2 
const = [r, k, h] 
t_final = 3600
# Check if convergence will occur
def Convergence(r):
    conv = r<=0.25 
    return conv

converging = Convergence(r)

# Only implement the model if convergence occurs
if converging:
    T_BC = [25, 15]
    T, pos, intervals, final = WineBottle("B", const, t_final=3600, T_BC=T_BC)

    # Solve for t > 0 using the Finite Difference Method (FDM)
    T, Found = FDM(T, intervals, const)


    x_final = final[0]
    y_final = final[1]
    # GRAPHING
    ## Set up arrays for graphing
    X = np.linspace(0, x_final + h, len(T[:,:,0]))
    Y = np.linspace(0, y_final + h, len(T[:,:,0][0]))
    X, Y = np.meshgrid(Y, X) 
    t = np.arange(0,t_final+k,k)
    
    ## Plot Temperature at midpoint of main body against time
    point = [int((intervals[0]/(2*h))), int(intervals[1]/(2*h))]
    TempDistnAtPoint(t, point, T, "midpoint")
    
    # Graphs for t=0s
    SurfacePlot_3D(0, k, X, Y, T)
    ContourPlot(0, k, X, Y, T) 
    
    # Graphs for t=10s
    SurfacePlot_3D(10, k, X, Y, T)
    ContourPlot(10, k, X, Y, T) 
    
    # Graphs for t=100s
    SurfacePlot_3D(100, k, X, Y, T)
    ContourPlot(100, k, X, Y, T) 
    
    # Graphs for t=3600s
    SurfacePlot_3D(3600, k, X, Y, T)
    ContourPlot(3600, k, X, Y, T)   

else:
    print("Convergence will not occur so aborted program.")

# print('CW done: I deserve a good mark')