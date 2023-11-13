from flask import Flask
import os, shutil

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hololive jaya'

    from .page_userinput import page_userinput
    from .page_camera import page_camera
    from .page_webscraping import page_webscraping
    from .page_about import page_about
    
    app.register_blueprint(page_userinput, url_prefix='/')
    app.register_blueprint(page_camera, url_prefix='/')
    app.register_blueprint(page_webscraping, url_prefix='/')
    app.register_blueprint(page_about, url_prefix='/')

    return app