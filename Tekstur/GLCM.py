import numpy as np
import cv2
import os
import Gray
import math
from PIL import Image
import concurrent.futures
import time

start_time = time.time()
def glcm(input):
    image = Gray.convert_to_grayscale(input)

    # jarak dan sudut untuk GLCM
    distance = 1
    angle = 0  # 0 derajat (horizontal)

    # Mendapatkan dimensi
    height, width = image.size

    # Membuat GLCM
    level = 256
    image = np.array(image)

    glcm = np.zeros((level, level), dtype=np.uint32)  # Matriks GLCM dengan Grayscale 0-255

    for i in range(width-2):
        for j in range(height-1):
            # Koordinat piksel saat ini
            current_pixel = image[i, j][0]
            
            # Koordinat piksel dalam arah yang diinginkan (misalnya, horizontal)
            neighbor_pixel = image[i, j + distance][0] if angle == 0 else None


            glcm[current_pixel, neighbor_pixel] += 1

    transpose_glcm = np.transpose(glcm)
    glcm += transpose_glcm
    # Normalisasi GLCM
    glcm = glcm.astype(float)
    glcm /= np.sum(glcm)

    vektor = []
    Contrast =0
    Homogenity =0
    Entropy =0
    for i in range(0,255) :
        for j in range(0,255) :
            Contrast += glcm[i][j] * ((i-j)**2)
            Homogenity += glcm[i][j] / (1 + (i-j)**2)
            if glcm[i, j] != 0:
                 Entropy -= glcm[i, j] * math.log(float(glcm[i, j]))

    vektor.append(Contrast)
    vektor.append(Homogenity)
    vektor.append(Entropy)

    return vektor

def cosineAB(vektorA , vektorB):
    atas =0
    bawahA=0
    bawahB=0
    for i in range(3):
        atas += vektorA[i]*vektorB[i]
        bawahA += vektorA[i]*vektorA[i]
        bawahB += vektorB[i]*vektorB[i]
    cosine = atas / (math.sqrt(bawahA) * math.sqrt(bawahB))
    return cosine

def similarity(input_path, dataset_path):
    A = glcm(input_path)
    B = glcm(dataset_path)
    return cosineAB(A, B)
# Test
current_folder = os.path.dirname(os.path.abspath(__file__))
folder_name = 'foto'
folder_path = os.path.join(current_folder, folder_name)
dataset_path = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
input = current_folder + "\input.jpg"  
print(dataset_path)
kemiripan =[]
# with concurrent.futures.ProcessPoolExecutor() as executor:
#         args_list = [(input, x) for x in dataset_path]
#         kemiripan = list(executor.map(similarity, args_list))



for i in range(len(dataset_path)) :
    A = glcm(input)
    B = glcm(dataset_path[i])
    kemiripan.append(cosineAB(A,B))
print(kemiripan)

#runtime
end_time = time.time()
runtime = end_time - start_time
print(f"Runtime: {runtime} seconds")