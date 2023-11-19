from flask import Flask
import os, shutil

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hololive jaya'

    from .page_home import page_home
    from .page_userinput import page_userinput
    from .page_camerainput import page_camerainput
    from .page_aboutus import page_aboutus
    
    app.register_blueprint(page_home, url_prefix='/')
    app.register_blueprint(page_userinput, url_prefix='/')
    app.register_blueprint(page_camerainput, url_prefix='/')
    app.register_blueprint(page_aboutus, url_prefix='/')

    return app