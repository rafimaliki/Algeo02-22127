import os, shutil, time
import cbir_texture
from flask import Blueprint, render_template, request, redirect, url_for
# from website import get_result_images

page_userinput = Blueprint('page_userinput', __name__)
runtime = 0
result_images = []
selected_method = 0
scroll_position = 0

def get_result_images():
    import random, os, time
    global result_images
    time.sleep(1.2)
    result_folder = 'website/static/dataset_picture'
    result_images = [[image, random.randint(80, 97)+random.randint(0, 9)/10] for image in os.listdir(result_folder) if image.endswith(('.png', '.jpg', '.jpeg'))]
    result_images = sorted(result_images, key=lambda x: x[1], reverse=True)
    return result_images

@page_userinput.route('/userinput', methods=['GET', 'POST'])
def home():

    image_path = os.path.join('website/static/submitted_picture', 'submitted_image.png')

    if request.method == 'POST':
        if os.path.exists(image_path):
            os.remove(image_path)

    selected_image = 'submitted_image.png' if os.path.exists(image_path) else None
    len_dataset = len(os.listdir('website/static/dataset_picture'))

    # Get len result images
    len_result = len(result_images)

    # Pagination
    images_per_page = 5
    total_pages = (len(result_images) // images_per_page ) + 1 
    current_page = int(request.args.get('page', 1))

    start_index = (current_page - 1) * images_per_page
    end_index = start_index + images_per_page
    paginated_images = result_images[start_index:end_index]

    return render_template("page_userinput.html", selected_image=selected_image, 
                                                  len_dataset=len_dataset, 
                                                  result_images=paginated_images, 
                                                  total_pages=total_pages, 
                                                  current_page=current_page, 
                                                  runtime=runtime, 
                                                  len_result=len_result,
                                                  selected_method=selected_method)

@page_userinput.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        image.save(os.path.join('website/static/submitted_picture', 'submitted_image.png'))
    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/delete_image', methods=['GET','POST'])
def delete_image():
    image_path = os.path.join('website/static/submitted_picture', 'submitted_image.png')
    if os.path.exists(image_path):
        os.remove(image_path)
    global selected_method
    selected_method = 0
    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/upload_dataset_images', methods=['POST'])
def upload_dataset_images():
    # Clear existing images in the database_picture folder
    database_folder = 'website/static/dataset_picture'
    if os.path.exists(database_folder):
        shutil.rmtree(database_folder)
    os.makedirs(database_folder)

    # Save the uploaded images to the database_picture folder
    if 'images[]' in request.files:
        images = request.files.getlist('images[]')
        for image in images:
            image.save(os.path.join(database_folder, image.filename))

    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/delete_all_dataset_images', methods=['GET','POST'])
def delete_all_dataset_images():

    global result_images
    result_images = []
    database_folder = 'website/static/dataset_picture'
    if os.path.exists(database_folder):
        shutil.rmtree(database_folder)
        os.makedirs(database_folder)
    global selected_method
    selected_method = 0
    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/cbir_color', methods=['POST'])
def cbir_color():

    global selected_method
    selected_method = "color"

    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/cbir_texture', methods=['POST'])
def cbir_texture():

    global selected_method
    selected_method = "texture"

    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/run_search', methods=['POST'])
def run_search():
    
    global runtime
    runtime = time.time()

    if selected_method == "color":
        runtime = float(time.time())

        print("TRIGGER FUNCTION: CBIR Metode Color")
        result_images = get_result_images() 
    
        runtime = f"{round(float(time.time()) - float(runtime),3)}"

    else:
        runtime = float(time.time())

        print("TRIGGER FUNCTION: CBIR Metode Tekstur")
        result_images = cbir_texture.get_result_images()
    
        runtime = f"{round(float(time.time()) - float(runtime),3)}"

    return redirect(url_for('page_userinput.home'))