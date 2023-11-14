from website import create_app
import os, shutil

# Clear all images from folder
folder = 'website/static/dataset_picture'
if os.path.exists(folder):
    shutil.rmtree(folder)
os.makedirs(folder)

folder = 'website/static/submitted_picture'
if os.path.exists(folder):
    shutil.rmtree(folder)
os.makedirs(folder)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)