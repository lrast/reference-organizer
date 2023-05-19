import requests
import json

from flask import request, g
from flask import render_template, send_file, redirect, flash
from flask import url_for

from backend import app
from backend.utilities import isURLWebOrLocal

from database.oldInterface import get_db, addPageTopic



@app.route('/openpage/<int:pageid>', methods=['GET'])
def servePage(pageid):
    """Redirect to the URL of the requested page""" 
    db = get_db()
    url = db.execute("SELECT url FROM Page WHERE id=(?)", (pageid,)).fetchone()['url']

    URLsource, formattedURL = isURLWebOrLocal(url)
    if URLsource == 'web':
        return redirect(formattedURL)
    elif URLsource == 'local':
        return send_file(formattedURL)


# graph ql fiddle
from backend.api.graphQL import schema
from flask_graphql import GraphQLView
app.add_url_rule(
    '/graphiql',
    view_func=GraphQLView.as_view(
        'graphiql',
        schema=schema,
        graphiql=True
    )
)

