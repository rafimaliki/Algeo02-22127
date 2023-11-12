from website import create_app
import os, shutil

# Clear all images from folder
database_folder = 'website/static/database_picture'
if os.path.exists(database_folder):
    shutil.rmtree(database_folder)
os.makedirs(database_folder)

database_folder = 'website/static/submitted_picture'
if os.path.exists(database_folder):
    shutil.rmtree(database_folder)
os.makedirs(database_folder)

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
