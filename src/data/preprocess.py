import os
import numpy as np
import plot
from multiprocessing import Process
import pickle
import json

def read_file_num(subdir):
    path_dir = os.getcwd() + "/" + subdir
    file_list = [int(x.split(".")[0]) for x in os.listdir(path_dir)]
    return file_list

def read_data(filename):
    with open(filename, "r") as f:
        data = f.read().split()
    return data

def read_json(filename):
    with open(filename, "r") as f:
        data = json.load(f)
    return data
    
def extract_image(data):
    size = int(data[data.index("sizing") + 2])    
    data = [x for x in data if x != "c"]
    
    meshsize = int(data[data.index("sizing") + 2])
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
    
    except ValueError:
        # phase 2 가 없으면 다 matrix
        matrix = [i+1 for i in range(meshsize)]
        void = []
    
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
    image = mesh_3d.reshape(30,30,30,1)
    
    return image
    

def extract_label(data):
    E_1 = data["E1"]
    E_2 = data["E2"]
    E_3 = data["E3"]
    return np.array([E_1, E_2, E_3]).reshape(3,1)
    
# analysis 에 있는 데이터를 processed numpy array 로 바꾼다
def generate_dataset(start, end):
    """
    docstring
    """
    # file_nums = read_file_num("raw/analysis/")
    # file_nums.sort()
    # for file_num in file_nums:
    images = []
    labels_11 = []
    labels_22 = []
    labels_33 = []
    
    error = []
    
    for i in range(start, end+1):
        try:
            image = read_data("raw/analysis/" + str(i) +".dat")
            label = read_json("raw/properties/" + str(i) +".json")
            
            image = extract_image(image)  
            label = extract_label(label)      

            print(i, image.shape, label.shape)
            
            images.append(image)
            labels_11.append(label[0])
            labels_22.append(label[1])
            labels_33.append(label[2])
        
        # if file_num % 1000 == 1:
        #     plot.plot_voxel(image.reshape(30,30,30), file_num)
        except FileNotFoundError:
            error.append(i)
    
    if len(error) > 0:
        for i in error:
            print(f"file {i} not found")
    
    return np.array(images), np.array(labels_11), np.array(labels_22), np.array(labels_33)


# total data
# while True:
    # start = int(input("start: "))
    # end = int(input("end: "))
    # if end - start > 0:
    #     break
    
print("Total data")
end = int(input("end: "))
image, label_11, label_22, label_33 = generate_dataset(1,end)

with open('processed/image.pkl', 'wb') as f:
    pickle.dump(image, f)

with open('processed/label_11.pkl', 'wb') as f:
    pickle.dump(label_11, f)
with open('processed/label_22.pkl', 'wb') as f:
    pickle.dump(label_22, f)
with open('processed/label_33.pkl', 'wb') as f:
    pickle.dump(label_33, f)