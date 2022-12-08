from flask import Flask

from webapp.db import database_setup


# setup and configure the application
app = Flask(__name__)
app.config.from_prefixed_env()

import webapp.routes

database_setup(app)



