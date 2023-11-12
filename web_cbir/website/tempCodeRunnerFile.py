import random, os
global result_images
result_folder = 'website/static/database_picture'
result_images = [[image, random.randint(70, 90)] for image in os.listdir(result_folder) if image.endswith(('.png', '.jpg', '.jpeg'))]
result_images = sorted(result_images, key=lambda x: x[1], reverse=True)
print(result_images)