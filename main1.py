# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from graphing import SurfacePlot_3D, ContourPlot, TempDistnAtPoint
from solver import FDM

# Solving a PDE of wine bottle inside a cooler
# Heat diffusion equation: T_t = alpha(u_xx + u_yy) 

# Define wine bottle constants (lengths in mm)
length = 300
out_diam = 75
in_diam = 25
body_length = 200
initial_wine_temp = 25

# PDE constants
# alpha = 0.392 # thermal diffusivity of wine (mm2/s)
alpha = 0.1
k = 1 # time step
h = 1 # x and y step
r = alpha*k/h**2 
const = [r, k, h] 

# Check if convergence will occur
def Convergence(r):
    conv = r<=0.25 
    return conv

converging = Convergence(r)

# Only implement the model if convergence occurs
if converging:
    Found = False # Used to determine if temp in acceptable range
    
    # Define domain ranges of x, y & t
    x_final = length
    y_final = out_diam
    t_final = 3600

    # Determine number of intervals required
    x_intervals = int(x_final/h)
    y_intervals = int(y_final/h)
    t_intervals = int(t_final/k)
    intervals = [x_intervals, y_intervals, t_intervals]

    # Discretise domain and create empty array of specificed size for (x,y,t)
    T = np.zeros((x_intervals + 1, y_intervals + 1, t_intervals + 1))

    # Initial Conditions & Implementation
    T_initial = 25
    T[:, :, 0] = T_initial

    # Boundary Conditions & Implementation
    T_cooler = 15
    left_bc = T_cooler #(x = 0)
    right_bc = T_cooler #(x = length)
    top_bc = T_cooler #(y = out_diam)
    bottom_bc = T_cooler #(y=0)

    T[0,:,:] = left_bc #(x = 0)
    T[-1,:,:] = right_bc #(x = length)
    T[:, 0, :] = top_bc #(y=out_diam)
    T[:, -1, :] = bottom_bc #(y=0)

    ## Define indexes required for neck boundaries
    neck_lower_index = int((0.5 * (y_final - in_diam)) / h) # neck bottom y value
    neck_upper_index = int((0.5 * (y_final + in_diam)) / h) # neck top y value
    left_neck_index = int(body_length / h) # neck and body boundary x value
    indices = [neck_lower_index, neck_upper_index, left_neck_index]

    ## Implement BC to cooler region within control volume
    for i in range(left_neck_index, x_intervals + 1):
        for j in range(0,y_intervals + 1):
            if (j > neck_upper_index) or (j < neck_lower_index):
                T[i,j,:] = T_cooler # if in the cooler region apply BC    
    
    
    # Solve for t > 0 using the Finite Difference Method (FDM)
    T = FDM(T, intervals, indices, const)

    # GRAPHING
    ## Set up arrays for graphing
    X = np.linspace(0, x_final + h, len(T[:,:,0]))
    Y = np.linspace(0, y_final + h, len(T[:,:,0][0]))
    X, Y = np.meshgrid(Y, X) 
    t = np.arange(0,t_final+k,k)
    
    ## Plot Temperature at midpoint of main body against time
    point = [int((body_length/(2*h))), int(out_diam/(2*h))]
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