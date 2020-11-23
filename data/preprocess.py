import os
import numpy as np
import plot
import json

def read_filename(subdir):
    path_dir = os.getcwd() + "/" + subdir
    file_list = [x for x in os.listdir(path_dir)]
    return file_list

def read_data(filename):
    with open(filename, "r") as f:
        data = f.read().split()
    return data

def extract(data):
    size = int(data[data.index("sizing") + 2])    
    data = [x for x in data if x != "c"]
    
    n_elements = int(data[data.index("sizing") + 2])
    # n_nodes = int(data[data.index("sizing") + 3])
    
    try:
        idx1 = data.index("Phase1") + 1
        idx2 = data.index("Phase2") - 3
        # define element set Phase2

        matrix_size = idx2 - idx1
        void_size = size - matrix_size

        idx3 = data.index("Phase2") + 1
        idx4 = idx3 + void_size

        matrix = list(map(int, data[idx1:idx2]))
        void = list(map(int, data[idx3:idx4]))
        return (matrix, void, n_elements)
    
    except ValueError:
        # phase 2 가 없으면 다 matrix
        matrix = [i+1 for i in range(n_elements)]
        void = []
        return (matrix, void, n_elements)
    
    
if __name__ == "__main__":
    ## initialize ##
    # /analysis 폴더에 접근
    filenames = read_filename("raw/analysis/")
    meshlist = {}

    for filename in filenames:
        data = read_data("raw/analysis/" + filename)
        
        # matrix 는 차있는 부분 좌표 (1차원에서)
        # void 는 비어있는 부분 좌표 (1차원에서)
        matrix, void, meshsize = extract(data)
        print("meshsize:", meshsize)
        
        meshsize_x = round(meshsize ** (1.0/3.0))
        
        mesh = [-1 for i in range(meshsize)]
        
        # matrix, void 는 1부터 시작이므로 1씩 빼줘야 적절한 index 이다
        for i in matrix:
            mesh[int(i)-1] = 1
            
        for i in void:
            mesh[int(i)-1] = 0
        
        # print(mesh)
        mesh = np.array(mesh)
        mesh_3d = mesh.reshape(meshsize_x, meshsize_x, meshsize_x)
        
        # digimat 과 같은 모양으로 voxel 회전
        mesh_3d = np.flip(mesh_3d, axis=2)
        mesh_3d = np.rot90(mesh_3d, 1, (0,2))
        
        # plot
        file_num = int(filename[:-4])
        plot.plot_voxel(mesh_3d, file_num)
        
        # 딕셔너리에 추가
        meshlist[file_num] = mesh_3d.tolist()
    
    print(meshlist[1])
        
    # 딕셔너리를 직렬화 해서 json 에 저장
    with open("processed/mesh.json", "w") as f:
        json.dump(meshlist, f)