from flask import Blueprint, render_template, request, redirect, url_for

page_aboutus = Blueprint('page_aboutus', __name__)

@page_aboutus.route('/aboutus', methods=['GET', 'POST'])
def home():

    return render_template("page_aboutus.html")
