import numpy as np
import matplotlib.pyplot as plt

"""
This script should create a bottle and the required params by decoding the input for a bottle type.

The following bottles are currently supported: Bordeaux (750ml).

Dimensions were taken from: {
Bordeaux (750ml): https://www.ledomduvin.com/2017/10/bottle-dimensions.html,
}
"""

# Define wine bottle constants (lengths in mm)
length = 300
out_diam = 75
in_diam = 25
body_length = 200
initial_wine_temp = 25

def WineBottle(type, const, t_final, T_BC):
    if type == "B":
        T, pos, intervals, final = Bordeaux(const, t_final, T_BC)
    
    if type == "basic":
        T, pos, intervals, final = Basic(const, t_final, T_BC)
        
    return T, pos, intervals, final

def Bordeaux(const, t_final, T_BC):
    """
    This script will produce a Bordeaux bottle.
    """
    # Constants
    height = 320
    neck_diam = 27.5
    width = 75
    punt_h = 19
    punt_w = 65
    straight_h = 185
    curved_h = 45
    final = [width, height]
    h = const[2]
    k = const[1]
    x_intervals = int(length/h)
    y_intervals = int(width/h)
    t_intervals = int(t_final/k)
    intervals = [x_intervals, y_intervals, t_intervals]
    print(intervals)
    
    # Discretise Domain
    T = np.zeros((x_intervals + 1, y_intervals + 1, t_intervals + 1))
    
    T_initial = T_BC[0]
    T_cooler = T_BC[1]
    
    T[:,:,0] = T_initial
    pos = np.zeros((x_intervals + 1, y_intervals + 1)) # Array to tell whether bottle exists or not
    
    for i in range(x_intervals+1):
        for j in range(y_intervals+1):
            x = i * h
            y = j * h
            
            
            
    
    countFalse = 0
    countTrue = 0
    
    # Set BCs and ICs
    T[:,:,0] = T_initial # ICs
    pos = np.zeros((x_intervals + 1, y_intervals + 1)) # Array to tell whether bottle exists or not
    for i in range(x_intervals+1):
        for j in range(y_intervals+1):
            x = i * h
            y = j * h
            left_neck_x = (width - neck_diam)/2
            # Check if in the top straight region
            if (x > (straight_h + curved_h)):
                print("In straight top region")
                if (y > ((width/2) - (neck_diam/2))) and (y < ((width/2) + (neck_diam/2))):
                    pos[i][j] = True
                    countTrue += 1
                else:
                    pos[i][j] = False
                    countFalse += 1                    
            
            # Deal with curved region, modelled as 
            
            elif (x > straight_h) and (x < (straight_h + curved_h)):
                if y < ((width/2) - (neck_diam/2)):
                    if ((((x - straight_h)**2)/curved_h) + (((y - left_neck_x)**2)/left_neck_x)) < 1:
                        pos[i][j] = True
                elif y > ((width/2) + (neck_diam/2)):
                    continue
                else:
                    pos[i][j] = True
                    countTrue += 1
            
            # main body is true
            elif x > punt_h and y < straight_h:
                pos[i][j] = True
                countTrue += 1
                            
            # If in punt area false
            elif ((((y-(width/2))**2)/(punt_w/2)**2) + (((y-(width/2))**2)/(punt_w/2)**2)) < 1:
                pos[i][j] = False
                countFalse += 1
            
            elif (y > ((width/2) + (punt_w/2))) or (y < ((width/2) - (punt_w/2))):
                if x < straight_h:
                    pos[i][j] = True
                    countTrue += 1
                
            else:
                pos[i][j] = False
                countFalse += 1
    
    T[0,:,:] = T_cooler #(x = 0)
    T[-1,:,:] = T_cooler #(x = length)
    T[:, 0, :] = T_cooler #(y=out_diam)
    T[:, -1, :] = T_cooler #(y=0)       
    
    
    
    for i in range(x_intervals + 1):
        for j in range(y_intervals + 1):
            if pos[i][j] == False:
                T[i,j,:] = T_cooler
            else:
                T[i,j,:] = T_initial    
    
    
    return T, pos, intervals, final

def Basic(const, t_final, T_BC):
    return const, t_final, T_BC