from flask import Flask

# setup the application
app = Flask(__name__)

# get configs 
app.config.from_prefixed_env()

# get routing info
import webapp.routes


