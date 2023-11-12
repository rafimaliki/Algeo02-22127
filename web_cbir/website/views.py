import os
from flask import Blueprint, render_template, request, redirect, url_for

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    image_path = os.path.join('website/static/submitted_picture', 'submitted_image.png')
    
    if request.method == 'POST':
        # If the form was submitted, check if the image exists
        if os.path.exists(image_path):
            os.remove(image_path)

    selected_image = 'submitted_image.png' if os.path.exists(image_path) else None
    return render_template("home.html", selected_image=selected_image)

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

@views.route('/cbir_color', methods=['POST'])
def cbir_color():
    print("TRIGGER FUNCTION: CBIR Metode Color")
    return redirect(url_for('views.home'))

@views.route('/cbir_texture', methods=['POST'])
def cbir_texture():
    print("TRIGGER FUNCTION: CBIR Metode Tekstur")
    return redirect(url_for('views.home'))
