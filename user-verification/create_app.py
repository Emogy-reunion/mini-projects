from flask import Flask
from config import Config
'''
This is an app factory
it creates the app instance so that other modules can import
    it without causing circular imports
'''


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    return app
