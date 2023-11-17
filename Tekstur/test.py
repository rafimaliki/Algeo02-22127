import os

import numpy as np
from skimage import io, color
from skimage.feature import greycomatrix
from skimage import img_as_ubyte
from skimage.metrics import structural_similarity as ssim
import matplotlib.pyplot as plt

# Load the image
image = io.imread('path_to_your_image.jpg')

# Convert the image to grayscale
gray_image = color.rgb2gray(image)

# Convert the image to unsigned byte (0-255)
gray_image = img_as_ubyte(gray_image)

# Define the distance and angles for GLCM
distances = [1, 2, 3]
angles = [0, np.pi/4, np.pi/2, 3*np.pi/4]

# Compute the GLCM
glcm = greycomatrix(gray_image, distances=distances, angles=angles, symmetric=True, normed=True)

# Calculate various similarity measures using GLCM
contrast = np.mean((glcm[:, :, 0, 0] * (np.arange(glcm.shape[0]) - np.arange(glcm.shape[0]).mean())**2).sum())
correlation = np.corrcoef(glcm[:, :, 0, 0].ravel(), np.arange(glcm.shape[0]).repeat(glcm.shape[0]))[0, 1]
homogeneity = np.sum(glcm[:, :, 0, 0] / (1 + np.abs(np.arange(glcm.shape[0]) - np.arange(glcm.shape[0]).mean())))
entropy = -np.sum(glcm[:, :, 0, 0] * np.log(glcm[:, :, 0, 0] + 1e-10))

# Print the similarity measures
print(f"Contrast: {contrast}")
print(f"Correlation: {correlation}")
print(f"Homogeneity: {homogeneity}")
print(f"Entropy: {entropy}")

# You can also calculate SSIM (Structural Similarity Index)
ssim_index, _ = ssim(gray_image, gray_image, full=True)
print(f"SSIM Index: {ssim_index}")

# Display the original image
plt.subplot(121)
plt.imshow(gray_image, cmap='gray')
plt.title('Original Image')

# Display the GLCM
plt.subplot(122)
plt.imshow(glcm[:, :, 0, 0], cmap='viridis', interpolation='nearest')
plt.title('GLCM')
plt.show()

