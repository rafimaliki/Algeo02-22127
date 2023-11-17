import numpy as np
import os
import math
from PIL import Image

def convert_to_grayscale (input_path):
    # Open the image
    image = Image.open(input_path).convert("RGB")

    # Convert to grayscale
    grayscale_image = np.array(image) @ [0.299, 0.587, 0.114]
    grayscale_image = np.stack([grayscale_image] * 3, axis=-1).astype(np.uint8)

    # Create a Pillow Image from the NumPy array
    grayscale_image = Image.fromarray(grayscale_image)

    # Optionally, you can return the compressed image
    return grayscale_image

def glcm(image):
    level = 256

    image_array = np.array(image, dtype=np.uint8)

    glcm = np.zeros((level, level), dtype=np.uint32)

    current_pixels = image_array[:, :-1]
    neighbor_pixels = image_array[:, 1:]

    #Menggunakan NumPy's indexing dan bincount agar kode jauh lebih efisien
    flat_indices = current_pixels * level + neighbor_pixels
    glcm_flat = np.bincount(flat_indices.flatten(), minlength=level**2)
    glcm = glcm_flat.reshape((level, level))

    transpose_glcm = glcm.T
    glcm += transpose_glcm
    glcm = glcm.astype(float) / np.sum(glcm)

    vektor = [
        np.sum(glcm * (np.arange(level).reshape(1, -1) - np.arange(level).reshape(-1, 1)) ** 2),
        np.sum(glcm / (1 + (np.arange(level).reshape(1, -1) - np.arange(level).reshape(-1, 1)) ** 2)),
        -np.sum(glcm[glcm != 0] * np.log(glcm[glcm != 0])),
    ]

    return vektor

def cosineSim(vektorA , vektorB):
    atas =0
    bawahA=0
    bawahB=0
    for i in range(3):
        atas += vektorA[i]*vektorB[i]
        bawahA += vektorA[i]*vektorA[i]
        bawahB += vektorB[i]*vektorB[i]
    cosine = atas / (math.sqrt(bawahA) * math.sqrt(bawahB))
    return round(cosine, 4)


def get_result_image():
    current_folder = os.path.dirname(os.path.abspath(__file__))
    folder_name = 'foto'
    folder_path = os.path.join(current_folder, folder_name)
    dataset_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
    input_path = os.path.join(current_folder, 'inp.jpg')

    # kalkulasi similarity
    input_glcm = glcm(convert_to_grayscale(input_path))
    similarities = [(similarity_value, os.path.basename(path)) for path, similarity_value in zip(dataset_paths, [cosineSim(input_glcm, glcm(convert_to_grayscale(path))) * 100 for path in dataset_paths]) if similarity_value > 60]
    similarities.sort(reverse=True, key=lambda x: x[0])

