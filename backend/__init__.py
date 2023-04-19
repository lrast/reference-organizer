from flask import Flask
from flask_cors import CORS

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config.from_prefixed_env()

import backend.views


# url configuration
from backend.apis import api
from backend.buttons import button

app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(button, url_prefix='/button')


# database configuration
from database.model import db as sqlaDB
sqlaDB.init_app(app)

from database.oldInterface import database_setup
database_setup(app)

# cors configuration
CORS(app, resources={r"/api/*": {"origins": 'http://localhost:3000'}} )
