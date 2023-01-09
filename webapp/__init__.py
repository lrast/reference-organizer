from flask import Flask
from webapp.db import database_setup
from webapp.apis import api
from webapp.buttons import button


# setup and configure the application
app = Flask(__name__)
app.config.from_prefixed_env()
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(button, url_prefix='/button')

import webapp.routes


database_setup(app)
