import os
current_folder = os.path.dirname(os.path.abspath(__file__))
folder_name = 'static\dataset_picture'
input_name = 'static\submitted_picture'
input_path = os.path.join(current_folder, input_name)
folder_path = os.path.join(current_folder, folder_name)
dataset_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, file))]
input_path = os.path.join(input_path, 'submitted_image.png')
print(input_path)