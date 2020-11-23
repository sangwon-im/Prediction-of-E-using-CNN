import matplotlib.pyplot as plt
import numpy as np
import time

# This import registers the 3D projection, but is otherwise unused.
# from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import

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
    
    
# def explode(data):
#     size = np.array(data.shape)*2
#     data_e = np.zeros(size - 1, dtype=data.dtype)
#     data_e[::2, ::2, ::2] = data
#     return data_e

# def plot_voxel(voxel):
#     # build up the numpy logo
#     facecolors = np.where(voxel, '#FFD65DC0', '#7A88CCC0')
#     edgecolors = np.where(voxel, '#BFAB6E', '#7D84A6')
#     filled = np.ones(voxel.shape)

#     # upscale the above voxel image, leaving gaps
#     filled_2 = explode(filled)
#     fcolors_2 = explode(facecolors)
#     ecolors_2 = explode(edgecolors)

#     # Shrink the gaps
#     x, y, z = np.indices(np.array(filled_2.shape) + 1).astype(float) // 2
#     x[0::2, :, :] += 0.05
#     y[:, 0::2, :] += 0.05
#     z[:, :, 0::2] += 0.05
#     x[1::2, :, :] += 0.95
#     y[:, 1::2, :] += 0.95
#     z[:, :, 1::2] += 0.95

#     fig = plt.figure()
#     ax = fig.gca(projection='3d')
#     ax.voxels(x, y, z, filled_2, facecolors=fcolors_2, edgecolors=ecolors_2)

#     plt.show()
    