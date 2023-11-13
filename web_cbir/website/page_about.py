from flask import Blueprint, render_template, request, redirect, url_for

page_about = Blueprint('page_about', __name__)

@page_about.route('/', methods=['GET', 'POST'])
def home():

    return render_template("page_about.html")
