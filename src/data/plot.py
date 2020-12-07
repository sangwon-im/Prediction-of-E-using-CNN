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
    
    # plt.show()
    plt.savefig(f'processed/mesh_image/{filename}.png')    

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    temp = np.where(voxels, False, True)
    ax.voxels(temp, facecolors=colors, edgecolor='k')
    ax.set(xlabel='x', ylabel='y', zlabel='z')
    plt.savefig(f'processed/mesh_image/{filename}_pole.png')    
    print("ploting time:", time.time()-start)