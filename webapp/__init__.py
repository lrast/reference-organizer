from flask import Flask
from webapp.db import database_setup
from webapp.apis import api


# setup and configure the application
app = Flask(__name__)
app.config.from_prefixed_env()
app.register_blueprint(api, url_prefix='/api')

import webapp.routes
import webapp.buttons

database_setup(app)
