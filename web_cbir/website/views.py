import os, shutil, time
from flask import Blueprint, render_template, request, redirect, url_for
# from website import get_result_images

views = Blueprint('views', __name__)
runtime = 0

def get_result_images():
    result_folder = 'website/static/result_picture'
    result_images = [image for image in os.listdir(result_folder) if image.endswith(('.png', '.jpg', '.jpeg'))]
    return result_images

@views.route('/', methods=['GET', 'POST'])
def home():

    print("runtime:",runtime)

    image_path = os.path.join('website/static/submitted_picture', 'submitted_image.png')

    if request.method == 'POST':
        if os.path.exists(image_path):
            os.remove(image_path)

    selected_image = 'submitted_image.png' if os.path.exists(image_path) else None
    len_dataset = len(os.listdir('website/static/database_picture'))

    # Get result images
    result_images = get_result_images()

    # Pagination
    images_per_page = 5
    total_pages = (len(result_images) + images_per_page - 1) // images_per_page
    current_page = int(request.args.get('page', 1))

    start_index = (current_page - 1) * images_per_page
    end_index = start_index + images_per_page
    paginated_images = result_images[start_index:end_index]

    return render_template("home.html", selected_image=selected_image, len_dataset=len_dataset, result_images=paginated_images, total_pages=total_pages, current_page=current_page, runtime=runtime)

@views.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' in request.files:
        image = request.files['image']
        image.save(os.path.join('website/static/submitted_picture', 'submitted_image.png'))
    return redirect(url_for('views.home'))

@views.route('/delete_image', methods=['POST'])
def delete_image():
    image_path = os.path.join('website/static/submitted_picture', 'submitted_image.png')
    if os.path.exists(image_path):
        os.remove(image_path)
    return redirect(url_for('views.home'))

@views.route('/upload_database_images', methods=['POST'])
def upload_database_images():
    # Clear existing images in the database_picture folder
    database_folder = 'website/static/database_picture'
    if os.path.exists(database_folder):
        shutil.rmtree(database_folder)
    os.makedirs(database_folder)

    # Save the uploaded images to the database_picture folder
    if 'images[]' in request.files:
        images = request.files.getlist('images[]')
        for image in images:
            image.save(os.path.join(database_folder, image.filename))

    return redirect(url_for('views.home'))

@views.route('/delete_all_dataset_images', methods=['POST'])
def delete_all_dataset_images():
    database_folder = 'website/static/database_picture'
    if os.path.exists(database_folder):
        shutil.rmtree(database_folder)
        os.makedirs(database_folder)
    return redirect(url_for('views.home'))

@views.route('/cbir_color', methods=['POST'])
def cbir_color():
    print("TRIGGER FUNCTION: CBIR Metode Color")
    return redirect(url_for('views.home'))

@views.route('/cbir_texture', methods=['POST'])
def cbir_texture():

    global runtime
    runtime = time.time()
    
    print("TRIGGER FUNCTION: CBIR Metode Tekstur")

    def copy_images(source_folder, destination_folder, image_filenames):
        for image_filename in image_filenames:
            source_path = os.path.join(source_folder, image_filename)
            destination_path = os.path.join(destination_folder, image_filename)

            try:
                shutil.copy2(source_path, destination_path)
                print(f"Image '{image_filename}' copied successfully.")
            except FileNotFoundError:
                print(f"Error: Image '{image_filename}' not found.")
            except Exception as e:
                print(f"Error: {e}")

    # Example usage:
    source_folder = "../dataset"
    destination_folder = "website/static/result_picture"
    image_filenames_to_copy = [f"{i}.jpg" for i in range(30)]
    copy_images(source_folder, destination_folder, image_filenames_to_copy)

    runtime = f"{round(time.time() - runtime,3)} s"

    return redirect(url_for('views.home'))