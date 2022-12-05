from flask import Flask

# setup and configure the application
app = Flask(__name__)
app.config.from_prefixed_env()

# get routing info
import webapp.routes
import webapp.dbInterface


