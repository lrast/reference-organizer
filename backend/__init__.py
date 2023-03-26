from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from database.oldInterface import database_setup
from backend.apis import api
from backend.buttons import button


# setup and configure the application
app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config.from_prefixed_env()
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(button, url_prefix='/button')

sqlaDB = SQLAlchemy()
sqlaDB.init_app(app)

import backend.views

database_setup(app)
