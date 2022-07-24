# Import libraries
import matplotlib.pyplot as plt
import numpy as np
from graphing import SurfacePlot_3D
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
const = [r, k]

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
    fig = plt.figure()
    plt.plot(t,T[int((body_length/(2*h))), int(out_diam/(2*h)),:])
    plt.xlabel("Time, t")
    plt.ylabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    plt.yticks(np.arange(15,26))
    plt.savefig("Scatter graph")
    plt.show()
    
    
    SurfacePlot_3D(0, X, Y, T)

    ## Contour plot at t = 0s
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.contourf(X,Y,T[:,:,0],cmap='plasma', levels= np.arange(15,25.1,0.1)) # vmax=25
    cbar = fig.colorbar(im)
    im.set_clim(15, 25) # if not in range, will show as white
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,0]),np.amax(T[:,:,0])+1))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,100,25)) # Added for clarity when viewing plot
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)")
    plt.savefig("Contour plot t0")
    plt.show()

    ## 3D plot at t = 10s
    index_10s  = int(10/k) # index at which t=10 occurs
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_box_aspect((2,8,3)) # Change aspect ratio to match bottle dimensions
    im = ax.plot_surface(X, Y, T[:,:,index_10s], rstride=1, cstride=1, 
                         antialiased=False, cmap='plasma')
    cbar = fig.colorbar(im)
    im.set_clim(15, np.amax(T[:,:,index_10s])) 
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,index_10s]),np.amax(T[:,:,index_10s]+1)))
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)", labelpad=20)
    ax.set_zlabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    ax.set_zticks(np.arange(np.amin(T[:,:,index_10s]), np.amax(T[:,:,index_10s])+1, 2))
    plt.savefig("3d plot t10.png")
    plt.show()

    ## Contour plot at t = 10s
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.contourf(X,Y,T[:,:,index_10s],cmap='plasma', levels= np.arange(15,25.1,0.1))
    cbar = fig.colorbar(im)
    im.set_clim(15, 25) # if not in range, will show as white
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,index_10s]),np.amax(T[:,:,index_10s]+1)))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,100,25)) # Added for clarity when viewing plot
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)")
    plt.savefig("Contour plot t10")
    plt.show()
    
    ## 3D plot at t = 100s
    index_100s  = int(100/k) # index at which t=10 occurs
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_box_aspect((2,8,3)) # Change aspect ratio to match bottle dimensions
    im = ax.plot_surface(X, Y, T[:,:,index_100s], rstride=1, cstride=1, 
                         antialiased=False, cmap='plasma')
    cbar = fig.colorbar(im)
    im.set_clim(15, np.amax(T[:,:,index_100s]))
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,index_100s]),np.amax(T[:,:,index_100s]+1)))
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)", labelpad=20)
    ax.set_zlabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    ax.set_zticks(np.arange(np.amin(T[:,:,index_100s]), np.amax(T[:,:,index_100s])+1, 2))
    plt.savefig("3d plot t100.png")
    plt.show()

    ## Contour plot at t = 100s
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.contourf(X,Y,T[:,:,index_100s],cmap='plasma', levels= np.arange(15,25.1,0.1))
    cbar = fig.colorbar(im)
    im.set_clim(15, np.amax(T[:,:,index_100s]))
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,index_100s]),np.amax(T[:,:,index_100s]+1)))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,100,25)) # Added for clarity when viewing plot
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)")
    plt.savefig("Contour plot t100")
    plt.show()

    ## Plot 3d plot at t = 3600s
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_box_aspect((2,8,4)) # Change aspect ratio to match bottle dimensions
    im = ax.plot_surface(X, Y, T[:,:,-1],rstride=1,cstride=1,cmap='plasma', antialiased=False)
    im.set_clim(15,16)
    cbar = fig.colorbar(im)
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(15,16.2,0.2))
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)", labelpad=20)
    ax.set_zlabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    ax.set_zticks(np.arange(15,16.1,0.2))
    plt.savefig("Surface plot t3600")
    plt.show()
    
    ## Contour plot at t = 3600s
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.contourf(X,Y,T[:,:,-1],cmap='plasma', levels= np.arange(15,16.1,0.1))
    cbar = fig.colorbar(im)
    im.set_clim(15, np.amax(T[:,:,-1]))
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,-1]),np.amax(T[:,:,-1]+1)))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,100,25)) # Added for clarity when viewing plot
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)")
    plt.savefig("Contour plot t100")
    plt.show()   

else:
    print("Convergence will not occur so aborted program.")

print('CW done: I deserve a good mark')