from flask import Blueprint, render_template, request, redirect, url_for

page_webscraping = Blueprint('page_webscraping', __name__)

@page_webscraping.route('/webscraping', methods=['GET', 'POST'])
def home():

    return render_template("page_webscraping.html")
