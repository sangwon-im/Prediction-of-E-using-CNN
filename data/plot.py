import matplotlib.pyplot as plt
import numpy as np
import time

def plot_voxel(voxels, filename):
    start = time.time()
    
    colors = np.where(voxels, "blue", "red")
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    
    template = np.ones(voxels.shape, dtype=object)
    ax.voxels(template, facecolors=colors, edgecolor='k')
    ax.set(xlabel='x', ylabel='y', zlabel='z')
    
    print("ploting time:", time.time()-start)
    # plt.show()
    plt.savefig(f'processed/mesh_image/{filename}.png')
    
