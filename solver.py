import matplotlib.pyplot as plt
import numpy as np

# Solve for t > 0 using the Finite Difference Method (FDM)
def FDM(T, intervals, const):
    Found = False
    # Extract info from inputs
    x_intervals = intervals[0]
    y_intervals = intervals[1]
    t_intervals = intervals[2]
    
    
    r = const[0]
    k = const[1]
    
    # Solve for t > 0 using the Finite Difference Method (FDM)
    for t in range(1, t_intervals + 1):
        for i in range(1,x_intervals):
            for j in range(1,y_intervals):
                # Skip the points where boundary conditions occur
                if T[i,j,t] == False:
                    continue
                
                # Apply solution for FDM (1D in time, 2D in space)
                T[i,j,t] = (1 - 4*r)*(T[i,j,t-1]) + r*(T[i-1,j,t-1] + T[i+1, j, t-1] + T[i, j-1, t-1] + T[i, j+1, t-1])
                
        # Check if midbody temperature is below 16 degrees Celsius
        if (np.amax(T[:, :, t]) < 16) and not Found:
            t_crit = t * k # Actual time value
            Found = True
            print("At ", str(t_crit), " seconds, the wine is in the acceptable range")
    
    return T, Found