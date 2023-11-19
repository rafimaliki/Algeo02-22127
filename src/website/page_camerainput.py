from flask import Blueprint, render_template, request, redirect, url_for

page_camerainput = Blueprint('page_camerainput', __name__)

@page_camerainput.route('/camerainput', methods=['GET', 'POST'])
def home():

    return render_template("page_camerainput.html")
