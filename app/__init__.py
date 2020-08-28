import os
from flask import Flask

from app.model import model
from app.appli import appli

def create_app():

    app = Flask(__name__)

    app.register_blueprint(model)
    app.register_blueprint(appli)


    return app






if __name__ == '__main__':
    my_app = create_app()
    my_app.run(debug=True)