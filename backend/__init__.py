from flask import Flask
from flask_cors import CORS

app = Flask(__name__,
            template_folder='../frontend/templates', 
            static_folder='../frontend/static'
            )
app.config.from_prefixed_env()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + app.root_path[:-7] + \
                                            app.config['DATABASE_URL']


import backend.views

# url configuration
from backend.apis import api

app.register_blueprint(api, url_prefix='/api')


# database configuration
from database.model import db as sqlaDB
sqlaDB.init_app(app)

from database.oldInterface import database_setup
database_setup(app)

# cors configuration
CORS(app, resources={r"/api/*": {"origins": 'http://localhost:3000'}})
