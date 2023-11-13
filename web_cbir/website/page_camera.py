from flask import Blueprint, render_template, request, redirect, url_for

page_camera = Blueprint('page_camera', __name__)

@page_camera.route('/camera', methods=['GET', 'POST'])
def home():

    return render_template("page_camera.html")
