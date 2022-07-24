import numpy as np
import matplotlib.pyplot as plt

def SurfacePlot_3D(t, X, Y, T):
    # t must be input as the index at which it occurs
    fig = plt.figure()
    ax = fig.add_subplot(111, projection = '3d')
    ax.set_box_aspect((2,8,3)) # Change aspect ratio to match bottle dimensions
    im = ax.plot_surface(X, Y, T[:,:,0], rstride=1, cstride=1, 
                         antialiased=False, cmap='plasma')
    cbar = fig.colorbar(im)
    im.set_clim(15, 25) # if not in range, will show as white
    cbar.set_label("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)", labelpad=10)
    cbar.set_ticks(np.arange(np.amin(T[:,:,t]),np.amax(T[:,:,t]+1)))
    plt.xlabel("X distance along bottle (mm)")
    plt.ylabel("Y distance along bottle (mm)", labelpad=20)
    ax.set_zlabel("Temperature of wine (" + u"\N{DEGREE SIGN}" + "C)")
    ax.set_zticks(np.arange(15,26,2))
    plt.savefig("3d plot at time, t = " + str(t) + ".png")
    plt.show()
    return None