import numpy as np
import matplotlib.pyplot as plt

def SurfacePlot_3D(t, k, X, Y, T):
    # t must be input as the index at which it occurs
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_box_aspect((2,8,3)) # Change aspect ratio to match bottle dimensions
    im = ax.plot_surface(X, Y, T[:,:,int(t/k)], rstride=1, cstride=1, 
                         antialiased=False, cmap='plasma')
    cbar = fig.colorbar(im)
    # im.set_clim(15, 25) # if not in range, will show as white
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,t]),np.amax(T[:,:,t]+1)))
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)", labelpad=20)
    ax.set_zlabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    # ax.set_zticks(np.arange(15,26,2))
    plt.title("3D Surface plot at time t = " + str(t))
    plt.savefig(f"graphs\Surface Plot at t = {str(t)}s.png")
    plt.show()
    return None

def ContourPlot(t, k, X, Y, T):
    index = int(t/k)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    im = ax.contourf(X,Y,T[:,:,index],cmap='plasma', levels= np.arange(15,25.1,0.1))
    cbar = fig.colorbar(im)
    im.set_clim(15, 25) # if not in range, will show as white
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,index]),np.amax(T[:,:,index]+1)))
    ax.set_aspect('equal')
    plt.xticks(np.arange(0,100,25)) # Added for clarity when viewing plot
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)")
    plt.title("Contour plot at time t = " + str(t))
    plt.savefig(f"graphs\Contour plot at t = {str(t)}s")
    plt.show()
    return None

def TempDistnAtPoint(t, point, T, descriptor):
    plt.plot(t,T[point[0], point[1],:])
    plt.xlabel("Time, t")
    plt.ylabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    plt.yticks(np.arange(15,26))
    plt.savefig(f"graphs\Temp Distribution at {descriptor}.png")
    plt.show()
    return None 