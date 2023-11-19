import os, shutil, time
from .cbir_texture import get_result_images_texture
from .cbir_color import get_result_images_color
from .webscrap import download_images
from math import ceil

from flask import Blueprint, render_template, request, redirect, url_for

page_userinput = Blueprint('page_userinput', __name__)
runtime = 0
result_images = []
selected_method = 0
scroll_position = 0
is_web_scrap = False

@page_userinput.route('/userinput', methods=['GET', 'POST'])
def home():

    image_path = os.path.join('website/static/submitted_picture', 'submitted_image.png')

    if request.method == 'POST':
        if os.path.exists(image_path):
            os.remove(image_path)

    selected_image = 'submitted_image.png' if os.path.exists(image_path) else None
    len_dataset = len(os.listdir('website/static/dataset_picture'))
    if len_dataset:
        dataset_images =  [image for image in os.listdir('website/static/dataset_picture') if image.endswith(('.png', '.jpg', '.jpeg'))]
    else:
        dataset_images = []

    # Get len result images
    len_result = len(result_images)

    # Pagination
    images_per_page = 5

    total_pages_result = ceil(len(result_images) // images_per_page )
    current_page_result = int(request.args.get('page_result', 1))
    start_index_result = (current_page_result - 1) * images_per_page
    end_index_result = start_index_result + images_per_page
    paginated_images_result = result_images[start_index_result:end_index_result]

    total_pages_dataset = ceil(len(dataset_images) // images_per_page )
    current_page_dataset = int(request.args.get('page_dataset', 1))
    start_index_dataset = (current_page_dataset - 1) * images_per_page
    end_index_dataset = start_index_dataset + images_per_page
    paginated_images_dataset = dataset_images[start_index_dataset:end_index_dataset]

    return render_template("page_userinput.html", selected_image=selected_image, 
                                                  len_dataset=len_dataset, 
                                                  result_images=paginated_images_result, 
                                                  total_pages_result=total_pages_result, 
                                                  current_page_result=current_page_result, 
                                                  runtime=runtime, 
                                                  len_result=len_result,
                                                  selected_method=selected_method,
                                                  isWebScrap=is_web_scrap,
                                                  total_pages_dataset=total_pages_dataset, 
                                                  current_page_dataset=current_page_dataset, 
                                                  dataset_images=paginated_images_dataset)

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
    global result_images

    if selected_method == "color":
        runtime = float(time.time())

        print("TRIGGER FUNCTION: CBIR Metode Color")
        result_images = get_result_images_color() 

        runtime = f"{round(float(time.time()) - float(runtime),3)}"
    
    else:
        runtime = float(time.time())

        print("TRIGGER FUNCTION: CBIR Metode Tekstur")
        result_images = get_result_images_texture()
        for image in result_images:
            image[1] = round(image[1], 2)

        runtime = f"{round(float(time.time()) - float(runtime),3)}"
    
    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/toggle_webscrap_button', methods=['POST', 'GET'])
def toggle_webscrap_button():

    global is_web_scrap
    if not(is_web_scrap):
        is_web_scrap = True
    else:
        is_web_scrap = False
    return redirect(url_for('page_userinput.home'))

@page_userinput.route('/run_webscrap', methods=['POST', 'GET'])
def run_webscrap():


    link_input = request.form['link_input']
    number_input = int(request.form['number_input'])
    print("TRIGGER WEBSCRAP")

    download_images(link_input, number_input)

    return redirect(url_for('page_userinput.home'))
