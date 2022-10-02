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
    if type == "basic":
        T, intervals, final = Basic(const, t_final, T_BC)
    
    if type == "B":
        T, intervals, final = Bordeaux(const, t_final, T_BC)
        # print("Feature not implemented yet")
        # exit()
        
    return T, intervals, final

def Basic(const, t_final, T_BC):
    h = const[2]
    k = const[1]
    length = 75
    height = 300
    neck_diam = 27.5
    main_length = 185
    
    x_intervals = int((height)/h)
    y_intervals = int((length)/h)
    t_intervals = int((t_final)/k)
    intervals = [x_intervals, y_intervals, t_intervals]
    
    T = np.zeros((x_intervals + 1, y_intervals + 1, t_intervals + 1))
    T_initial = T_BC[0]
    T_cooler = T_BC[1]
    
    T[:,:,0] = T_initial # ICs
    for i in range(x_intervals+1):
        for j in range(y_intervals+1):
            x = i * h
            y = j * h
            if x < main_length:
                T[i,j,:] = T_initial
            elif (y < ((length/2)+(neck_diam/2))) and (y > ((length/2)-(neck_diam/2))):
                T[i,j,:] = T_initial
            else:
                T[i,j,:] = T_cooler
    
    T[0,:,:] = T_cooler #(x = 0)
    T[-1,:,:] = T_cooler #(x = length)
    T[:, 0, :] = T_cooler #(y=out_diam)
    T[:, -1, :] = T_cooler #(y=0)
    
    final = [height, length]
    
    return T, intervals, final

def Bordeaux(const, t_final, T_BC):
    h = const[2]
    k = const[1]
    length = 75
    height = 300
    neck_diam = 27.5
    main_length = 185
    
    height = 320
    neck_diam = 27.5
    length = 75
    straight_height = 185
    curved_horizontal_radius = 0.5 * (length - neck_diam)
    
    x_intervals = int((height)/h)
    y_intervals = int((length)/h)
    t_intervals = int((t_final)/k)
    intervals = [x_intervals, y_intervals, t_intervals]
    
    T = np.zeros((x_intervals + 1, y_intervals + 1, t_intervals + 1))
    T_initial = T_BC[0]
    T_cooler = T_BC[1]
    
    T[:,:,0] = T_cooler # ICs
    
    right_neck_y = ((length/2)+(neck_diam/2))
    left_neck_y = ((length/2)-(neck_diam/2))
    for i in range(x_intervals+1):
        for j in range(y_intervals+1):
            x = i * h
            y = j * h
            # Main body
            if x < main_length:
                T[i,j,:] = T_initial
                
            # Basic neck
            elif (y < right_neck_y) and (y > left_neck_y):
                T[i,j,:] = T_initial
                
            # Curved necks (modelled as a quarter circle)
            elif x < (main_length + curved_horizontal_radius):
                if curved_horizontal_radius**2 > ((x-main_length)**2 + (y-left_neck_y)**2):
                    T[i,j,:] = T_initial
                if curved_horizontal_radius**2 > ((x-main_length)**2 + (y-right_neck_y)**2):
                    T[i,j,:] = T_initial
            else:
                # print(x,y)
                T[i,j,:] = T_cooler
    
    T[0,:,:] = T_cooler #(x = 0)
    T[-1,:,:] = T_cooler #(x = length)
    T[:, 0, :] = T_cooler #(y=out_diam)
    T[:, -1, :] = T_cooler #(y=0)
    
    final = [height, length]
    
    return T, intervals, final


# Not currently implemented, requires changes to the height
def BordeauxHighShoulder(const, t_final, T_BC):
    h = const[2]
    k = const[1]
    length = 75
    height = 300
    neck_diam = 27.5
    main_length = 185
    
    height = 320
    neck_diam = 27.5
    length = 75
    straight_height = 185
    curved_horizontal_radius = 0.5 * (length - neck_diam)
    
    x_intervals = int((height)/h)
    y_intervals = int((length)/h)
    t_intervals = int((t_final)/k)
    intervals = [x_intervals, y_intervals, t_intervals]
    
    T = np.zeros((x_intervals + 1, y_intervals + 1, t_intervals + 1))
    T_initial = T_BC[0]
    T_cooler = T_BC[1]
    
    T[:,:,0] = T_cooler # ICs
    
    right_neck_y = ((length/2)+(neck_diam/2))
    left_neck_y = ((length/2)-(neck_diam/2))
    for i in range(x_intervals+1):
        for j in range(y_intervals+1):
            x = i * h
            y = j * h
            # Main body
            if x < main_length:
                T[i,j,:] = T_initial
                
            # Basic neck
            elif (y < right_neck_y) and (y > left_neck_y):
                T[i,j,:] = T_initial
                
            # Curved necks (modelled as a quarter circle)
            elif x < (main_length + curved_horizontal_radius):
                if curved_horizontal_radius**2 > ((x-main_length)**2 + (y-left_neck_y)**2):
                    T[i,j,:] = T_initial
                if curved_horizontal_radius**2 > ((x-main_length)**2 + (y-right_neck_y)**2):
                    T[i,j,:] = T_initial
            else:
                # print(x,y)
                T[i,j,:] = T_cooler
    
    T[0,:,:] = T_cooler #(x = 0)
    T[-1,:,:] = T_cooler #(x = length)
    T[:, 0, :] = T_cooler #(y=out_diam)
    T[:, -1, :] = T_cooler #(y=0)
    
    final = [height, length]
    
    return T, intervals, final