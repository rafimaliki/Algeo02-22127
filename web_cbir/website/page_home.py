from flask import Blueprint, render_template, request, redirect, url_for

page_home = Blueprint('page_home', __name__)

@page_home.route('/', methods=['GET', 'POST'])
def home():

    return render_template("page_home.html")
